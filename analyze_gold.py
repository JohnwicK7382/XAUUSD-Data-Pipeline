import sqlite3
import pandas as pd

# 1. Connect to the database
conn = sqlite3.connect("gold_prices.db")

# 2. The "Window Function" Query
# We use 'AVG(Close) OVER...' to look back at previous rows
query = """
SELECT 
    Datetime,
    "Close" as Current_Price,
    AVG("Close") OVER (
        ORDER BY Datetime 
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) as SMA_5_Min,
    ("High" - "Low") as Volatility
FROM xauusd_minute_data
ORDER BY Datetime DESC
LIMIT 10
"""

# 3. Run Query and Print
df = pd.read_sql(query, conn)

print("--- LIVE MARKET ANALYTICS (SQL) ---")
print(df)
import matplotlib.pyplot as plt

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(df['Datetime'], df['Current_Price'], label='Gold Price', color='gold')
plt.plot(df['Datetime'], df['SMA_5_Min'], label='SMA (5 Min)', color='blue', linestyle='--')

plt.title('Live XAUUSD Price vs. Simple Moving Average (SQL Calculated)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Show the chart
print("Opening chart...")
plt.show()

conn.close()