# 🎯 Sales Lead Scorer

> AI-powered lead prioritisation engine · Gradient Boosting · Streamlit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sales-lead-scorer.streamlit.app)

---

## Overview

Predicts the **conversion probability** of a sales lead in real time using a
Gradient Boosting Classifier trained on 1,200 synthetic MyGlamm-inspired leads.
Score individual leads or batch-upload a CSV to rank your entire pipeline.

## Features

| Tab | What it does |
|-----|-------------|
| 🎯 Score a Lead | Real-time scoring with gauge, tier badge & factor breakdown |
| 📊 Pipeline Analytics | Conversion rates, funnels, scatter plots, histograms |
| 🧠 Model Insights | ROC curve, confusion matrix, feature importance |
| ℹ️ About | Project details, tech stack, builder info |

## Model

- **Algorithm:** Gradient Boosting Classifier (scikit-learn)
- **Estimators:** 200 trees · Max depth: 4 · Learning rate: 0.08
- **Features:** lead_source, product_category, engagement_score, time_on_site_sec,
  pages_visited, previous_purchases, days_since_contact, budget_range, location_tier, age_group
- **Training data:** 1,200 synthetic leads (MyGlamm D2C funnel inspired)

## Tech Stack

`Python` · `Streamlit` · `scikit-learn` · `Plotly` · `Pandas` · `NumPy`

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

**Built by [Sourav Burman](https://github.com/thesouravburman)**
