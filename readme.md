# Stock Data Visualization

A simple, interactive web application for fetching, storing, and visualizing stock market data.

This repository demonstrates how to collect historical (or near‑real‑time) stock data, save it to an SQLite database, and display interactive charts via a lightweight Flask web app.

---

## 🚀 Project Overview

- **Repo name:** `stock_data_viswalization`
- **Author:** Nishant R De
- **Purpose:** Fetch stock market data (example scripts target NSE/Indian market), store it in `database.db`, and visualize time series (price, volume, etc.) in a browser.

---

## 🧰 Tech Stack

- **Language:** Python 3.x
- **Web framework:** Flask
- **Database:** SQLite (`database.db`)
- **Data collection:** `collect_nse_data.py` (example script)
- **DB init:** `init_db.py` and `schema.sql`
- **Frontend:** Templates in `templates/` and static assets in `static/` (JS charting library such as Chart.js or Plotly expected)

---

## 🔧 Files & Directory Structure (suggested)

```
stock_data_viswalization/
├── app.py                # Flask web app
├── collect_nse_data.py   # Script to fetch stock data (example)
├── init_db.py            # Initialize SQLite DB from schema.sql
├── schema.sql            # SQL schema for tables
├── requirements.txt      # Python dependencies
├── database.db           # (gitignored) SQLite DB created at runtime
├── templates/            # HTML templates (index, chart pages)
├── static/               # CSS, JS, images
└── README.md             # This file
```

> If any of these filenames differ in your repo, update the README accordingly.

---

## ✅ Features

- Initialize and manage a local SQLite database for stock records
- Fetch data from a market source (example: NSE) and insert into DB
- Simple Flask UI to browse and visualize stock time series (candlestick/line charts)
- Extensible: add indicators, streaming, or user accounts

---

## 📥 Requirements

Example `requirements.txt` (add/remove based on your code):

```
Flask>=2.0
pandas>=1.3
requests>=2.25
python-dotenv>=0.19
plotly>=5.0    # optional, if used
chartjs==2.9.4 # optional, for frontend
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🧭 Setup & Usage

1. **Clone the repo**

```bash
git clone https://github.com/Nishantrde/stock_data_viswalization.git
cd stock_data_viswalization
```

2. **Create a virtual environment (recommended)**

```bash
python3 -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Initialize the database**

If `init_db.py` is present, run:

```bash
python init_db.py
```

If not, create the DB from `schema.sql` manually:

```bash
sqlite3 database.db < schema.sql
```

5. **Fetch stock data**

Run the data collection script (example):

```bash
python collect_nse_data.py --symbol RELIANCE --start 2020-01-01 --end 2025-01-01
```

Adjust options to match how `collect_nse_data.py` accepts arguments. The script should insert rows into `database.db`.

6. **Run the web app**

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## 🔎 Example: Minimal `app.py` (reference)

> The repository may already contain `app.py`. Below is a minimal Flask app example to serve as reference if you need to recreate or test locally.

```python
# app.py (minimal example)
from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)
DB_PATH = "database.db"

def query_stock(symbol, start=None, end=None):
    con = sqlite3.connect(DB_PATH)
    q = f"SELECT date, open, high, low, close, volume FROM stocks WHERE symbol = ?"
    params = [symbol]
    df = pd.read_sql_query(q, con, params=params, parse_dates=["date"])
    con.close()
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    symbol = request.args.get('symbol', 'RELIANCE')
    df = query_stock(symbol)
    return df.to_json(orient='records', date_format='iso')

if __name__ == '__main__':
    app.run(debug=True)
```

> Adapt the queries and columns to match your `schema.sql`.

---

## ⚙️ Example: `init_db.py` (reference)

```python
# init_db.py
import sqlite3
from pathlib import Path

DB_PATH = Path('database.db')
SCHEMA = Path('schema.sql')

def init_db():
    if DB_PATH.exists():
        print('database.db already exists — remove it first if you want a fresh db')
        return
    con = sqlite3.connect(DB_PATH)
    with open(SCHEMA, 'r') as f:
        con.executescript(f.read())
    con.commit()
    con.close()
    print('Initialized database.db using schema.sql')

if __name__ == '__main__':
    init_db()
```

---

## 🗃️ Example `schema.sql` (reference)

```sql
-- schema.sql
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    UNIQUE(symbol, date)
);
```

---

## ✅ Tips & Next Steps

- Add a `.gitignore` to exclude `database.db` and `venv/`.
- Add unit tests for data ingestion and DB operations.
- Add a scheduler (cron, celery, or APScheduler) for periodic data collection.
- Enhance the frontend with more charts and controls (date range, moving averages, indicators).

---

## 🤝 Contributing

Contributions welcome. Fork the repo, make changes on a branch, and submit a pull request. Please include clear descriptions and tests where possible.

---

## 📄 License

Add a license file to the repo (for example, `LICENSE` with MIT license). If you want, include an example MIT license block here:

```
MIT License

Copyright (c) 2025 Nishant R De

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
... (add the rest of the license text)
```

---

## ✉️ Contact

Created by **Nishant R De**. For questions, open an issue in the repo or contact via your preferred channel.

---

Thank you for sharing your project — if you want, I can also:
- generate a `requirements.txt` from your environment,
- produce sample `index.html` and JS for Chart.js visualization,
- or create a Dockerfile to containerize the app.

