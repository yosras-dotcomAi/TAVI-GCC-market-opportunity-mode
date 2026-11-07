"""
GCC TAVI Market Opportunity Model (independent, public-data project)

Single-file Streamlit app. Every sourced input is embedded below with its source,
and every assumption is a visible slider. No patient-level or company-internal data.
"""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="GCC TAVI Market Opportunity Model", page_icon="🫀", layout="wide")

# ----------------------------------------------------------------------------
# SOURCED INPUTS
# ----------------------------------------------------------------------------
# Residents aged 75+ in 2026: UN World Population Prospects 2024, medium variant
# (as tabulated by populationpyramids.org country pages).
POP75 = {
    "Saudi Arabia": 341_543,
    "United Arab Emirates": 57_298,
    "Oman": 53_980,
    "Kuwait": 40_750,
    "Bahrain": 19_506,
    "Qatar": 11_809,
}
TOTAL_POP = {
    "Saudi Arabia": 35_165_787,
    "United Arab Emirates": 11_574_683,
    "Oman": 5_671_458,
    "Kuwait": 5_102_773,
    "Bahrain": 1_675_572,
    "Qatar": 3_173_560,
}
# Osnabrugge et al., J Am Coll Cardiol 2013;62(11):1002-12 -> (base, low, high)
PREV = {"Base": 0.034, "Low": 0.011, "High": 0.057}          # severe AS prevalence, age 75+
SYMP = {"Base": 0.756, "Low": 0.658, "High": 0.854}          # share symptomatic
NOTSURG = {"Base": 0.405, "Low": 0.358, "High": 0.451}       # share not treated surgically
ANNUAL_RATE = 0.092   # derived: (17,712 + 9,189) / (189,836 + 102,558) from the same paper

# Saudi cost inputs, Al-Omar et al., Front Cardiovasc Med 2026 (doi 10.3389/fcvm.2026.1937664).
# Study was commissioned by Edwards Lifesciences; the valve price is NUPCO's 2025 price for SAPIEN 3.
VALVE_SAR_REF = 127_761
PROC_SAR_REF = 30_667
SAR_PER_USD = 3.75

# Gulf TAVR Registry: 795 patients, 8 centres in KSA/Kuwait/Bahrain/Oman, 1 Jan 2017 - 31 Dec 2019.
REGISTRY_PATIENTS = 795
REGISTRY_YEARS = 3
REGISTRY_COUNTRIES = ["Saudi Arabia", "Kuwait", "Bahrain", "Oman"]

SCENARIOS = {
    "A - Conservative": "Symptomatic severe AS not treated surgically (high-risk / inoperable proxy)",
    "B - Expanded": "A plus a share of surgically treated patients shifting to TAVI (lower-risk indications)",
    "C - Full 75+ (ceiling)": "All symptomatic severe AS aged 75+ (guideline ceiling, not a forecast)",
}


def pools(pop, bound, shift):
    severe = pop * PREV[bound]
    symptomatic = severe * SYMP[bound]
    a = symptomatic * NOTSURG[bound]
    b = a + symptomatic * (1 - NOTSURG[bound]) * shift
    c = symptomatic
    return severe, symptomatic, {"A - Conservative": a, "B - Expanded": b, "C - Full 75+ (ceiling)": c}


# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.title("🫀 GCC TAVI Market Opportunity Model")
st.caption("Independent project built only from public data. Not affiliated with or endorsed by any manufacturer or employer.")
st.info(
    "How to read this: epidemiology and population figures are **sourced** (see the Sources tab). "
    "Volumes, prices, shares and margins in the sidebar are **what-if assumptions you control**, "
    "not observed data. The model is a demographic floor, not a market forecast."
)

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
st.sidebar.title("Controls")
countries = st.sidebar.multiselect("Countries", list(POP75), default=list(POP75))
scenario = st.sidebar.selectbox("Patient-pool scenario", list(SCENARIOS), index=1)
st.sidebar.caption(SCENARIOS[scenario])
bound = st.sidebar.radio("Epidemiology bound", ["Low", "Base", "High"], index=1, horizontal=True)
shift = st.sidebar.slider("Scenario B: share of surgical patients shifting to TAVI", 0.0, 1.0, 0.5, 0.05)

