import pandas as pd
import numpy as np

import statsmodels.api as sm􀀄
# Create fake pre/test periods using pre-period weeks􀀄
placebo_df = df[df[‘period’] == ‘pre’].copy()􀀄
placebo_df[‘fake_period’] = np.where(

 placebo_df[‘week_number’] >= 5, ‘fake_test’, ‘fake_pre’􀀄


)

# Group by DMA and fake period to get average sales􀀄

placebo_summary = placebo_df.groupby([‘dma_code’, ‘fake_period’])[‘weekly_􀀄
sales’].mean().reset_index()􀀄
# Pivot to wide format􀀄
placebo_pivot = placebo_summary.pivot(

 index=’dma_code’,
columns=’fake_period’,
values=’weekly_sales’􀀄

).reset_index()􀀄
# Add treatment/control assignment􀀄
placebo_pivot = placebo_pivot.merge(

 df[[‘dma_code’, ‘assignment’]].drop_duplicates(),
on=’dma_code’􀀄

)

# Compute placebo lift (should be ~0 if pre-periods are balanced)􀀄

placebo_pivot[‘fake_lift’] = (placebo_pivot[‘fake_test’] / placebo_􀀄
pivot[‘fake_pre’]) - 1􀀄
# Run placebo regression􀀄
placebo_model = sm.OLS(

 placebo_pivot[‘fake_lift’],

 sm.add_constant(pd.get_dummies(placebo_pivot[‘assignment’], drop_􀀄
first=True))􀀄
).fit()􀀄

# Report placebo results

print(f”Placebo effect: {placebo_model.params[1]:.4f}”)􀀄
print(f”Placebo p-value: {placebo_model.pvalues[1]:.4f}”)􀀄
