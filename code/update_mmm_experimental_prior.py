# Example: Updating MMM with experimental prior􀀄
# Prior from experiment: 3.4% ± 1.5%􀀄
prior_mean = 0.034􀀄
prior_sd = 0.015􀀄


# Combine with MMM posterior using inverse variance weighting􀀄
mmm_estimate = 0.028􀀄
mmm_se = 0.022􀀄
pooled_estimate = (

 (prior_mean / prior_sd**2 + mmm_estimate / mmm_se**2) /
(1 / prior_sd**2 + 1 / mmm_se**2)􀀄

)

pooled_se = np.sqrt(1 / (1 / prior_sd**2 + 1 / mmm_se**2))􀀄
print(f"Updated coefficient: {pooled_estimate:.3f}")􀀄
print(f"Updated standard error: {pooled_se:.3f}")􀀄

