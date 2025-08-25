# Verify completeness􀀄
coverage = weekly_data.groupby('dma_code').size()􀀄
print(f"DMAs with full data: {(coverage == expected_weeks).sum()} / 210")􀀄
# Check for anomalies􀀄
import matplotlib.pyplot as plt􀀄
weekly_data.groupby('dma_code')['sales_amount'].plot(figsize=(12, 8))􀀄
plt.title('Sales by DMA Over Time')􀀄
plt.show()􀀄
# Test for skewness􀀄
from scipy import stats􀀄


skew = stats.skew(weekly_data['sales_amount'])􀀄

if abs(skew) > 1:
print("Consider log or square-root transformation")
weekly_data['log_sales'] = np.log(weekly_data['sales_amount'] + 1)􀀄

# If using sales volume (continuous), check distribution of normalized
values.􀀄
# Normalize by population or baseline to remove DMA size effects􀀄

# Example: sales per capita or index to baseline period􀀄
weekly_data['sales_per_capita'] = weekly_data['sales_amount'] / weekly_􀀄
data['population']􀀄

# Or normalize to baseline period (e.g., pre-treatment mean)􀀄

baseline_means = weekly_data[weekly_data['week'] < treatment_start].􀀄
groupby('dma')['sales_amount'].mean()􀀄
weekly_data['sales_index'] = weekly_data.apply(lambda x: x['sales_amount'] /

baseline_means[x['dma']], axis=1)􀀄
# Test normalized values for approximate normality􀀄
skew = stats.skew(weekly_data['sales_per_capita'])􀀄
if abs(skew) > 1:

 print(f"Normalized sales skewness: {skew:.2f}")
print("Consider additional transformations if needed for model
assumptions")􀀄
