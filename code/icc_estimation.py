import pandas as pd

import numpy as np

from scipy.stats import ttest_ind􀀄

from statsmodels.regression.mixed_linear_model import MixedLM􀀄

# Simulate DMA-level sales data with a target ICC􀀄

def simulate_dma_sales(n_dmas=210, n_weeks=6, icc=0.15, mean_sales=1000,􀀄

sd_sales=300, seed=42):

 np.random.seed(seed)

 # Calculate between and within cluster variance

 var_total = sd_sales ** 2

 var_between = icc * var_total

 var_within = var_total - var_between

 # Generate random intercepts for each DMA

 dma_effects = np.random.normal(0, np.sqrt(var_between), size=n_dmas)

 # Simulate weekly sales per DMA

 data = []
for dma in range(n_dmas):
for week in range(n_weeks):􀀄
y = mean_sales + dma_effects[dma] + np.random.normal(0,
np.sqrt(var_within))􀀄
data.append({‘dma’: dma, ‘week’: week, ‘sales’: y})
return pd.DataFrame(data)􀀄

# Estimate ICC using mixed-effects model (robust to imbalance)􀀄

def estimate_icc(df):

 model = MixedLM.from_formula(‘sales ~ 1’, groups=’dma’, data=df)

 result = model.fit()

 var_between = result.cov_re.iloc[0, 0] # Random intercept variance

 var_within = result.scale􀀄# Residual (within-group)

variance


 icc = var_between / (var_between + var_within)

 return icc

# Compare power at different durations given ICC􀀄

def simulate_power(n_weeks_list=[4, 6], icc=0.15, lift=0.05, n_sim=100):
results = []
for weeks in n_weeks_list:

 significant = 0

 for _ in range(n_sim):􀀄
df = simulate_dma_sales(n_weeks=weeks, icc=icc)􀀄
treated = np.random.choice(df[‘dma’].unique(), size=105,

replace=False)􀀄
df[‘group’] = df[‘dma’].apply(lambda x: ‘T’ if x in treated else
‘C’)􀀄

# Apply lift to final week in treatment group􀀄

df.loc[(df[‘group’] == ‘T’) & (df[‘week’] == weeks - 1),
‘sales’] *= (1 + lift)􀀄

# Difference-in-differences by DMA􀀄
pre = df[df[‘week’] < weeks - 1].groupby(‘dma’)[‘sales’].mean()􀀄
post = df[df[‘week’] == weeks - 1].groupby(‘dma’)[‘sales’].􀀄

mean()

did = (post - pre).reset_index().merge(df[[‘dma’, ‘group’]].􀀄
drop_duplicates(), on=’dma’)􀀄

t, p = ttest_ind(did[did[‘group’] == ‘T’][‘sales’],􀀄
did[did[‘group’] == ‘C’][‘sales’],􀀄
equal_var=False)􀀄

if p < 0.05:􀀄

significant += 1
power = significant / n_sim
results.append({‘weeks’: weeks, ‘power’: power})

 return pd.DataFrame(results)􀀄


# Example usage􀀄
df = simulate_dma_sales(icc=0.18)􀀄
print(f”Estimated ICC: {estimate_icc(df):.3f}”)􀀄

power_df = simulate_power(n_weeks_list=[4, 6, 8], icc=0.18)􀀄
print(power_df)􀀄