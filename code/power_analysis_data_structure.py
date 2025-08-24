# Example 2: Power Analysis Data Structure
import pandas as pd

# Required data format for power analysis
historical_data = pd.DataFrame({
    'dma_code': [501, 501, 501, 502, 502, 502],        # DMA identifier
    'week_ending': ['2023-01-07', '2023-01-14', '2023-01-21', 
                   '2023-01-07', '2023-01-14', '2023-01-21'],  # Date column
    'sales_volume': [125000, 132000, 128000, 
                    98000, 105000, 101000],              # Primary outcome metric
    'transaction_count': [450, 475, 465, 
                         380, 395, 385],                # Alternative outcome
    'store_count': [12, 12, 12, 8, 8, 8]               # Optional covariate
})

# Data structure requirements:
# - dma_code: Unique identifier for each DMA
# - week_ending: Date column in YYYY-MM-DD format
# - sales_volume: Primary outcome variable (numeric)
# - transaction_count: Secondary outcome variable (numeric) 
# - store_count: Optional covariate for analysis (numeric)