st.sidebar.markdown("### What-if: volumes")
penetration = st.sidebar.slider("Share of annual eligible candidates treated", 0.05, 1.0, 0.50, 0.05)
mfr_share = st.sidebar.slider("Your what-if share of treated patients", 0.01, 0.50, 0.15, 0.01)

st.sidebar.markdown("### What-if: cost and profit")
valve_price = st.sidebar.number_input("Valve net price per unit (SAR)", 20_000, 300_000, VALVE_SAR_REF, 1_000)
proc_cost = st.sidebar.number_input("Hospital procedure cost per case (SAR)", 5_000, 150_000, PROC_SAR_REF, 1_000)
gross_margin = st.sidebar.slider("Gross margin on valve revenue (illustrative)", 0.30, 0.90, 0.65, 0.01)
opex_pct = st.sidebar.slider("Commercial and support cost, % of revenue (illustrative)", 0.05, 0.50, 0.25, 0.01)
st.sidebar.caption(
    "Default valve and procedure prices are Saudi figures from a published study (SAPIEN 3, NUPCO 2025). "
    "They are a category reference, not any specific product's price. Margins are illustrative: "
    "no company's internal margin is public here."
)

if not countries:
    st.warning("Select at least one country in the sidebar.")
    st.stop()

# ----------------------------------------------------------------------------
# MODEL
# ----------------------------------------------------------------------------
rows = []
for c in POP75:
    sev, sym, pool_base = pools(POP75[c], bound, shift)
    _, _, pool_low = pools(POP75[c], "Low", shift)
    _, _, pool_high = pools(POP75[c], "High", shift)
    pool = pool_base[scenario]
    annual = pool * ANNUAL_RATE
    procs = annual * penetration
    mfr_procs = procs * mfr_share
    payer_value = procs * (valve_price + proc_cost)          # SAR
    revenue = mfr_procs * valve_price                         # SAR
    gross = revenue * gross_margin
    opex = revenue * opex_pct
    rows.append({
        "Country": c, "Population 75+": POP75[c], "Severe AS": sev, "Symptomatic severe AS": sym,
        "Eligible pool": pool, "Pool (low)": pool_low[scenario], "Pool (high)": pool_high[scenario],
        "Annual new candidates": annual, "Procedures / year": procs, "Your procedures / year": mfr_procs,
        "Market value (SAR)": payer_value, "Your revenue (SAR)": revenue,
        "Gross profit (SAR)": gross, "Commercial cost (SAR)": opex, "Operating profit (SAR)": gross - opex,
    })
full = pd.DataFrame(rows)
df = full[full["Country"].isin(countries)].copy()
tot = df.drop(columns="Country").sum()


def usd_m(sar):
    return sar / SAR_PER_USD / 1e6


k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Eligible pool (stock)", f"{tot['Eligible pool']:,.0f}")
k2.metric("New candidates / year", f"{tot['Annual new candidates']:,.0f}")
k3.metric("Procedures / year (what-if)", f"{tot['Procedures / year']:,.0f}")
k4.metric("Market value / year", f"${usd_m(tot['Market value (SAR)']):,.1f}M")
k5.metric("Your revenue / year", f"${usd_m(tot['Your revenue (SAR)']):,.2f}M")
k6.metric("Operating profit / year", f"${usd_m(tot['Operating profit (SAR)']):,.2f}M")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Market funnel", "💰 Procedures, cost and profit", "🔎 Reality check and evidence", "📚 Sources and method"]
)

