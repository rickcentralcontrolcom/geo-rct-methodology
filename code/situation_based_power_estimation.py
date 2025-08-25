import pandas as pd
import numpy as np

from joblib import Parallel, delayed􀀄
from scipy.stats import ttest_ind􀀄
def run_power_simulation(historical_data, effect_sizes=[0.02, 0.03, 0.05],􀀄

test_weeks=[3, 4, 5, 6, 8], n_sims=1000,
alpha=0.05):
“””
Run power simulation for geographic RCT
“””
results = []
for effect in effect_sizes:
for weeks in test_weeks:􀀄

# Run simulations in parallel

sim_results = Parallel(n_jobs=-1)(􀀄
delayed(single_simulation)(􀀄


historical_data, effect, weeks, alpha􀀄
) for _ in range(n_sims)􀀄

)

power = np.mean(sim_results)􀀄

results.append({􀀄
‘effect_size’: effect,􀀄
‘test_weeks’: weeks,􀀄
‘power’: power􀀄

})

 return pd.DataFrame(results)􀀄

def single_simulation(historical_data, effect, weeks, alpha):
“””
Single simulation iteration
“””
# Sample random test window (ensure space for 8-week pre-period)
start_week = np.random.randint(8, len(historical_data) - weeks)
# Extract pre and test periods
pre_data = historical_data.iloc[start_week - 8:start_week].copy()
test_data = historical_data.iloc[start_week:start_week + weeks].copy()
# Random assignment of DMAs to treatment and control
dmas = historical_data[‘dma_code’].unique()
treatment_dmas = np.random.choice(dmas, len(dmas) // 2, replace=False)
pre_data[‘group’] = pre_data[‘dma_code’].apply(lambda x: ‘T’ if x in

treatment_dmas else ‘C’)
test_data[‘group’] = test_data[‘dma_code’].apply(lambda x: ‘T’ if x in

treatment_dmas else ‘C’)
# Aggregate weekly sales by DMA
pre_avg = pre_data.groupby(‘dma_code’)[‘sales_volume’].mean().reset_􀀄

index(name=’pre_avg’)
test_avg = test_data.groupby(‘dma_code’)[‘sales_volume’].mean().reset_􀀄

index(name=’test_avg’)
# Apply simulated lift to treatment group
test_avg[‘group’] = test_avg[‘dma_code’].apply(lambda x: ‘T’ if x in

treatment_dmas else ‘C’)
test_avg.loc[test_avg[‘group’] == ‘T’, ‘test_avg’] *= (1 + effect)􀀄


 # Merge for lift calculation
merged = pre_avg.merge(test_avg[[‘dma_code’, ‘test_avg’, ‘group’]],

on=’dma_code’)
# Compute lift index
merged[‘lift’] = (merged[‘test_avg’] / merged[‘pre_avg’]) -1
# Run t-test on lift between groups
t_vals = merged[merged[‘group’] == ‘T’][‘lift’]
c_vals = merged[merged[‘group’] == ‘C’][‘lift’]
t_stat, p_val = ttest_ind(t_vals, c_vals, equal_var=False)
return p_val < alpha􀀄

# Example usage􀀄
# historical_data = pd.read_csv(‘historical_sales_data.csv’)􀀄
# power_results = run_power_simulation(historical_data)􀀄
# print(power_results)􀀄
