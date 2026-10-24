"""Offline tests for the 25 Oct upgrades: memory and follow-ups, grounded explanation, cached and parallel routing.

    python -m mandi.test_upgrades

Kept apart from mandi.selftest on purpose, so that file still reports its nine tests. Numbers are made-up fixtures.
"""
import json
import tempfile
from pathlib import Path
from unittest import mock

from mandi import conditions, core, logistics_agent, personal, weather_agent
from mandi.core import Assumptions
from mandi.models import Place, RouteRequest, WeatherInfo, WeatherRequest
from mandi.ranking import rank
from mandi.selftest import fixture

SAVED = {"intent": "sell", "commodity": "Tomato", "origin": "Gurugram, Haryana", "origin_state": "Haryana",
         "quantity_quintals": 250, "truck_rate_rs_per_tonne_km": 4.0}


def test_follow_up_inherits_saved_profile():
    merged, filled = personal.merge_request({"intent": "other", "quantity_quintals": 600}, SAVED)
    assert merged["intent"] == "sell" and merged["commodity"] == "Tomato"
    assert merged["origin"] == "Gurugram, Haryana" and merged["origin_state"] == "Haryana"
    assert merged["quantity_quintals"] == 600 and merged["truck_rate_rs_per_tonne_km"] == 4.0
    assert "crop" in filled and "place" in filled


def test_not_a_mandi_question_is_left_alone():
    merged, filled = personal.merge_request({"intent": "other"}, SAVED)
    assert merged["intent"] == "other" and not filled and "commodity" not in merged


def test_new_crop_drops_old_quantity_and_new_place_drops_old_state():
    merged, _ = personal.merge_request({"intent": "sell", "commodity": "Onion"}, SAVED)
    assert merged["commodity"] == "Onion" and merged["origin"] == "Gurugram, Haryana"
    assert merged.get("quantity_quintals") in (None, "")  # 250 quintals was tomato
    assert "quantity_quintals" not in personal.remember(SAVED, merged)
    merged, _ = personal.merge_request({"intent": "sell", "origin": "Jaipur"}, SAVED)
    assert merged["origin"] == "Jaipur" and not merged.get("origin_state")  # Haryana belonged to Gurugram


def test_remember_forget_and_memory_line():
    saved = personal.remember({}, {"intent": "buy", "commodity": "Onion", "origin": "Delhi", "commission_pct": 6, "language": "hi"})
    assert saved["language"] == "hi" and saved["commission_pct"] == 6 and saved["intent"] == "buy"
    assert "Onion" in personal.memory_line(saved) and "6%" in personal.memory_line(saved)
    assert personal.memory_line({}) == ""
    for phrase in ("forget me", "Please clear my memory", "reset my settings", "mujhe bhool jao", "मुझे भूल जाओ"):
        assert personal.is_forget(phrase), phrase
    assert not personal.is_forget("I forgot to say the price") and not personal.is_forget("where do I sell tomato")
    assert personal.clean_language("fr") == "en" and personal.clean_language("hinglish") == "hinglish"


def test_grounding_accepts_facts_and_rejects_invented_numbers_and_advice():
    rows, routes = fixture()
    results = rank(rows, routes, "tomato", "sell", Assumptions())
    facts = personal.facts_text(results, "sell", 100, Assumptions())
    best = results[0]
    ok = f"{best.market} clears Rs {best.net:,.0f} a quintal after {best.distance_km:.0f} km of driving."
    assert personal.grounded(ok, facts)
    assert not personal.grounded(f"{best.market} clears Rs {best.net + 777:,.0f} a quintal.", facts)  # invented number
    assert not personal.grounded("Prices will rise tomorrow, so wait.", facts)  # no forecasts or timing advice
    assert not personal.grounded("", facts)
    hindi = f"{best.market} में आपको {str(int(round(best.net))).translate(str.maketrans('0123456789', '०१२३४५६७८९'))} रुपये प्रति क्विंटल मिलेंगे।"
    assert personal.grounded(hindi, facts)  # Devanagari digits are read as the same number


def test_why_prompt_carries_language_and_only_the_top_rows():
    rows, routes = fixture()
    results = rank(rows, routes, "tomato", "sell", Assumptions())
    facts = personal.facts_text(results, "sell", None, Assumptions(), top=2)
    assert results[0].market in facts and "3. " not in facts.splitlines()[1]
    sys_msg = personal.why_messages(facts, "hi", "sell")[0]["content"]
    assert "Hindi" in sys_msg and "ONLY the facts" in sys_msg
    assert "Hinglish" in personal.why_messages(facts, "hinglish", "buy")[0]["content"]