# ----------------------------- TAB 1 ----------------------------------------
with tab1:
    left, right = st.columns([1, 1])
    with left:
        st.subheader("Patient funnel (selected countries)")
        stages = ["Residents aged 75+", "Severe aortic stenosis", "Symptomatic severe AS", f"Eligible pool: scenario {scenario[0]}"]
        values = [tot["Population 75+"], tot["Severe AS"], tot["Symptomatic severe AS"], tot["Eligible pool"]]
        fig = go.Figure(go.Funnel(y=stages, x=values, textinfo="value+percent initial"))
        fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig)
    with right:
        st.subheader("Where the older population sits")
        share_df = df[["Country", "Population 75+"]].copy()
        share_df["Share of selected"] = share_df["Population 75+"] / share_df["Population 75+"].sum()
        fig = px.bar(share_df.sort_values("Population 75+"), x="Population 75+", y="Country", orientation="h",
                     text=share_df.sort_values("Population 75+")["Share of selected"].map("{:.0%}".format))
        fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig)

    st.subheader("Eligible pool with published uncertainty range")
    err = df.sort_values("Eligible pool", ascending=False)
    fig = go.Figure(go.Bar(
        x=err["Country"], y=err["Eligible pool"],
        error_y=dict(type="data", symmetric=False,
                     array=err["Pool (high)"] - err["Eligible pool"],
                     arrayminus=err["Eligible pool"] - err["Pool (low)"]),
    ))
    fig.update_layout(height=360, yaxis_title="Patients", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig)
    st.caption("Whiskers use the published low and high bounds of the epidemiology inputs together, so the range is deliberately wide.")

# ----------------------------- TAB 2 ----------------------------------------
with tab2:
    st.subheader("Procedures, market value and profit by country (what-if)")
    show = df[["Country", "Annual new candidates", "Procedures / year", "Your procedures / year"]].copy()
    show["Market value (USD M)"] = df["Market value (SAR)"].map(usd_m)
    show["Your revenue (USD M)"] = df["Your revenue (SAR)"].map(usd_m)
    show["Operating profit (USD M)"] = df["Operating profit (SAR)"].map(usd_m)
    st.dataframe(
        show.sort_values("Procedures / year", ascending=False).style.format({
            "Annual new candidates": "{:,.0f}", "Procedures / year": "{:,.0f}", "Your procedures / year": "{:,.1f}",
            "Market value (USD M)": "{:,.1f}", "Your revenue (USD M)": "{:,.2f}", "Operating profit (USD M)": "{:,.2f}",
        }),
        hide_index=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df.sort_values("Procedures / year", ascending=False), x="Country", y="Procedures / year",
                     title="Procedures per year (what-if)")
        fig.update_layout(height=340, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig)
    with c2:
        rev, gp, ox = tot["Your revenue (SAR)"], tot["Gross profit (SAR)"], tot["Commercial cost (SAR)"]
        wf = go.Figure(go.Waterfall(
            x=["Revenue", "Cost of goods", "Gross profit", "Commercial cost", "Operating profit"],
            measure=["absolute", "relative", "total", "relative", "total"],
            y=[usd_m(rev), -usd_m(rev - gp), 0, -usd_m(ox), 0],
            text=[f"{usd_m(rev):.2f}", f"{-usd_m(rev - gp):.2f}", "", f"{-usd_m(ox):.2f}", ""],
        ))
        wf.update_layout(title="From revenue to operating profit (USD M, what-if)", height=340,
                         margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
        st.plotly_chart(wf)

    st.subheader("Sensitivity: operating profit (USD M) across penetration and share")
    pens = [0.10, 0.25, 0.50, 0.75, 1.00]
    shares = [0.05, 0.10, 0.15, 0.20, 0.30]
    annual_total = tot["Annual new candidates"]
    grid = pd.DataFrame(
        [[usd_m(annual_total * p * s * valve_price * (gross_margin - opex_pct)) for s in shares] for p in pens],
        index=[f"{int(p*100)}% treated" for p in pens], columns=[f"{int(s*100)}% share" for s in shares],
    )
    fig = px.imshow(grid, text_auto=".2f", aspect="auto", color_continuous_scale="Blues")
    fig.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig)
    st.caption(
        "Every cell is a what-if, not a forecast. The valve price default is a published Saudi reference price for a "
        "different manufacturer's valve; replace it with your own assumption. Operating profit = revenue x (gross margin - commercial cost %)."
    )

