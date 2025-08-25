import pandas as pd

import statsmodels.formula.api as smf􀀄
# Copy original data and create post-treatment indicator􀀄
did_df = df.copy()􀀄
did_df[‘post’] = (did_df[‘period’] == ‘test’).astype(int)􀀄
# Run Difference-in-Differences model with fixed effects and clustered SEs􀀄
did_model = smf.ols(

 formula=’weekly_sales ~ assignment * post + C(dma_code)’, # includes
DMA fixed effects
data=did_df􀀄
).fit(
cov_type=’cluster’,
cov_kwds={‘groups’: did_df[‘dma_code’]} # cluster SEs at DMA level􀀄

)

# Output the DiD interaction coefficient􀀄
interaction_term = ‘assignment[T.Treatment]:post’􀀄
if interaction_term in did_model.params:

 print(f”DiD estimate: {did_model.params[interaction_term]:.4f}”)􀀄

else:

 print(“Interaction term not found in model output. Check data
encoding.”)􀀄
