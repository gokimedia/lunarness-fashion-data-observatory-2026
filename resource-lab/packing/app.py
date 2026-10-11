import io
import csv
import pandas as pd
import streamlit as st
from solver import solve_cover, DEMO_LOOKS, DEMO_ASSETS

st.set_page_config(page_title="Shoot Packing Set-Cover Planner — Lunarness",
                   page_icon="🧳", layout="centered")
st.title("Shoot Packing Set-Cover Planner")
st.caption("An original open tool by Lunarness")
st.write("Plan the smallest set of distinct accessories covering sequential shoot looks, "
         "using coverage you declare. Each selected accessory may be reused between looks.")
st.info("The starting labels are fictional. Use non-sensitive labels: this hosted "
        "Streamlit app processes inputs on its server. The app code does not save "
        "entered plans to files or a database.")

with st.form("packing_inputs"):
    look_text = st.text_input("Look IDs, separated by commas", value=", ".join(DEMO_LOOKS))
    st.write("Edit the coverage table. Put comma-separated look IDs in “Covers looks”.")
    frame = pd.DataFrame([{"Asset ID": a["id"], "Asset label": a["name"],
                           "Covers looks": a["covers"]} for a in DEMO_ASSETS])
    edited = st.data_editor(frame, num_rows="dynamic", hide_index=True,
                           use_container_width=True, key="coverage_editor",
                           column_config={
                               "Asset ID": st.column_config.TextColumn(required=True),
                               "Asset label": st.column_config.TextColumn(required=True),
                               "Covers looks": st.column_config.TextColumn(required=True),
                           })
    submitted = st.form_submit_button("Find the smallest packing set", type="primary")

if submitted:
    looks = [x.strip() for x in look_text.split(",")]
    rows = [{"id": str(r["Asset ID"]), "name": str(r["Asset label"]),
             "covers": str(r["Covers looks"])}
            for _, r in edited.fillna("").iterrows()
            if any(str(v).strip() for v in r)]
    try:
        result = solve_cover(looks, rows)
    except ValueError as exc:
        st.error(str(exc))
    else:
        if result["status"] == "uncovered":
            st.warning("No complete plan exists with this declared coverage. "
                       "Uncovered looks: " + ", ".join(result["missing"]))
        else:
            st.metric("Minimum distinct accessory types", result["minimum"])
            st.success("Selected: " + ", ".join(a["id"] for a in result["selected"]))
            st.dataframe(pd.DataFrame(result["selected"]), hide_index=True,
                         use_container_width=True)
            st.subheader("One assignment across sequential looks")
            assignment = [{"Look": look, "Selected asset": key}
                          for look, key in result["assignment"].items()]
            st.table(assignment)
            if len(result["alternatives"]) > 1:
                st.write("Other equally small sets found (up to eight):")
                st.write(result["alternatives"])
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=["Look", "Selected asset"])
            writer.writeheader()
            writer.writerows(assignment)
            st.download_button("Download this assignment as CSV", buffer.getvalue(),
                               file_name="sequential-look-packing-plan.csv",
                               mime="text/csv")

with st.expander("How the plan is calculated"):
    st.write("The solver checks combinations in increasing order of size and stops "
             "at the first feasible size. This establishes a minimum for the "
             "coverage supplied, up to 12 looks and 18 assets.")
    st.write("The demo is intentionally a case where choosing the broadest accessory "
             "first is inefficient: B and C together cover all six looks.")
    st.write("Coverage is a user declaration. Verify quantity, schedule, included "
             "pieces and documented product measurements in the separate shoot brief.")
st.subheader("Measurement references")
st.link_button("Lunarness size guide", "https://lunarness.com/pages/size-guide")
st.link_button("Lunarness harness size calculator",
               "https://lunarness.com/pages/harness-size-calculator")
st.caption("Original solver and fictional examples: Lunarness, 2026. MIT license.")