# ----------------------------- TAB 3 ----------------------------------------
with tab3:
    st.subheader("Reality check against published Gulf registry activity")
    reg_per_year = REGISTRY_PATIENTS / REGISTRY_YEARS
    ck = []
    for sc in SCENARIOS:
        flow = 0
        for c in REGISTRY_COUNTRIES:
            _, _, p = pools(POP75[c], "Base", shift)
            flow += p[sc] * ANNUAL_RATE
        ck.append({"Scenario": sc, "Modeled annual candidates (KSA, Kuwait, Bahrain, Oman)": round(flow),
                   "Registry procedures / year (2017-2019, 8 centres)": round(reg_per_year),
                   "Registry as % of model": reg_per_year / flow})
    ckdf = pd.DataFrame(ck)
    st.dataframe(ckdf.style.format({"Registry as % of model": "{:.0%}"}), hide_index=True)
    st.warning(
        "Eight high-volume centres alone recorded a large fraction of the conservative estimate in 2017-2019, so real "
        "activity is likely well above what this demographic model implies. Reasons: it counts only residents aged 75+, "
        "uses prevalence from Western populations, and approximates the annual flow. Treat the volume outputs as a floor "
        "until the model is calibrated against observed center-level activity."
    )

    st.subheader("Published evidence points used in this project")
    st.markdown(
        """
- **Regional evidence is thin.** The Gulf TAVR Registry covers eight high-volume centres in Saudi Arabia, Kuwait, Bahrain and Oman (2017-2019); Qatar's registry covers 241 patients at one hospital (2012-2023); a Jeddah series covers 52 patients.
- **Navitor CE mark.** Abbott announced an expanded CE mark in August 2025 extending the Navitor indication to low and intermediate surgical risk in Europe. Sources found describe the US indication as high or extreme risk only; verify current status before quoting.
- **Navitor trial data.** Abbott's announcement cites the VANTAGE study (technical success of about 97%, no moderate-or-worse paravalvular leak at 30 days). This dashboard makes no device-to-device performance comparison.
- **Saudi cost anchors.** A 2026 peer-reviewed Saudi cost-effectiveness study reports a TAVI valve cost of SAR 127,761 (NUPCO 2025 price for SAPIEN 3) and an intervention cost of SAR 30,667. The study was commissioned by Edwards Lifesciences, so treat it as one transparent data point, not a market price list.
        """
    )

# ----------------------------- TAB 4 ----------------------------------------
with tab4:
    st.subheader("Method")
    st.markdown(
        """
1. Residents aged 75+ per country (UN WPP 2024, medium variant, 2026).
2. x severe aortic stenosis prevalence in 75+ (3.4%; 1.1% to 5.7%).
3. x share symptomatic (75.6%; 65.8% to 85.4%).
4. Scenario A: x share not treated surgically (40.5%; 35.8% to 45.1%). Scenario B adds a chosen share of the rest. Scenario C keeps all symptomatic patients.
5. Annual new candidates = pool x 9.2%, a ratio derived from the same meta-analysis (approximation).
6. Procedures = annual candidates x the penetration you choose. Revenue, cost and profit use only the prices and margins you set.
        """
    )
    st.subheader("Sources")
    st.markdown(
        """
- United Nations, *World Population Prospects 2024*, medium variant (2026 projection), via populationpyramids.org country pages.
- Osnabrugge RL et al. Aortic stenosis in the elderly: disease prevalence and number of candidates for TAVR. *J Am Coll Cardiol* 2013;62(11):1002-12.
- Gulf TAVR Registry (one-year outcomes), 795 patients, eight centres, 2017-2019; QATAVI registry, *Int J Cardiol* 2025; Albugami et al., *Cureus* 2021 (Jeddah).
- Al-Omar HA et al. Cost-effectiveness of TAVI for asymptomatic severe AS in Saudi Arabia. *Front Cardiovasc Med* 2026, doi 10.3389/fcvm.2026.1937664 (funded by Edwards Lifesciences).
- Abbott press materials on the Navitor expanded CE mark (August 2025), as reported by trade media.
        """
    )
    st.subheader("Known limitations")
    st.markdown(
        """
- Western epidemiology applied to Gulf residents; age cut-off at 75 excludes younger patients.
- Population counts include large expatriate working-age groups, so elderly counts are small relative to total population.
- Non-Saudi countries use the Saudi price references unless you change them.
- No reimbursement, tender, center-capacity or competitor effects are modeled.
- Margins are illustrative; no company-internal data is used anywhere in this project.
        """
    )
