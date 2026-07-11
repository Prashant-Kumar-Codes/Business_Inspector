# Business Inspector

> Upload any transaction dataset. Map 3 columns. Get instant customer intelligence.

---

## What It Does

Business Inspector is a **universal customer analytics tool**. It takes raw transaction data from **any business** — e-commerce, SaaS, retail, restaurants — and produces:

1. **Customer Segments** — RFM analysis + K-Means clustering groups customers into Champions, Loyal, At Risk, Dormant, etc.
2. **Revenue Forecasting** — predicts next month's revenue, customer count, and transaction volume from historical trends
3. **Churn Risk Detection** — customers in low-activity clusters are flagged as likely churned — no separate model needed

Every company's data looks different. Instead of training one model on one dataset, Business Inspector **trains fresh on whatever data you provide**. The user maps their columns to 3 fields (Customer ID, Date, Amount) and the entire ML pipeline runs on the spot.

---

## How It Works

```
Upload CSV/Excel → Map 3 Columns → Clean Data → Compute RFM → Cluster → Forecast → Dashboard
```

1. User uploads a transaction file (any format, any column names)
2. User maps their columns: *"Which column is Customer ID? Date? Amount?"*
3. Data cleaning pipeline standardizes everything internally
4. RFM scores computed per customer (Recency, Frequency, Monetary)
5. K-Means finds natural customer groups; segments get business-friendly labels
6. Time-series model forecasts next month's metrics from monthly aggregates
7. Dashboard displays charts, tables, forecasts, and churn risk flags

---

## Tools Used

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| Data Wrangling | pandas, numpy |
| Clustering | scikit-learn (KMeans, StandardScaler) |
| Forecasting | statsmodels (Exponential Smoothing) |
| RFM Scoring | pandas (quintile-based scoring) |
| Backend | Flask + Blueprints |
| Frontend | Jinja2 + Chart.js |
| Server | Gunicorn |
| Containers | Docker + docker-compose |
| Deployed On | AWS (app), Neon (database) |

---

## Demo Dataset

**Online Retail II** — [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)

~1.5M transactions from a UK-based online retailer (Dec 2009 – Dec 2011). Real e-commerce data with no pre-built labels — the pipeline computes everything from raw transactions.

But the tool isn't tied to this dataset. Any CSV/Excel with customer, date, and amount columns will work.
