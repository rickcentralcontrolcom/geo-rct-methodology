import pandas as pd

import statsmodels.api as sm􀀄
import matplotlib.pyplot as plt􀀄
# Run leave-one-out regression by dropping one DMA at a time􀀄
loo_results = []􀀄
for excluded_dma in analysis_df[‘dma_code’].unique():

 temp_df = analysis_df[analysis_df[‘dma_code’] != excluded_dma]􀀄


 # Regress lift_index ~ assignment (Treatment vs Control)

 model_loo = sm.OLS(
temp_df[‘lift_index’],
sm.add_constant(pd.get_dummies(temp_df[‘assignment’], drop_􀀄

first=True))
).fit()
loo_results.append({
‘excluded_dma’: excluded_dma,
‘estimate’: model_loo.params[1], # treatment coefficient
‘pvalue’: model_loo.pvalues[1] # p-value for treatment effect
})
# Create dataframe of LOO estimates􀀄
loo_df = pd.DataFrame(loo_results)􀀄

# Plot LOO estimates to identify influential DMAs􀀄
plt.figure(figsize=(10, 6))􀀄
plt.scatter(loo_df[‘excluded_dma’], loo_df[‘estimate’], alpha=0.7)􀀄
plt.axhline(y=0.0342, color=’red’, linestyle=’--’, label=’Full-sample

estimate’)􀀄
plt.xlabel(‘Excluded DMA’)􀀄
plt.ylabel(‘Treatment Effect Estimate’)􀀄
plt.title(‘Leave-One-Out Sensitivity Analysis’)􀀄
plt.legend()􀀄
plt.tight_layout()􀀄
plt.show()􀀄
