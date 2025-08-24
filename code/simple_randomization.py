import pandas as pd
import numpy as np
# Set seed for reproducibility
np.random.seed(42)
# Read DMA list
dmas = pd.read_csv("dma_list.csv")
# Simple random assignment without replacement to avoid duplicate groupings
dmas["arm"] = np.random.choice(["Treatment", "Control"],
                              size=len(dmas),
                              replace=False)
# Check and print group size balance
group_counts = dmas["arm"].value_counts()
print("Group assignment counts:\n", group_counts)
# Save assignments
dmas.to_csv("geoRCT_assignments.csv", index=False)

import pandas as pd
import numpy as np

# Set seed for reproducibility􀀄
np.random.seed(42)􀀄

# Read DMA list

dmas = pd.read_csv(“dma_list.csv”)􀀄
# Simple random assignment without replacement to avoid duplicate groupings􀀄
dmas[“arm”] = np.random.choice([“Treatment”, “Control”],􀀄

size=len(dmas),􀀄

replace=False)􀀄
# Check and print group size balance􀀄
group_counts = dmas[“arm”].value_counts()􀀄
print(“Group assignment counts:\n”, group_counts)􀀄
# Save assignments􀀄
dmas.to_csv(“geoRCT_assignments.csv”, index=False)􀀄