def test_route_cache_hits_disk_and_skips_the_network():
    calls = []

    def fake_get(url, **kw):
        calls.append(url)
        resp = mock.Mock()
        resp.json.return_value = {"code": "Ok", "routes": [{"distance": 50000.0, "duration": 3600.0}]}
        return resp

    with tempfile.TemporaryDirectory() as d, mock.patch.object(core, "ROUTE_CACHE", Path(d) / "r.json"), \
            mock.patch.object(core, "_routes", None), mock.patch.object(core.httpx, "get", fake_get):
        assert core.road_route((28.46, 77.03), (28.9, 77.5)) == (50.0, 1.0)
        assert core.road_route((28.46, 77.03), (28.9, 77.5)) == (50.0, 1.0)
        assert len(calls) == 1  # second answer came from the cache
        core.save_route_cache()
        assert json.loads((Path(d) / "r.json").read_text())  # persisted for the next process


def test_parallel_routing_keeps_order_and_counts_estimates():
    places = [Place(market=f"M{i}", district="D", state="Haryana") for i in range(8)]

    def fake_locate(p):
        i = int(p.market[1:])
        return (28.46 + 0.05 * i, 77.03), i == 5  # M5 is a district-centre guess (approx)

    def fake_route(a, b):
        if abs(b[0] - (28.46 + 0.05 * 3)) < 1e-9:
            raise RuntimeError("routing service down")  # M3 falls back to an estimate
        return 10.0 + b[0], 1.0

    with mock.patch.object(logistics_agent, "geocode", lambda q: (28.46, 77.03)), \
            mock.patch.object(logistics_agent, "_locate", fake_locate), \
            mock.patch.object(logistics_agent, "road_route", fake_route), \
            mock.patch.object(logistics_agent, "save_route_cache", lambda: None):
        rep = logistics_agent.compute(RouteRequest(origin="Gurugram", places=places, max_radius_km=300))
    assert [r.market for r in rep.routes] == [f"M{i}" for i in range(8)]
    assert rep.estimated == 1 and rep.routes[3].approx and rep.routes[5].approx and not rep.routes[0].approx
    assert rep.skipped == 0


def test_open_meteo_payload_is_parsed_and_junk_is_rejected():
    payload = {"daily": {"time": ["2026-10-25"], "temperature_2m_max": [31.5], "temperature_2m_min": [20.5],
                         "precipitation_probability_max": [4], "precipitation_sum": [0.0]}}
    w = core.parse_weather(payload)
    assert w == {"date": "2026-10-25", "max_c": 31.5, "min_c": 20.5, "rain_chance_pct": 4, "rain_mm": 0.0}
    assert core.parse_weather({}) is None and core.parse_weather({"daily": {"time": []}}) is None


def test_weather_line_uses_source_numbers_and_flags_rain_and_heat_only_when_true():
    mild = WeatherInfo(place="A", found=True, max_c=31.5, min_c=20.5, rain_chance_pct=4, rain_mm=0)
    wet = WeatherInfo(place="B", found=True, max_c=29.0, min_c=22.0, rain_chance_pct=80, rain_mm=12)
    hot = WeatherInfo(place="C", found=True, max_c=39.0, min_c=27.0, rain_chance_pct=0, rain_mm=0)
    gone = WeatherInfo(place="D", found=False)
    line = conditions.weather_line([mild, wet, hot, gone], ["Gurugram", "Rohtak", "Jaipur", "Nowhere"])
    assert "Gurugram 32°C" in line or "Gurugram 31°C" in line  # one decimal place of the source, shown as a whole number
    assert "rain is likely around Rohtak (80%)" in line and "Jaipur is hot (39°C)" in line
    assert "Nowhere" not in line and "does not change with the weather" in line
    calm = conditions.weather_line([mild], ["Gurugram"])
    assert "Take note" not in calm  # no warning when nothing warrants one
    assert conditions.weather_line([gone], ["X"]) is None


def test_agents_used_line_names_every_agent_and_is_honest_about_a_missing_one():
    full = conditions.agents_used_line(30, 16, True, True)
    assert "Price Agent (30 mandis" in full and "16 routes" in full and "Weather Agent (Open-Meteo)" in full
    assert "writing the explanation" in full
    partial = conditions.agents_used_line(30, 16, False, False)
    assert "no answer this time" in partial and "writing the explanation" not in partial


def test_weather_agent_geocodes_then_fetches_in_parallel_and_marks_missing_places():
    def fake_geocode(q):
        return None if q == "Nowhere" else (28.0 + len(q) / 100, 77.0)

    def fake_weather(lat, lon):
        return {"date": "2026-10-25", "max_c": 30.0, "min_c": 20.0, "rain_chance_pct": 10, "rain_mm": 0.0}

    with mock.patch.object(weather_agent, "geocode", fake_geocode), mock.patch.object(weather_agent, "weather_today", fake_weather):
        rep = weather_agent.compute(WeatherRequest(places=["Gurugram, Haryana", "Nowhere", "Rohtak, Haryana, India"]))
    assert [i.place for i in rep.items] == ["Gurugram, Haryana", "Nowhere", "Rohtak, Haryana, India"]
    assert [i.found for i in rep.items] == [True, False, True] and rep.items[0].max_c == 30.0 and rep.items[1].max_c is None


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok  ", t.__name__)
    print(f"\n{len(tests)} tests passed")
