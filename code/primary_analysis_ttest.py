import pandas as pd
import numpy as np

from scipy import stats􀀄
import statsmodels.api as sm􀀄
from statsmodels.stats.anova import anova_lm􀀄
from statsmodels.stats.sandwich_covariance import cov_hc1􀀄
# Load DMA-level pre/post sales and assignment data􀀄
df = pd.read_csv(“geo_rct_results.csv”)􀀄
# Step 1: Calculate pre-period metrics (average + trend)􀀄
pre_period = df[df[‘period’] == ‘pre’].groupby(‘dma_code’).agg({􀀄


 ‘weekly_sales’: [
‘mean’,
lambda x: np.polyfit(range(len(x)), x, 1)[0] # slope of sales trend

 ]􀀄

}).reset_index()􀀄

pre_period.columns = [‘dma_code’, ‘pre_avg’, ‘pre_trend’]􀀄

# Step 2: Calculate average test-period sales􀀄

test_period = df[df[‘period’] == ‘test’].groupby(‘dma_code’).agg({
‘weekly_sales’: ‘mean’􀀄

}).reset_index()􀀄

test_period.columns = [‘dma_code’, ‘test_avg’]􀀄

# Step 3: Merge pre, test, and assignment groups􀀄

analysis_df = pre_period.merge(test_period, on=’dma_code’)􀀄

analysis_df = analysis_df.merge(
df[[‘dma_code’, ‘assignment’]].drop_duplicates(),
on=’dma_code’􀀄

)

# Step 4: Estimate expected sales using pre-period trend􀀄
# Assumes linear growth and 5 weeks of test period􀀄
analysis_df[‘expected_sales’] = analysis_df[‘pre_avg’] * (1 + analysis_􀀄

df[‘pre_trend’] * 5)􀀄
# Step 5: Calculate normalized lift index􀀄
analysis_df[‘lift_index’] = (analysis_df[‘test_avg’] / analysis_􀀄

df[‘expected_sales’]) - 1􀀄
# Step 6: Run OLS regression with treatment group as predictor􀀄
X = sm.add_constant(pd.get_dummies(analysis_df[‘assignment’], drop_􀀄

first=True)) # e.g., Control=0, Treatment=1􀀄
y = analysis_df[‘lift_index’]􀀄
model = sm.OLS(y, X).fit()􀀄
print(model.summary())􀀄
# Step 7: Report robust (HC1) standard errors􀀄
robust_cov = cov_hc1(model)􀀄
robust_se = np.sqrt(np.diag(robust_cov))􀀄
print(f”Robust standard error for treatment effect: {robust_se[1]:.4f}”)􀀄
