"""Offline self-tests (no network, no agents): python -m mandi.selftest

Numbers below are made-up TEST FIXTURES to check the maths, not data the agents ever show.
"""
import json
import tempfile
from pathlib import Path
from unittest import mock

from mandi import core, extras
from mandi.core import Assumptions
from mandi.logistics_agent import _clean
from mandi.models import MandiRow, RouteInfo
from mandi.ranking import format_reply, rank, search_states


def fixture():
    rows = [MandiRow(market=m, district=d, state="Haryana", variety="V", arrival_date="01/01/2026",
                     min_price=p - 100, max_price=p + 100, modal_price=p)
            for m, d, p in (("Near APMC", "A", 2000.0), ("Mid APMC", "B", 2300.0), ("Far APMC", "C", 2600.0))]
    routes = [RouteInfo(market="Near APMC", district="A", state="Haryana", distance_km=20, drive_hours=0.5),
              RouteInfo(market="Mid APMC", district="B", state="Haryana", distance_km=100, drive_hours=1.5),
              RouteInfo(market="Far APMC", district="C", state="Haryana", distance_km=300, drive_hours=4.5, approx=True)]
    return rows, routes


def test_net_price_math():
    a = Assumptions(truck_rate_rs_per_tonne_km=3.0, market_fee_pct=2.0, commission_pct=0.0,
                    spoilage_pct_per_hour={"default": 0.2})
    transport, spoilage, fees, net = core.net_price(1000.0, 100.0, 2.0, "x", a)
    assert abs(transport - 30.0) < 1e-9  # 3 Rs x 100 km x 0.1 tonne per quintal
    assert abs(spoilage - 4.0) < 1e-9  # 1000 x 0.2% x 2 h
    assert abs(fees - 20.0) < 1e-9
    assert abs(net - 946.0) < 1e-9


def test_rank_sell_and_buy():
    rows, routes = fixture()
    a = Assumptions()
    sell = rank(rows, routes, "tomato", "sell", a)
    assert [r.market for r in sell][0] in ("Far APMC", "Mid APMC")
    assert sell[0].net >= sell[1].net >= sell[2].net  # highest net first
    buy = rank(rows, routes, "tomato", "buy", a)
    assert buy[0].net <= buy[1].net <= buy[2].net  # lowest landed cost first
    assert buy[0].market == "Near APMC"
    assert all(r.fees == 0.0 for r in buy)  # buyer does not pay the seller-side fees


def test_reply_text():
    rows, routes = fixture()
    res = rank(rows, routes, "tomato", "sell", Assumptions())
    text = format_reply(res, "Tomato", "Gurugram, Haryana", "sell", 80, Assumptions(), 1)
    assert "Recommendation" in text and "1 market was skipped" in text and "~" in text


def depth(node, d=1):
    kids = node.get("children", []) if isinstance(node, dict) else []
    if isinstance(node, dict) and node.get("type") == "list":
        kids = [c for item in node.get("items", []) for c in item.get("children", [])] + kids
    return max([d] + [depth(k, d + 1) for k in kids])


def test_card_payload_valid():
    rows, routes = fixture()
    res = rank(rows, routes, "tomato", "sell", Assumptions())
    payload = extras.build_card_payload(res, "Tomato", "Gurugram, Haryana", "sell", 80)
    raw = json.dumps(payload)
    assert len(raw) < 64 * 1024
    assert payload["root"]["type"] == "section"
    assert depth(payload["root"]) + 1 <= 8  # list items add a level
    msg = extras.card_message("hi", payload)
    meta = msg.content[1].metadata
    assert meta["card_protocol_version"] == "1" and meta["requires_card_interaction"] == "true"
    assert meta["card_kind"] == "custom" and all(isinstance(v, str) for v in meta.values())
    buttons = [c for it in payload["root"]["children"][0]["items"] for c in it["children"] if c["type"] == "button"]
    assert len(buttons) == 3 and buttons[0]["primary"] is True
    sel = buttons[1]["action"]["selection"]
    assert extras.parse_selection(json.dumps(sel))["rank"] == 1


def test_parse_selection_rejects_other_text():
    assert extras.parse_selection("I have 8 tonnes of tomato") is None
    assert extras.parse_selection(json.dumps({"action": "other"})) is None
    assert extras.parse_selection("[1,2]") is None


def test_plan_load():
    rows, routes = fixture()
    a = Assumptions()
    res = rank(rows, routes, "tomato", "sell", a)
    one = extras.plan_load(res, 0, 80, a, "sell")
    assert "1 truck" in one and "spread" not in one.lower()
    many = extras.plan_load(res, 0, 250, a, "sell")  # 250 qtl -> 3 trucks of 100 qtl
    assert "3 trucks" in many and "spread the trucks" in many
    unknown = extras.plan_load(res, 0, None, a, "sell")
    assert "assumed one full truck" in unknown


def test_snapshot_fallback():
    with tempfile.TemporaryDirectory() as tmp, mock.patch.object(core, "SNAPSHOT_DIR", Path(tmp)):
        live = [{"state": "Haryana", "market": "M"}, {"state": "Punjab", "market": "N"}]
        with mock.patch.object(core, "fetch_prices", return_value=live):
            rows, info = core.fetch_prices_with_source("Tomato")
        assert info["source"] == "live" and len(rows) == 2
        with mock.patch.object(core, "fetch_prices", side_effect=RuntimeError("down")):
            rows, info = core.fetch_prices_with_source("Tomato")
            assert info["source"] == "snapshot" and info["fetched_at"] and len(rows) == 2
            rows, info = core.fetch_prices_with_source("Tomato", "Haryana")
            assert [r["market"] for r in rows] == ["M"]
            try:
                core.fetch_prices_with_source("Unseen crop")
                raise AssertionError("expected an error with no snapshot")
            except RuntimeError:
                pass


def test_estimate_route_and_clean_and_states():
    km, h = core.estimate_route((28.46, 77.03), (28.72, 77.16))
    assert 30 < km < 60 and abs(h - km / 45.0) < 1e-9
    assert _clean("New Grain Market , Faridabad APMC") == "Faridabad"
    assert _clean("Barwala(Hisar) APMC") == "Barwala"
    assert "Haryana" in search_states("Haryana") and "Punjab" in search_states("Haryana")
    assert search_states(None) == []


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok  ", t.__name__)
    print(f"\n{len(tests)} tests passed")
