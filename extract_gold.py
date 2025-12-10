import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime

# 1. Define the ticker
ticker = "GC=F"

# 2. Download data
print(f"Extracting data for {ticker}...")
data = yf.download(ticker, period="1d", interval="1m")

# --- NEW: CLEAN UP HEADERS ---
# This fixes the "Multi-Index" issue that was causing the "0.0" error
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)  # Remove the 'Ticker' row from headers
# -----------------------------

# 3. Add timestamp
data['extracted_at'] = datetime.now()

if not data.empty:
    # 4. Connect and Save
    conn = sqlite3.connect("gold_prices.db")
    print("Connected to database...")
    
    data.to_sql("xauusd_minute_data", conn, if_exists="append", index=True)
    
    print("Data successfully saved to SQLite database!")
    conn.close()
else:
    print("No data found.")