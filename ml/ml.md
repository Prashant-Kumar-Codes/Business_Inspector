### 1. **Visual Dashboard with Forecasting**
- **Current state graphs:**
  - Total revenue (this month)
  - Active customers count
  - Profit/loss status
  
- **1-month ahead forecast:**
  - Expected revenue trend (will next month be up or down?)
  - Predicted customer count (will we gain/lose customers?)
  - Profit/loss projection

**ML needed:** Time-series forecasting (Prophet, ARIMA, or even simple exponential smoothing)

### 2. **RFM + Clustering for Segmentation & Churn**
- **Compute RFM per customer:**
  - **R**ecency: days since last purchase
  - **F**requency: how many purchases in last X months
  - **M**onetary: total spend in last X months

- **Cluster them (K-Means)** → get customer segments (Champions, At Risk, Dormant, etc.)

- **Extract churn signal:** Customers in "dormant" or "at-risk" clusters = high churn probability

**No need for a separate classification model** — your clusters *are* your churn indicator.

---

| Part | Tool |
|---|---|
| **Data ingestion** | Python + pandas |
| **Time-series forecasting** | Prophet or ARIMA (from `statsmodels`) |
| **RFM + Clustering** | scikit-learn (K-Means) |

---