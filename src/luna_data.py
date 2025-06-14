from skyfield.api import load, Topos, load_constellation_map
from skyfield.almanac import find_discrete, moon_phases
from skyfield import almanac
from datetime import datetime, timedelta
import json
import math

# Load constellation map
constellation_map = load_constellation_map()

# Load astronomical data
ts = load.timescale()
eph = load('de421.bsp')
sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

# ======================
# 1. Get Moon Phases (New/Full/Quarter)
# ======================

def illumination_at(t):
    """Calculate moon illumination percentage (0-100) correctly"""
    e = earth.at(t)
    s = e.observe(sun).apparent()
    m = e.observe(moon).apparent()
    angle = s.separation_from(m).radians
    illumination = (1 - math.cos(angle))/2  # Correct formula
    return round(illumination * 100)

def get_moon_phases_daily(year=2025):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    current_date = start_date
    phases = []

    while current_date <= end_date:
        t = ts.utc(current_date.year, current_date.month, current_date.day)
        e = earth.at(t)
        sun_pos = e.observe(sun).apparent()
        moon_pos = e.observe(moon).apparent()
        angle = sun_pos.separation_from(moon_pos).degrees
        illumination = round((1 - math.cos(math.radians(angle))) / 2 * 100)
        phase_name = get_moon_phase_name(angle)
        
        phases.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "phase": phase_name,
            "illumination": illumination
        })

        current_date += timedelta(days=1)

    return phases

def get_moon_phase_name(angle_deg):
    angle_deg = angle_deg % 360  # Normalize angle between 0-360
    if angle_deg < 10 or angle_deg > 350:
        return "New Moon"
    elif 10 <= angle_deg < 90:
        return "Waxing Crescent"
    elif 90 <= angle_deg < 100:
        return "First Quarter"
    elif 100 <= angle_deg < 170:
        return "Waxing Gibbous"
    elif 170 <= angle_deg < 190:
        return "Full Moon"
    elif 190 <= angle_deg < 260:
        return "Waning Gibbous"
    elif 260 <= angle_deg < 280:
        return "Last Quarter"
    elif 280 <= angle_deg <= 350:
        return "Waning Crescent"
    else:
        return "Unknown"

# ======================
# 2. Detect Eclipses (Fixed)
# ======================
def get_all_eclipses(year=2025):
    eclipses = []
    t0 = ts.utc(year, 1, 1)
    t1 = ts.utc(year, 12, 31)

    current_time = t0.utc_datetime()
    end_time = t1.utc_datetime()
    step = timedelta(minutes=30)

    while current_time <= end_time:
        t = ts.utc(current_time)
        e = earth.at(t)
        sun_pos = e.observe(sun).apparent()
        moon_pos = e.observe(moon).apparent()
        separation_deg = sun_pos.separation_from(moon_pos).degrees

        # Calculate moon phase angle
        angle = separation_deg
        illumination = (1 - math.cos(math.radians(angle))) / 2 * 100

        # Lunar eclipse (Full Moon and opposite Sun)
        if 178 <= angle <= 182 and illumination > 95:
            eclipses.append({
                "date": t.utc_strftime("%Y-%m-%d %H:%M"),
                "type": "Lunar Eclipse",
                "visibility": "Visible at night"
            })

        # Solar eclipse (New Moon and near Sun)
        if angle < 1.5 and illumination < 5:
            eclipse_type = "Solar Eclipse (Total)" if angle < 0.5 else "Solar Eclipse (Partial)"
            eclipses.append({
                "date": t.utc_strftime("%Y-%m-%d %H:%M"),
                "type": eclipse_type,
                "visibility": "Visible in daytime"
            })

        current_time += step

    # Deduplicate
    seen = set()
    unique_eclipses = []
    for e in eclipses:
        key = (e['date'][:10], e['type'])
        if key not in seen:
            seen.add(key)
            unique_eclipses.append(e)

    return sorted(unique_eclipses, key=lambda x: x['date'])

# ======================
# 3. Planet Positions 
# ======================
def get_planet_positions_over_year(planet_name="JUPITER", year=2025):
    # Map to ephemeris keys exactly as they appear in de421
    planet_key_map = {
        "MERCURY": "mercury barycenter",
        "VENUS": "venus barycenter",
        "EARTH": "earth barycenter",
        "MARS": "mars barycenter",
        "JUPITER": "jupiter barycenter",
        "SATURN": "saturn barycenter",
        "URANUS": "uranus barycenter",
        "NEPTUNE": "neptune barycenter",
        "PLUTO": "pluto barycenter",
        "SUN": "sun",
        "MOON": "moon"
    }

    key = planet_key_map.get(planet_name.upper())
    if key is None:
        raise ValueError(f"Planet '{planet_name}' not recognized.")

    planet = eph[key]

    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    current_date = start_date
    results = []

    while current_date <= end_date:
        t = ts.utc(current_date.year, current_date.month, current_date.day)
        astro = earth.at(t).observe(planet).apparent()
        ra, dec, _ = astro.radec()
        constellation_name = constellation_map(astro)

        results.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "RA": f"{ra.hours:.2f}h",
            "Dec": f"{dec.degrees:.2f}°",
            "Constellation": constellation_name
        })

        current_date += timedelta(days=1)

    return results

# ======================
# Run and Save Data
# ======================
if __name__ == "__main__":
    print("Fetching astronomical data...")

    moon_phases = get_moon_phases_daily()
    eclipses = get_all_eclipses()        # Use the combined lunar + solar eclipse finder now
    jupiter_positions = get_planet_positions_over_year()

    data = {
        "moon_phases": moon_phases,
        "eclipses": eclipses,
        "planet_positions": jupiter_positions
    }

    with open("astronomy_data.json", "w") as f:
        json.dump(data, f, indent=2)

    print("=== First 5 Moon Phases ===")
    print(json.dumps(moon_phases[:5], indent=2))

    print("\n=== First 3 Jupiter Positions ===")
    print(json.dumps(jupiter_positions[:3], indent=2))

    print("\n=== Eclipses ===")
    print(json.dumps(eclipses, indent=2))

    print("\nData saved to 'astronomy_data.json'")

