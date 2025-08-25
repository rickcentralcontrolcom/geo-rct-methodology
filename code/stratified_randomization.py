import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler􀀄
from sklearn.cluster import KMeans􀀄
def stratified_randomization(dmas_df, strat_vars, n_strata=4, seed=42):

 “””
Stratified randomization for Geo RCT
“””
# Standardize stratification variables
scaler = StandardScaler()
X = scaler.fit_transform(dmas_df[strat_vars])
# Create strata using k-means clustering
kmeans = KMeans(n_clusters=n_strata, random_state=seed)
dmas_df[‘stratum’] = kmeans.fit_predict(X)
# Randomize within strata
np.random.seed(seed)
dmas_df[‘assignment’] = ‘Control’
for stratum in range(n_strata):

 stratum_indices = dmas_df[dmas_df[‘stratum’] == stratum].index
n_treat = len(stratum_indices) // 2􀀄


 treat_dmas = np.random.choice(stratum_indices, n_treat,􀀄
replace=False)
dmas_df.loc[treat_dmas, ‘assignment’] = ‘Treatment’
# Handle the leftover DMA if stratum size is odd
if len(stratum_indices) % 2 != 0:􀀄
remaining = list(set(stratum_indices) - set(treat_dmas))􀀄
assign_to = np.random.choice([‘Treatment’, ‘Control’])􀀄
dmas_df.loc[np.random.choice(remaining, 1), ‘assignment’] =
assign_to
return dmas_df􀀄
# Example usage􀀄
dmas = pd.read_csv(‘dma_data.csv’)􀀄
strat_vars = [‘pre_period_sales’, ‘population’, ‘median_income’]􀀄

assignments = stratified_randomization(dmas, strat_vars)􀀄
