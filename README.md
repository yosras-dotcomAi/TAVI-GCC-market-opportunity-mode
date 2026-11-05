# 🫀 GCC TAVI Market Opportunity & Commercial Analytics Model

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tavi-gcc-market-opportunity-mode-lh4pkxnnzpkzmyhgne5epx.streamlit.app/)

A comprehensive end-to-end commercial analytics and market sizing framework tailored for Transcatheter Aortic Valve Implantation (TAVI) across the Gulf Cooperation Council (GCC) healthcare landscape, with a primary strategic focus on **Abbott’s Navitor™ System** and Saudi Arabia's **NUPCO** procurement framework.

---

## 🚀 Live Interactive Dashboard
Explore the live analytics platform, filters, and clinical performance models here:  
👉 **[GCC TAVI Market & Clinical Dashboard on Streamlit](https://tavi-gcc-market-opportunity-mode-lh4pkxnnzpkzmyhgne5epx.streamlit.app/)**

---

## 📊 Project Architecture & Key Features
1. **Market Sizing & Funnel Modeling:** Utilizes clinical meta-analysis benchmarks (severe AS prevalence, symptomatic rates, and untreated cohorts) to project addressable market volumes across KSA, UAE, Kuwait, Qatar, Oman, and Bahrain.
2. **Target Account Tiering:** Evaluates high-volume reference cardiac centers (Tier-1 hubs such as KSMC, KFMC, and NGHA) based on bed capacity, Heart Team status, and hybrid OR readiness.
3. **Clinical & Safety Analytics:** Compares device performance metrics, focusing on 30-day Paravalvular Leak (PVL) severity profiles and procedural success rates.
4. **Procurement Alignment:** Integrates NUPCO e-catalogue frameworks and regional tender channels to streamline market access and supply chain efficiency.

---

## 🛠️ Tech Stack & Repository Structure
* **Python (Pandas, NumPy, Plotly):** Automated data modeling, simulation, and chart generation.
* **Streamlit:** Interactive web application framework for executive data storytelling.
* **GitHub:** Version control, documentation, and continuous deployment.

```text
TAVI-GCC-market-opportunity-mode/
├── app.py                         # Interactive Streamlit Dashboard application
├── requirements.txt               # Required Python packages for deployment
├── README.md                      # Executive Project Documentation & Live Link
├── python/
│   └── tavi_market_model.py       # Market sizing logic & scenario forecasting
├── docs/
│   └── One_Page_Annual_Action_Plan.md # 2026 Strategic Commercial Action Plan
└── data/
    ├── GCC_TAVI_Granular_Cases_Model.csv # Simulated clinical & procedure dataset (13,490+ records)
    └── Target_Hospitals_Scoring.csv     # GCC reference hospital tiering matrix
