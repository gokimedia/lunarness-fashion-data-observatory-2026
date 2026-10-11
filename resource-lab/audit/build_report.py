"""Build a static, reproducible audit of the existing public data compilation."""
import ast
import json
from decimal import Decimal
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "fashion_observatory_2026.json"


def arithmetic(expression):
    def visit(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return Decimal(str(node.value))
        if isinstance(node, ast.BinOp):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
        raise ValueError("Only numeric arithmetic is allowed in a derivation.")
    return visit(ast.parse(expression, mode="eval").body)


def representation(record):
    if "value" in record:
        return "point", str(record["value"])
    if "value_lower_bound" in record:
        return "lower bound", "≥ " + str(record["value_lower_bound"])
    if "value_min" in record and "value_max" in record:
        return "range", f'{record["value_min"]}–{record["value_max"]}'
    raise ValueError("Missing numeric representation: " + record["id"])


def quantity(record):
    if record["id"].startswith("fw_"):
        return "top-three-brand MIV sum"
    return record["id"]


def compare_metadata(left, right):
    differences = [field for field in ("topic", "unit", "period", "geography")
                   if left[field] != right[field]]
    if quantity(left) != quantity(right):
        differences.append("quantity definition")
    if representation(left)[0] != representation(right)[0]:
        differences.append("numeric representation")
    if differences:
        return "Comparison withheld: " + ", ".join(differences)
    return ("Metadata aligns for illustrative arithmetic; "
            "review underlying source methods before interpretation.")


def build():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    records = payload["records"]
    by_id = {r["id"]: r for r in records}
    derivations = []
    for record in records:
        representation(record)
        if "derivation" in record:
            calculated = arithmetic(record["derivation"])
            expected = Decimal(str(record["value"]))
            if abs(calculated - expected) > Decimal("0.000000001"):
                raise ValueError("Derivation mismatch: " + record["id"])
            derivations.append({"id": record["id"], "expression": record["derivation"],
                                "computed": str(calculated), "stored": str(expected),
                                "result": "Matches recorded value"})
    cases = [
        ("Paris versus London top-three brand MIV",
         "fw_paris_top3_total", "fw_london_top3_total"),
        ("Online apparel percentage versus age-gap percentage points",
         "eu_online_apparel_all", "eu_online_apparel_age_gap"),
        ("Textile consumption versus textile waste",
         "eu_textile_consumption", "eu_textile_waste"),
    ]
    comparisons = [{"name": name, "left": left, "right": right,
                    "result": compare_metadata(by_id[left], by_id[right])}
                   for name, left, right in cases]
    assert len(records) == 10
    assert len(derivations) == 5
    assert comparisons[1]["result"].startswith("Comparison withheld")
    assert comparisons[2]["result"].startswith("Comparison withheld")
    missing = [r["id"] for r in records if not r.get("caveat")]
    assert missing == ["eu_online_apparel_age_gap", "eu_textile_waste"]
    try:
        arithmetic("__import__('os').getcwd()")
    except ValueError:
        pass
    else:
        raise AssertionError("Non-numeric expression was accepted.")
    summary = {"records": len(records), "source_urls": len({r["source"] for r in records}),
               "derivations_verified": len(derivations), "missing_caveat_records": missing,
               "comparison_examples": comparisons,
               "source_snapshot": payload["published"],
               "original_analysis_only": True, "independent_fact_refresh": False}
    (HERE / "audit-results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    def table(headers, rows):
        return ("<div class='table-wrap'><table><thead><tr>"
                + "".join("<th>" + escape(h) + "</th>" for h in headers)
                + "</tr></thead><tbody>"
                + "".join("<tr>" + "".join("<td>" + cell + "</td>" for cell in row)
                          + "</tr>" for row in rows) + "</tbody></table></div>")
    audit_rows = []
    for r in records:
        kind, number = representation(r)
        audit_rows.append([
            escape(r["id"]), escape(number + " " + r["unit"]),
            escape(kind), escape(r["period"]), escape(r["geography"]),
            escape(r["entity"]),
            escape(r.get("caveat") or "Not supplied here; review the original source"),
            '<a href="' + escape(r["source"], quote=True) + '">Original source</a>'
        ])
    calculations = table(["Record", "Expression", "Computed", "Check"],
                         [[escape(d["id"]), escape(d["expression"]), escape(d["computed"]),
                           escape(d["result"])] for d in derivations])
    comparison_table = table(["Example", "Decision"],
                             [[escape(c["name"]), escape(c["result"])] for c in comparisons])
    data_table = table(["Record", "Value", "Representation", "Period", "Geography",
                        "Entity / denominator", "Caveat", "Source"], audit_rows)
    report = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Reproducible checks for fashion-statistic arithmetic, units, quantity definitions and source caveats.">
<title>Fashion Statistic Comparability Audit — Lunarness</title>
<style>
:root{color-scheme:light;--ink:#162333;--muted:#526173;--accent:#315476}
body{font:17px/1.65 system-ui,sans-serif;color:var(--ink);margin:0;background:#f5f7fa}
main{max-width:1160px;margin:auto;padding:40px 24px 60px}
header{border-top:5px solid var(--accent);padding:24px;background:white}
h1{font-size:clamp(2rem,4vw,3rem);line-height:1.15;margin:8px 0 18px}
h2{margin-top:42px}h3{margin-top:28px}a{color:#254e77;text-underline-offset:3px}
.eyebrow{color:var(--muted);font-size:.85rem;letter-spacing:.08em;text-transform:uppercase}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:22px 0}
.card{padding:18px;background:white;border:1px solid #dce3eb;border-radius:8px}
.card strong{display:block;font-size:1.9rem}.note{border-left:4px solid #cf983c;padding:12px 18px;background:#fff9ed}
.table-wrap{overflow:auto;border:1px solid #dce3eb;border-radius:8px;background:white}
table{border-collapse:collapse;width:100%;font-size:.9rem}
td,th{padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid #dce3eb}
th{background:#eaf0f6}pre{background:#102337;color:#e6eff7;padding:18px;overflow:auto;border-radius:8px}
footer{margin-top:40px;border-top:1px solid #ccd6e2;padding-top:18px;color:var(--muted)}
@media(max-width:650px){.cards{grid-template-columns:1fr}main{padding:20px 14px}header{padding:18px}}
</style></head><body><main><header><p class="eyebrow">Open methods · Lunarness · 2026</p>
<h1>Fashion Statistic Comparability Audit</h1>
<p>Reproduce arithmetic and inspect the units, quantity definitions, periods and caveats that determine what a fashion statistic means.</p>
<p>Input: the existing <a href="https://lunarness.com/pages/fashion-statistics-observatory">Lunarness Fashion Statistics Observatory</a> compilation,
published 27 August 2026. This is an audit of that recorded snapshot; underlying provider estimates have not been independently refreshed.</p></header>
<div class="cards"><div class="card"><strong>10</strong>recorded metrics</div><div class="card"><strong>5</strong>derivations reproduced</div><div class="card"><strong>9</strong>underlying source URLs</div></div>
<h2>What this audit checks</h2><ol>
<li>Recompute each supplied sum or difference using decimal arithmetic.</li>
<li>Keep point values, lower bounds and ranges visibly distinct.</li>
<li>Withhold example comparisons when units, quantity definitions, time or scope differ.</li>
<li>Identify missing caveats so a reader can return to the original provider.</li></ol>
<p class="note">Matching metadata establishes a starting point for reviewing comparability. Source coverage, sampling and measurement methods still require the provider's documentation.</p>
<h2>Recorded calculations</h2>"""
    report += calculations
    report += "<h2>Three comparison decisions</h2>" + comparison_table
    report += """<p>A percentage share and a percentage-point difference represent different quantities. Consumption and waste remain different flows even when both are expressed in kilograms per resident.</p>
<h2>Source and scope ledger</h2>""" + data_table
    report += """<h2>Two documentation gaps</h2><p>The age-gap and textile-waste records have no caveat field in this compilation. The ledger makes that absence visible; it does not infer the missing context.</p>
<h2>Reproduce the audit</h2><p>The code, input snapshot, notebook and machine-readable results accompany this report.</p>
<pre>python build_report.py</pre>
<p><a href="https://github.com/gokimedia/lunarness-fashion-data-observatory-2026/tree/codex/lunarness-resource-lab/resource-lab/audit">Audit source and recorded input</a></p>
<h2>Related source tools</h2><p><a href="https://lunarness.com/pages/fashion-statistics-observatory">Lunarness Fashion Statistics Observatory: definitions and original synthesis</a></p>
<footer>Original report text and analysis: Lunarness, 2026, <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Third-party facts retain their providers' rights and terms; cite the underlying sources. Publication is not an independent endorsement of the underlying estimates.</footer>
</main></body></html>"""
    (HERE / "index.html").write_text(report, encoding="utf-8")
    (HERE / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    code = "import json\nfrom pathlib import Path\nfrom build_report import build\nsummary = build()\nprint(json.dumps(summary, indent=2))"
    notebook = {"nbformat": 4, "nbformat_minor": 5,
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python",
                                            "name": "python3"},
                             "language_info": {"name": "python", "version": "3.12"}},
                "cells": [
                    {"id": "intro", "cell_type": "markdown", "metadata": {}, "source": [
                        "# Fashion Statistic Comparability Audit — Lunarness\n",
                        "Recorded snapshot: 2026-08-27. Original analysis CC BY 4.0; underlying provider rights retained.\n",
                        "Run with build_report.py and fashion_observatory_2026.json in the same folder.\n"]},
                    {"id": "audit", "cell_type": "code", "metadata": {}, "execution_count": 1,
                     "source": code.splitlines(keepends=True),
                     "outputs": [{"output_type": "stream", "name": "stdout",
                                  "text": [json.dumps(summary, indent=2) + "\n"]}]}]}
    (HERE / "audit.ipynb").write_text(json.dumps(notebook, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
