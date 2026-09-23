"""
Sample data generator for the Kigali driver lookup assignment.

Produces the "raw list of driver objects" the delivery app currently scans
one by one. Import generate_drivers() into your own solution, or run this
file directly to write drivers.json.
"""
import json
import random

FIRST_NAMES = [
    "Jean", "Eric", "Claude", "Patrick", "Emmanuel", "Innocent", "Olivier",
    "Aline", "Diane", "Grace", "Josiane", "Clarisse", "Yves", "Fabrice",
    "Alice", "Didier", "Chantal", "Theogene", "Esperance", "Gilbert",
]
LAST_NAMES = [
    "Habimana", "Uwimana", "Niyonzima", "Mugisha", "Ishimwe", "Nshimiyimana",
    "Uwase", "Hakizimana", "Mukamana", "Niyitegeka", "Tuyishime", "Iradukunda",
    "Kayitesi", "Bizimana", "Ingabire", "Munyaneza",
]
SECTORS = {
    "Gasabo": ["Kimihurura", "Remera", "Kacyiru", "Kimironko", "Gisozi", "Kinyinya"],
    "Kicukiro": ["Gikondo", "Kanombe", "Kicukiro", "Niboye", "Kagarama"],
    "Nyarugenge": ["Nyamirambo", "Muhima", "Nyarugenge", "Gitega", "Kimisagara"],
}


def generate_drivers(n=10_000, seed=42):
    """Return a shuffled list of n driver dicts (same output for same seed)."""
    rng = random.Random(seed)
    drivers = []
    for i in range(1, n + 1):
        district = rng.choice(list(SECTORS))
        drivers.append({
            "driver_id": f"KGL-{i:05d}",
            "name": f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}",
            "phone": f"+2507{rng.choice('2389')}{rng.randint(0, 9_999_999):07d}",
            "vehicle": rng.choices(["motorcycle", "bicycle", "car"], weights=[70, 15, 15])[0],
            "district": district,
            "sector": rng.choice(SECTORS[district]),
            "location": {
                "lat": round(rng.uniform(-2.02, -1.90), 6),
                "lng": round(rng.uniform(30.00, 30.15), 6),
            },
            "status": rng.choices(["available", "on_delivery", "offline"], weights=[50, 30, 20])[0],
            "rating": round(rng.uniform(3.5, 5.0), 1),
        })
    rng.shuffle(drivers)  # real-world lists aren't sorted by ID
    return drivers


def sample_requests(drivers, k=10_000, missing_ratio=0.05, seed=7):
    """Return k driver IDs to look up; a small share are IDs that don't exist."""
    rng = random.Random(seed)
    ids = [d["driver_id"] for d in drivers]
    requests = []
    for _ in range(k):
        if rng.random() < missing_ratio:
            requests.append(f"KGL-{rng.randint(90_000, 99_999)}")  # not in the data
        else:
            requests.append(rng.choice(ids))
    return requests


if __name__ == "__main__":
    drivers = generate_drivers()
    with open("drivers.json", "w", encoding="utf-8") as f:
        json.dump(drivers, f, indent=2)
    print(f"Wrote {len(drivers):,} drivers to drivers.json")
    print("Example:", drivers[0])