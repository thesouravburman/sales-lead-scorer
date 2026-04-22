# 🎯 Sales Lead Scorer

![SAMSUNG](https://img.shields.io/badge/SAMSUNG-R%26D%20PROJECT-1428A0?style=flat-square&logo=samsung&logoColor=white)
![ML](https://img.shields.io/badge/GRADIENT%20BOOSTING-POWERED-10B981?style=flat-square)
![Python](https://img.shields.io/badge/PYTHON-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/STREAMLIT-DEPLOYED-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
[![Live Demo](https://img.shields.io/badge/🌐%20LIVE%20DEMO-CLICK%20HERE-F59E0B?style=flat-square)](https://sales-lead-scorer.streamlit.app)

**AI-powered lead prioritisation engine using Gradient Boosting Classifier**
Built as part of the AI/ML portfolio by Sourav Burman · Samsung R&D Institute, India

---

## 🌐 Live Demo

## 👉 [https://sales-lead-scorer.streamlit.app](https://sales-lead-scorer.streamlit.app)

Enter a lead's profile and instantly see:

- ✅ Conversion probability score (0–100%)
- ✅ Hot / Warm / Cold tier classification
- ✅ Top 5 conversion factors with importance bars
- ✅ Gauge chart with colour-coded risk zones
- ✅ Batch CSV upload to score entire pipelines

---

## 🧠 What It Predicts

| Feature | Type | Description |
|---------|------|-------------|
| 📱 Lead Source | Categorical | Instagram / Facebook / Google Ads / Referral / Email / WhatsApp |
| 💄 Product Category | Categorical | Skincare / Makeup / Haircare / Wellness / Fragrance |
| ⚡ Engagement Score | Numeric (1–10) | How actively the lead engaged |
| ⏱️ Time on Site | Numeric (sec) | Session duration on the platform |
| 📄 Pages Visited | Numeric | Number of pages browsed |
| 🛒 Previous Purchases | Numeric | Historical purchase count |
| 📅 Days Since Contact | Numeric | Recency of last touchpoint |
| 💰 Budget Range | Categorical | <500 / 500–2000 / 2000–5000 / 5000+ |
| 📍 Location Tier | Categorical | Metro / Tier-1 / Tier-2 / Tier-3 |
| 👤 Age Group | Categorical | 18–24 / 25–34 / 35–44 / 45+ |

---

## 📊 App Tabs

| Tab | What It Does |
|-----|-------------|
| 🎯 Score a Lead | Real-time scoring · gauge · tier badge · factor breakdown |
| 📊 Pipeline Analytics | Conversion rates · funnels · scatter plots · histograms |
| 🧠 Model Insights | ROC curve · confusion matrix · feature importance |
| ℹ️ About | Project details · tech stack · builder info |

---

## ⚙️ Model Specifications

| Property | Value |
|----------|-------|
| Algorithm | Gradient Boosting Classifier (scikit-learn) |
| Estimators | 200 trees |
| Max Depth | 4 |
| Learning Rate | 0.08 |
| Training Data | 1,200 synthetic leads (MyGlamm D2C inspired) |
| Evaluation | ROC-AUC · Precision · Recall · Confusion Matrix |

---

## 🚀 Run Locally

```bash
git clone https://github.com/thesouravburman/sales-lead-scorer.git
cd sales-lead-scorer
pip install -r requirements.txt
streamlit run app.py
```

---

## 🛠️ Tech Stack

`Python 3.11` · `Streamlit` · `scikit-learn` · `Gradient Boosting` · `Plotly` · `Pandas` · `NumPy`

---

**Built by [Sourav Burman](https://github.com/thesouravburman) · Samsung R&D Institute · India**
