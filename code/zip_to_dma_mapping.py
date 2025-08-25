# Load ZIP to DMA mapping file􀀄
zip_dma_map = pd.read_csv(‘zip_dma_mapping.csv’)􀀄

# Map ZIP codes to DMA codes

transactions = transactions.merge(
zip_dma_map[[‘zip’, ‘dma_code’]],
left_on=’customer_zip’,
right_on=’zip’,
how=’left’􀀄

)

# Convert transaction_date to datetime if needed􀀄

transactions[‘transaction_date’] = pd.to_datetime(transactions􀀄
[‘transaction_date’])􀀄
# Aggregate transactions to DMA-week level􀀄
weekly_data = transactions.groupby(

 [‘dma_code’, pd.Grouper(key=’transaction_date’, freq=’W’)]􀀄

).agg({
‘sales_amount’: ‘sum’, # Sum of sales for volume
‘trans_count’: ‘sum’ # Sum of transactions for counts􀀄
}).reset_index()􀀄
