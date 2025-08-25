import pandas as pd

from sqlalchemy import create_engine􀀄

# Create database connection (replace with actual credentials)􀀄
engine = create_engine(‘your_connection_string’)􀀄

# Define SQL query􀀄
query = “””􀀄
SELECT
customer_zip,
transaction_date,
sales_amount, -- for volume
1 AS trans_count -- for counts􀀄
FROM transactions

WHERE transaction_date BETWEEN ‘2025-03-01’ AND ‘2025-06-13’
AND customer_zip IS NOT NULL􀀄
“””􀀄

# Execute and load into DataFrame􀀄
transactions = pd.read_sql(query, engine)􀀄
