import pandas as pd
import numpy as np

# 1. Base Demographic Data (GCC Countries - Population 65+)
countries_data = {
    'Country': ['Saudi Arabia', 'UAE', 'Kuwait', 'Qatar', 'Oman', 'Bahrain'],
    'Pop_Over_65': [1600000, 250000, 210000, 85000, 180000, 75000]
}

df = pd.DataFrame(countries_data)

# 2. Clinical Parameters (Meta-analysis baseline benchmarks)
severe_as_rate = 0.034        # 3.4% severe aortic stenosis prevalence in elderly
symptomatic_rate = 0.756      # 75.6% symptomatic rate
untreated_surgical_rate = 0.405 # 40.5% unmanaged/untreated cohort

# 3. Funnel Calculations
df['Severe_AS_Patients'] = np.round(df['Pop_Over_65'] * severe_as_rate).astype(int)
df['Symptomatic_Patients'] = np.round(df['Severe_AS_Patients'] * symptomatic_rate).astype(int)
df['TAVI_Eligible_Pool'] = np.round(df['Symptomatic_Patients'] * untreated_surgical_rate).astype(int)

# 4. Scenario Modeling (Penetration Rates for Navitor & Competitors)
scenarios = {
    'Conservative': 0.15,
    'Base': 0.25,
    'Aggressive': 0.35
}

for scenario, rate in scenarios.items():
    df[f'TAVI_Volume_{scenario}'] = np.round(df['TAVI_Eligible_Pool'] * rate).astype(int)

# Display Output
print(df[['Country', 'TAVI_Eligible_Pool', 'TAVI_Volume_Conservative', 'TAVI_Volume_Base', 'TAVI_Volume_Aggressive']])

# Export to CSV for Power BI ingestion
df.to_csv('GCC_TAVI_Market_Model.csv', index=False)
