import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, roc_auc_score,
                              precision_score, recall_score,
                              confusion_matrix, roc_curve)
from sklearn.preprocessing import LabelEncoder
import streamlit as st

LEAD_SOURCES   = ['Instagram', 'Facebook', 'Google Ads', 'Referral', 'Email', 'WhatsApp']
PRODUCT_CATS   = ['Skincare', 'Makeup', 'Haircare', 'Wellness', 'Fragrance']
BUDGET_RANGES  = ['< Rs.500', 'Rs.500-2000', 'Rs.2000-5000', 'Rs.5000-10000', '> Rs.10000']
LOCATION_TIERS = ['Metro', 'Tier-1', 'Tier-2', 'Tier-3']
AGE_GROUPS     = ['18-24', '25-34', '35-44', '45-54', '55+']

def generate_data(n=1200, seed=42):
    np.random.seed(seed)
    ls  = np.random.choice(LEAD_SOURCES,   n, p=[0.30,0.20,0.15,0.15,0.10,0.10])
    pc  = np.random.choice(PRODUCT_CATS,   n, p=[0.35,0.30,0.15,0.12,0.08])
    eng = np.random.randint(1, 11, n)
    tst = np.random.randint(30, 600, n)
    pv  = np.random.randint(1, 15, n)
    pp  = np.random.randint(0, 8, n)
    ds  = np.random.randint(1, 90, n)
    br  = np.random.choice(BUDGET_RANGES,  n, p=[0.15,0.30,0.30,0.15,0.10])
    loc = np.random.choice(LOCATION_TIERS, n, p=[0.35,0.30,0.25,0.10])
    ag  = np.random.choice(AGE_GROUPS,     n, p=[0.25,0.35,0.22,0.13,0.05])
    source_w = {'Referral':3,'Instagram':2,'Facebook':1.5,'WhatsApp':1.5,'Google Ads':1,'Email':0.5}
    budget_w = {'< Rs.500':0,'Rs.500-2000':1,'Rs.2000-5000':2,'Rs.5000-10000':3,'> Rs.10000':4}
    cat_w    = {'Skincare':1.5,'Makeup':1.5,'Haircare':1,'Wellness':0.8,'Fragrance':0.5}
    loc_w    = {'Metro':1,'Tier-1':0.8,'Tier-2':0.5,'Tier-3':0.2}
    score = np.array([source_w[s]+budget_w[b]+cat_w[c]+loc_w[l]
                      for s,b,c,l in zip(ls,br,pc,loc)], dtype=float)
    score += eng*0.8 + pp*1.2 + (tst/600)*2 + (pv/15)*1.5 - (ds/90)*2
    score += np.random.normal(0, 1.5, n)
    converted = (score > np.percentile(score, 62)).astype(int)
    return pd.DataFrame({
        'lead_source':ls,'product_category':pc,'engagement_score':eng,
        'time_on_site_sec':tst,'pages_visited':pv,'previous_purchases':pp,
        'days_since_contact':ds,'budget_range':br,'location_tier':loc,
        'age_group':ag,'converted':converted
    })

@st.cache_resource
def get_model():
    df = generate_data()
    cat_cols = ['lead_source','product_category','budget_range','location_tier','age_group']
    encoders = {}
    df_enc = df.copy()
    for col in cat_cols:
        le = LabelEncoder()
        df_enc[col] = le.fit_transform(df[col])
        encoders[col] = le
    FEATURES = ['lead_source','product_category','engagement_score','time_on_site_sec',
                'pages_visited','previous_purchases','days_since_contact',
                'budget_range','location_tier','age_group']
    X = df_enc[FEATURES]
    y = df_enc['converted']
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    mdl = GradientBoostingClassifier(n_estimators=200, max_depth=4,
                                     learning_rate=0.1, min_samples_leaf=10, random_state=42)
    mdl.fit(Xtr, ytr)
    y_pred  = mdl.predict(Xte)
    y_proba = mdl.predict_proba(Xte)[:,1]
    fpr, tpr, _ = roc_curve(yte, y_proba)
    metrics = {
        "accuracy":            accuracy_score(yte, y_pred),
        "roc_auc":             roc_auc_score(yte, y_proba),
        "precision":           precision_score(yte, y_pred),
        "recall":              recall_score(yte, y_pred),
        "confusion_matrix":    confusion_matrix(yte, y_pred).tolist(),
        "feature_importances": mdl.feature_importances_.tolist(),
        "fpr":                 fpr.tolist(),
        "tpr":                 tpr.tolist(),
    }
    return mdl, encoders, FEATURES, metrics, df

def predict_lead(model, encoders, features, lead_data):
    cat_cols = ['lead_source','product_category','budget_range','location_tier','age_group']
    row = {col: (encoders[col].transform([lead_data[col]])[0]
                 if col in cat_cols else lead_data[col])
           for col in features}
    prob = model.predict_proba(pd.DataFrame([row]))[0][1]
    return prob, None, None
