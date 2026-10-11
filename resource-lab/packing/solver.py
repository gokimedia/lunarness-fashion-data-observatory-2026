"""Exact set-cover planning for declared coverage of sequential shoot looks."""
from itertools import combinations


def solve_cover(looks, assets):
    looks = [str(x).strip() for x in looks]
    if not looks or len(set(looks)) != len(looks) or any(not x for x in looks):
        raise ValueError("Use one or more unique, non-empty look IDs.")
    if len(looks) > 12 or len(assets) > 18:
        raise ValueError("This small exact solver supports up to 12 looks and 18 assets.")
    target = set(looks)
    seen = set()
    normalized = []
    for row in assets:
        key = str(row["id"]).strip()
        if not key or key in seen:
            raise ValueError("Asset IDs must be unique and non-empty.")
        seen.add(key)
        declared = row["covers"]
        coverage = ({s.strip() for s in declared.split(",") if s.strip()}
                    if isinstance(declared, str) else {str(s).strip() for s in declared})
        if coverage - target:
            raise ValueError(f"{key} refers to a look that is not in the look list.")
        normalized.append({"id": key, "name": str(row.get("name", key)),
                           "covers": coverage})
    missing = target - set().union(*(a["covers"] for a in normalized)) if normalized else target
    if missing:
        return {"status": "uncovered", "missing": sorted(missing), "selected": [],
                "alternatives": [], "minimum": None}
    # Enumerating increasing cardinalities proves the first solution is minimal.
    for count in range(1, len(normalized) + 1):
        winners = []
        for subset in combinations(normalized, count):
            if target <= set().union(*(a["covers"] for a in subset)):
                winners.append(subset)
                if len(winners) == 8:
                    break
        if winners:
            chosen = winners[0]
            return {
                "status": "covered", "minimum": count, "missing": [],
                "selected": [{"id": a["id"], "name": a["name"],
                              "covers": sorted(a["covers"])} for a in chosen],
                "alternatives": [[a["id"] for a in group] for group in winners],
                "alternatives_limited_to": 8,
                "assignment": {look: next(a["id"] for a in chosen if look in a["covers"])
                               for look in looks}
            }
    raise RuntimeError("Coverage was feasible but no set was found.")


DEMO_LOOKS = ["L1", "L2", "L3", "L4", "L5", "L6"]
DEMO_ASSETS = [
    {"id": "A", "name": "DEMO broad accessory", "covers": "L1,L2,L3,L4"},
    {"id": "B", "name": "DEMO accessory B", "covers": "L1,L2,L5"},
    {"id": "C", "name": "DEMO accessory C", "covers": "L3,L4,L6"},
    {"id": "D", "name": "DEMO single-look piece D", "covers": "L5"},
    {"id": "E", "name": "DEMO single-look piece E", "covers": "L6"},
]
