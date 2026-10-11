from solver import solve_cover, DEMO_LOOKS, DEMO_ASSETS

checks = []
def check(name, predicate):
    assert predicate, name
    checks.append(name)

demo = solve_cover(DEMO_LOOKS, DEMO_ASSETS)
check("greedy counterexample has exact two-asset solution",
      demo["minimum"] == 2 and {a["id"] for a in demo["selected"]} == {"B", "C"})
check("every look has an assignment from declared coverage",
      all(look in next(a["covers"] for a in demo["selected"] if a["id"] == asset)
          for look, asset in demo["assignment"].items()))
gap = solve_cover(["X", "Y"], [{"id": "a", "covers": "X"}])
check("uncovered look is reported without a false plan", gap["missing"] == ["Y"])
tie = solve_cover(["X"], [{"id": "a", "covers": "X"}, {"id": "b", "covers": "X"}])
check("equal minimum alternatives are retained", tie["alternatives"] == [["a"], ["b"]])
for name, looks, assets in [
    ("duplicate look IDs rejected", ["X", "X"], []),
    ("duplicate asset IDs rejected", ["X"], [{"id": "a", "covers": "X"},
                                            {"id": "a", "covers": "X"}]),
    ("unknown coverage target rejected", ["X"], [{"id": "a", "covers": "Y"}]),
    ("empty look ID rejected", [""], []),
]:
    try:
        solve_cover(looks, assets)
    except ValueError:
        check(name, True)
    else:
        raise AssertionError(name)
print({"passed": len(checks), "checks": checks})
