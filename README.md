## Business Inspector

---

**What it is:**
A customer intelligence platform that takes raw e-commerce transaction data and produces three things:
1. **Customer segments** (RFM, Champions, Loyal, At Risk, Dormant) — Data analytics & unsupervised (clustring) learning
2. **Churn predictions** (who's about to leave) — supervised classification
3. **Lifetime value forecasts** (how much each customer will spend next 3 months) — neural network regression
4. **Business sales forecast** (how much the company will sale for next 3 months) - nerual networks regression

All three run on the same dataset, get stored in a database, and exposed via a REST API + dashboard.

**Why it matters:**
- Combines all three ML disciplines (unsupervised + supervised + deep learning) in one real system
- Uses proper MLOps practices (model versioning, temporal train/test splits, PR-AUC instead of just accuracy)
- Deployed to the cloud (Render + Neon) with a production-grade codebase (Docker, migrations, JWT, caching)
- Teaches you how to build something you'd actually ship, not a Jupyter notebook

---

## Tools Used

| What | Tool |
|---|---|
| Language | Python 3.11+ |
| Data Analytics & wrangling | pandas, numpy |
| Classical ML | Forecast, Clustring |
| Deep learning | Nerual Networks (PyTorch)|
| Backend | Flask (with SQL |
| Server | Gunicorn |
| Containers | Docker + docker-compose |
| Deployed on | AWS (app), Neon (database) |

**Dataset:** Online Retail II from UCI Machine Learning Repository (real e-commerce transactions, no pre-built labels — you make them yourself)
