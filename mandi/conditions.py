"""Plain-text lines built from real weather numbers and from which agents answered. Pure functions, no network."""


def weather_line(items, labels) -> str | None:
    """'Weather today' line from WeatherInfo-like items; None when no place has data. Numbers come straight from the source."""
    bits, notes = [], []
    for it, label in zip(items, labels):
        if not it.found or it.max_c is None:
            continue
        rain = f", rain chance {it.rain_chance_pct:.0f}%" if it.rain_chance_pct is not None else ""
        bits.append(f"{label} {it.max_c:.0f}°C (low {it.min_c:.0f}°C){rain}")
        if it.rain_chance_pct is not None and it.rain_chance_pct >= 50:
            notes.append(f"rain is likely around {label} ({it.rain_chance_pct:.0f}%), so cover the load")
        if it.max_c >= 36:
            notes.append(f"{label} is hot ({it.max_c:.0f}°C), and heat speeds up spoilage")
    if not bits:
        return None
    line = "**Weather today** (Open-Meteo): " + "; ".join(bits) + "."
    if notes:
        line += " Take note: " + "; ".join(notes) + ". The transit-loss assumption below does not change with the weather."
    return line


def agents_used_line(priced: int, routed: int, weather_ok: bool, explained: bool) -> str:
    parts = [f"Price Agent ({priced} mandis priced, data.gov.in)", f"Logistics Agent ({routed} routes, OpenStreetMap/OSRM)"]
    parts.append("Weather Agent (Open-Meteo)" if weather_ok else "Weather Agent (no answer this time)")
    parts.append("ASI1 (reading your request" + (" and writing the explanation)" if explained else ")"))
    return "_Agents that worked on this answer: " + ", ".join(parts) + "._"
