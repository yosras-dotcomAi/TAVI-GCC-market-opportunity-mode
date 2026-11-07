# GCC TAVI Market Opportunity Model

An interactive what-if model that sizes the transcatheter aortic valve implantation (TAVI) opportunity across the six Gulf Cooperation Council countries: Saudi Arabia, UAE, Oman, Kuwait, Bahrain and Qatar.

> **Independent project built only from public data. Not affiliated with or endorsed by any manufacturer or employer.**

| | |
|---|---|
| **Live dashboard** | [Open the Streamlit app](https://tavi-gcc-market-opportunity-mode-iy7nxbmcjkkcg6eudp7aud.streamlit.app/) |
| **Project slides** | [View the presentation]([GCC_TAVI_Opportunity_Model_Slides.pptx](https://github.com/user-attachments/files/34524061/GCC_TAVI_Opportunity_Model_Slides.pptx)
 |

---

## The question

How large is the TAVI opportunity in the Gulf, where is it concentrated, and how sensitive is it to the assumptions that drive it?

## How to read this model

- **Sourced inputs:** population aged 75+ and aortic stenosis epidemiology come from published sources, with low, base and high bounds.
- **What-if inputs:** procedure volumes, prices, market shares and margins are assumptions you control in the sidebar. They are not observed data.
- **A floor, not a forecast:** the model is a demographic floor. It frames the size of the opportunity and does not predict sales.

## What the dashboard shows

The dashboard has four tabs:

1. **Market funnel:** from residents aged 75+ to severe aortic stenosis, symptomatic patients and the eligible pool, plus where the older population sits by country, with a published uncertainty range.
2. **Procedures, cost and profit:** annual candidates, procedures, market value, modeled revenue and operating profit by country, a revenue-to-profit waterfall, and a sensitivity grid across penetration and market share.
3. **Reality check and evidence:** the model compared with published Gulf registry activity.
4. **Sources and method:** the evidence points and assumptions used.

**Controls:** country selection, patient-pool scenario (A Conservative, B Expanded, C Full 75+ ceiling), epidemiology bound (low, base, high), the share of surgically treated patients shifting to TAVI, and what-if volume, price and margin inputs.

## Headline results

Scenario B (Expanded), base epidemiology, all six countries:

| Metric | Value |
|---|---|
| Eligible pool (stock) | 9,478 |
| New candidates per year | 872 |
| Procedures per year (what-if) | 436 |
| Market value per year | $18.4M |
| Modeled revenue per year | $2.23M |
| Operating profit per year | $0.89M |

Saudi Arabia accounts for about 65% of the 75+ population in the region and roughly two thirds of every output metric.

## Reality check

The model's candidate volumes were compared with the Gulf TAVR Registry (8 centres in Saudi Arabia, Kuwait, Bahrain and Oman, 2017-2019, 265 procedures per year).

| Scenario | Modeled annual candidates | Registry as % of model |
|---|---|---|
| A - Conservative | 437 | 61% |
| B - Expanded | 757 | 35% |
| C - Full 75+ (ceiling) | 1,078 | 25% |

Eight centres alone recorded a large fraction of the conservative estimate, so real activity is likely well above what a demographic model implies. Volume outputs should be treated as a floor until calibrated against centre-level data.

## Limitations

- Regional evidence is thin: one multi-centre registry, one Qatar registry and one Jeddah series.
- The model counts only residents aged 75+ and uses prevalence from Western populations.
- Prices and margins are what-if inputs. The Saudi cost-effectiveness study used as a price anchor was commissioned by a manufacturer, so it is treated as one transparent data point, not a market price list.
- No device-to-device performance comparison is made.

## Next steps

- Calibrate volumes against centre-level activity.
- Add adjustments for local disease prevalence.
- Test pricing and share scenarios against real market feedback.

## Run it locally

```bash
git clone <your-repo-url>
cd <your-repo-folder>
pip install -r requirements.txt
streamlit run app.py
```

## Author

**Yosra**, Cath Lab Head Nurse moving into healthcare data analytics.
GitHub: [yosras-dotcomAi](https://github.com/yosras-dotcomAi)
