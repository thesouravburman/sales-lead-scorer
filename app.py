import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from model import get_model, predict_lead

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Lead Scorer · Sourav Burman",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS injected via JavaScript (bypasses Streamlit's <style> tag sanitizer) ───
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;900&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<script>
(function injectCSS() {
  var id = 'lead-scorer-global-css';
  var existing = document.getElementById(id);
  if (existing) existing.remove();
  var style = document.createElement('style');
  style.id = id;
  style.textContent = [
    'html, body, [class*="css"] { font-family: Poppins, sans-serif; background: #060A0F; color: #E2E8F0; }',
    '.stApp { background: #060A0F; }',
    '#MainMenu, footer, header { visibility: hidden; }',
    '.block-container { padding-top: 1rem; padding-bottom: 2rem; }',
    '.stTabs [data-baseweb="tab-list"] { gap: 4px; background: rgba(16,185,129,0.06); border-radius: 12px; padding: 6px; border: 1px solid rgba(16,185,129,0.15); }',
    '.stTabs [data-baseweb="tab"] { background: transparent; border-radius: 8px; color: #94A3B8; font-family: Montserrat, sans-serif; font-weight: 600; font-size: 0.78rem; letter-spacing: 0.08em; padding: 8px 20px; border: none; }',
    '.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #10B981, #059669) !important; color: #fff !important; }',
    '.glass-card { background: rgba(16,185,129,0.05); border: 1px solid rgba(16,185,129,0.2); border-radius: 16px; padding: 24px; margin-bottom: 16px; backdrop-filter: blur(12px); }',
    '.amber-card { background: rgba(245,158,11,0.06); border: 1px solid rgba(245,158,11,0.25); border-radius: 16px; padding: 24px; margin-bottom: 16px; }',
    '.purple-card { background: rgba(139,92,246,0.06); border: 1px solid rgba(139,92,246,0.25); border-radius: 16px; padding: 24px; margin-bottom: 16px; }',
    '.metric-tile { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.3); border-radius: 14px; padding: 20px; text-align: center; }',
    '.metric-val { font-family: Montserrat, sans-serif; font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #10B981, #F59E0B); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }',
    '.metric-lbl { font-size: 0.72rem; color: #64748B; letter-spacing: 0.12em; text-transform: uppercase; font-family: Montserrat, sans-serif; margin-top: 4px; }',
    'label, .stSelectbox label, .stSlider label { font-family: Montserrat, sans-serif !important; font-size: 0.78rem !important; letter-spacing: 0.06em !important; color: #94A3B8 !important; text-transform: uppercase !important; }',
    '.stButton > button { background: linear-gradient(135deg, #10B981, #059669); color: #fff; border: none; border-radius: 10px; font-family: Montserrat, sans-serif; font-weight: 700; letter-spacing: 0.1em; padding: 12px 32px; font-size: 0.85rem; width: 100%; cursor: pointer; transition: all 0.2s; }',
    '.stButton > button:hover { background: linear-gradient(135deg, #059669, #047857); transform: translateY(-1px); box-shadow: 0 8px 24px rgba(16,185,129,0.35); }',
    '.brand-watermark { position: fixed; top: 14px; right: 18px; font-family: Montserrat, sans-serif; font-size: 0.62rem; letter-spacing: 0.18em; color: rgba(16,185,129,0.28); z-index: 999; pointer-events: none; }',
    '.brand-watermark-left { position: fixed; top: 14px; left: 18px; font-family: Montserrat, sans-serif; font-size: 0.62rem; letter-spacing: 0.18em; color: rgba(16,185,129,0.28); z-index: 999; pointer-events: none; }',
    'h1, h2, h3 { font-family: Montserrat, sans-serif !important; letter-spacing: 0.05em !important; }',
    '.emerald-divider { height: 1px; background: linear-gradient(90deg, transparent, #10B981, transparent); margin: 20px 0; border: none; }',
    '.dataframe { font-size: 0.8rem; }',
    '.js-plotly-plot .plotly { background: transparent !important; }'
  ].join(' ');
  document.head.appendChild(style);
  setTimeout(injectCSS, 800);
})();
</script>
""", unsafe_allow_html=True)

# ── Animated particle background ───────────────────────────────────────────────
st.markdown("""
<canvas id="leadCanvas" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;"></canvas>
<script>
(function(){
  const canvas = document.getElementById('leadCanvas');
  if(!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  window.addEventListener('resize', ()=>{ canvas.width=window.innerWidth; canvas.height=window.innerHeight; });
  const N = 55;
  const COLORS = ['#10B981','#F59E0B','#8B5CF6','#06FFA5','#D97706'];
  const pts = Array.from({length:N}, ()=>({
    x: Math.random()*canvas.width, y: Math.random()*canvas.height,
    vx: (Math.random()-0.5)*0.45, vy: (Math.random()-0.5)*0.45,
    r: Math.random()*2.2+0.8,
    c: COLORS[Math.floor(Math.random()*COLORS.length)],
    a: Math.random()*0.55+0.2
  }));
  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    for(let i=0;i<N;i++){
      for(let j=i+1;j<N;j++){
        const dx=pts[i].x-pts[j].x, dy=pts[i].y-pts[j].y;
        const dist=Math.sqrt(dx*dx+dy*dy);
        if(dist<130){
          ctx.beginPath(); ctx.moveTo(pts[i].x,pts[i].y); ctx.lineTo(pts[j].x,pts[j].y);
          ctx.strokeStyle=`rgba(16,185,129,${(1-dist/130)*0.12})`; ctx.lineWidth=0.7; ctx.stroke();
        }
      }
    }
    pts.forEach(p=>{
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle=p.c+Math.floor(p.a*255).toString(16).padStart(2,'0'); ctx.fill();
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<0||p.x>canvas.width) p.vx*=-1;
      if(p.y<0||p.y>canvas.height) p.vy*=-1;
    });
    requestAnimationFrame(draw);
  }
  draw();
})();
</script>
""", unsafe_allow_html=True)

st.markdown('<div class="brand-watermark">⬡ SOURAV BURMAN · CS ENGINEER</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-watermark-left">⬡ SALES LEAD SCORER v1.0</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:30px 0 10px;">
  <div style="font-family:'Montserrat',sans-serif;font-size:0.72rem;letter-spacing:0.35em;
              color:#10B981;text-transform:uppercase;margin-bottom:8px;">
    AI-POWERED · GRADIENT BOOSTING · MYGLAMM-INSPIRED
  </div>
  <h1 style="font-family:'Montserrat',sans-serif;font-size:2.6rem;font-weight:900;
             background:linear-gradient(135deg,#10B981,#F59E0B,#8B5CF6);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             margin:0;letter-spacing:0.04em;">
    SALES LEAD SCORER
  </h1>
  <div style="color:#64748B;font-size:0.85rem;margin-top:8px;font-family:'Poppins',sans-serif;">
    Predict conversion probability · Prioritise your pipeline · Close more deals
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="emerald-divider"></div>', unsafe_allow_html=True)

# ── Load model ──────────────────────────────────────────────────────────────────
@st.cache_resource
def load():
    return get_model()

model, encoders, feature_names, metrics, df = load()

# ── TABS ────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯  SCORE A LEAD", "📊  PIPELINE ANALYTICS",
    "🧠  MODEL INSIGHTS", "ℹ️  ABOUT"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SCORE A LEAD
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    col_form, col_result = st.columns([1.1, 0.9], gap="large")

    with col_form:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Montserrat',sans-serif;font-size:0.68rem;
                    letter-spacing:0.2em;color:#10B981;margin-bottom:16px;">
          ● LEAD PROFILE INPUT
        </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            lead_source = st.selectbox("Lead Source",
                ["Instagram","Facebook","Google Ads","Referral","Email","WhatsApp"])
            product_cat = st.selectbox("Product Category",
                ["Skincare","Makeup","Haircare","Wellness","Fragrance"])
            location    = st.selectbox("Location Tier",
                ["Metro","Tier-1","Tier-2","Tier-3"])
            age_group   = st.selectbox("Age Group",
                ["18-24","25-34","35-44","45-54","55+"])
            budget      = st.selectbox("Budget Range",
                ["< Rs.500","Rs.500-2000","Rs.2000-5000","Rs.5000-10000","> Rs.10000"])
        with c2:
            engagement = st.slider("Engagement Score", 1, 10, 6)
            time_site  = st.slider("Time on Site (sec)", 30, 600, 180)
            pages      = st.slider("Pages Visited", 1, 20, 5)
            prev_purch = st.slider("Previous Purchases", 0, 10, 1)
            days_since = st.slider("Days Since Last Contact", 0, 90, 7)

        st.markdown("</div>", unsafe_allow_html=True)
        score_btn = st.button("⚡  SCORE THIS LEAD")

    with col_result:
        # ── CHANGE 1: Social links pinned to top of right column ──────────────
        st.markdown("""
        <div style="text-align:right;margin-bottom:12px;">
          <a href="https://github.com/thesouravburman" target="_blank"
             style="display:inline-flex;align-items:center;gap:6px;
                    background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);
                    border-radius:8px;padding:6px 12px;text-decoration:none;
                    font-family:'Montserrat',sans-serif;font-size:0.72rem;
                    color:#10B981;letter-spacing:0.06em;margin-left:8px;
                    transition:background 0.2s;">
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24"
                 fill="currentColor">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57
                       0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41
                       -1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815
                       2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925
                       0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23
                       .96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65
                       .24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925
                       .435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57
                       A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
            </svg>
            GitHub
          </a>
          <a href="https://www.linkedin.com/in/sourav-burman/" target="_blank"
             style="display:inline-flex;align-items:center;gap:6px;
                    background:rgba(10,102,194,0.1);border:1px solid rgba(10,102,194,0.3);
                    border-radius:8px;padding:6px 12px;text-decoration:none;
                    font-family:'Montserrat',sans-serif;font-size:0.72rem;
                    color:#60A5FA;letter-spacing:0.06em;margin-left:8px;
                    transition:background 0.2s;">
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24"
                 fill="currentColor">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136
                       1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85
                       3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0
                       1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452z
                       M22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451
                       C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
            LinkedIn
          </a>
          <a href="mailto:thesouravburman@gmail.com"
             style="display:inline-flex;align-items:center;gap:6px;
                    background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.25);
                    border-radius:8px;padding:6px 12px;text-decoration:none;
                    font-family:'Montserrat',sans-serif;font-size:0.72rem;
                    color:#F59E0B;letter-spacing:0.06em;margin-left:8px;
                    transition:background 0.2s;">
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24"
                 fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
            Mail
          </a>
        </div>
        """, unsafe_allow_html=True)

        if score_btn:
            lead_data = {
                "lead_source":        lead_source,
                "product_category":   product_cat,
                "engagement_score":   engagement,
                "time_on_site_sec":   time_site,
                "pages_visited":      pages,
                "previous_purchases": prev_purch,
                "days_since_contact": days_since,
                "budget_range":       budget,
                "location_tier":      location,
                "age_group":          age_group,
            }
            prob, _, __ = predict_lead(model, encoders, feature_names, lead_data)
            pct = int(prob * 100)

            if pct >= 70:   score_color, tier, tier_icon = "#10B981", "HOT LEAD",  "🔥"
            elif pct >= 45: score_color, tier, tier_icon = "#F59E0B", "WARM LEAD", "🌡️"
            else:           score_color, tier, tier_icon = "#EF4444", "COLD LEAD", "❄️"

            r = int(score_color[1:3], 16)
            g = int(score_color[3:5], 16)
            b = int(score_color[5:7], 16)

            st.markdown(f"""
            <div class="glass-card" style="border-color:{score_color}40;
                 background:rgba({r},{g},{b},0.07);">
              <div style="text-align:center;padding:10px 0 18px;">
                <div style="font-family:'Montserrat',sans-serif;font-size:0.68rem;
                            letter-spacing:0.22em;color:{score_color};margin-bottom:6px;">
                  {tier_icon}  {tier}
                </div>
                <div style="font-family:'Montserrat',sans-serif;font-size:4.8rem;
                            font-weight:900;color:{score_color};line-height:1;">
                  {pct}%
                </div>
                <div style="color:#94A3B8;font-size:0.78rem;margin-top:4px;">
                  Conversion Probability
                </div>
              </div>
            """, unsafe_allow_html=True)

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pct,
                number={"suffix":"%","font":{"color":score_color,"size":28,"family":"Montserrat"}},
                gauge={
                    "axis":{"range":[0,100],"tickcolor":"#334155",
                            "tickfont":{"color":"#64748B","size":10}},
                    "bar":{"color":score_color,"thickness":0.28},
                    "bgcolor":"rgba(0,0,0,0)", "borderwidth":0,
                    "steps":[
                        {"range":[0,45],  "color":"rgba(239,68,68,0.12)"},
                        {"range":[45,70], "color":"rgba(245,158,11,0.12)"},
                        {"range":[70,100],"color":"rgba(16,185,129,0.12)"}
                    ],
                    "threshold":{"line":{"color":score_color,"width":3},
                                 "thickness":0.8,"value":pct}
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=20,b=10,l=20,r=20), height=200,
                font={"color":"#E2E8F0"})
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="amber-card">', unsafe_allow_html=True)
            st.markdown("""<div style="font-family:'Montserrat',sans-serif;font-size:0.68rem;
                          letter-spacing:0.2em;color:#F59E0B;margin-bottom:14px;">
                          ▲ TOP CONVERSION FACTORS</div>""", unsafe_allow_html=True)
            fi_pairs = sorted(zip(feature_names, metrics["feature_importances"]),
                              key=lambda x: x[1], reverse=True)
            for feat, imp in fi_pairs[:5]:
                bar_pct = int(imp * 300)
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                  <div style="display:flex;justify-content:space-between;
                              font-size:0.75rem;color:#CBD5E1;margin-bottom:3px;">
                    <span>{feat.replace('_',' ').title()}</span>
                    <span style="color:#F59E0B;">{imp:.3f}</span>
                  </div>
                  <div style="background:#1E293B;border-radius:4px;height:5px;">
                    <div style="width:{min(bar_pct,100)}%;height:5px;border-radius:4px;
                                background:linear-gradient(90deg,#F59E0B,#10B981);"></div>
                  </div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center;padding:60px 20px;">
              <div style="font-size:3rem;margin-bottom:16px;">🎯</div>
              <div style="font-family:'Montserrat',sans-serif;font-size:1rem;
                          font-weight:700;color:#10B981;letter-spacing:0.1em;">
                READY TO SCORE
              </div>
              <div style="color:#475569;font-size:0.82rem;margin-top:8px;">
                Fill in the lead profile and click<br>
                <b style="color:#F59E0B;">⚡ SCORE THIS LEAD</b>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="purple-card">', unsafe_allow_html=True)
        st.markdown("""<div style="font-family:'Montserrat',sans-serif;font-size:0.68rem;
                      letter-spacing:0.2em;color:#8B5CF6;margin-bottom:12px;">
                      📂 BATCH CSV SCORER</div>""", unsafe_allow_html=True)
        st.markdown("""<div style='font-size:0.78rem;color:#64748B;margin-bottom:10px;'>
            Upload a CSV with columns: lead_source, product_category, engagement_score,
            time_on_site_sec, pages_visited, previous_purchases, days_since_contact,
            budget_range, location_tier, age_group</div>""", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        if uploaded:
            try:
                batch_df = pd.read_csv(uploaded)
                results = []
                for _, row in batch_df.iterrows():
                    p, _, __ = predict_lead(model, encoders, feature_names, row.to_dict())
                    results.append(int(p*100))
                batch_df["Score (%)"] = results
                batch_df["Tier"] = batch_df["Score (%)"].apply(
                    lambda x: "🔥 Hot" if x>=70 else ("🌡️ Warm" if x>=45 else "❄️ Cold"))
                batch_df = batch_df.sort_values("Score (%)", ascending=False)
                st.dataframe(
                    batch_df[["Score (%)","Tier"] +
                              [c for c in batch_df.columns if c not in ["Score (%)","Tier"]]
                             ].head(20),
                    use_container_width=True)
            except Exception as e:
                st.error(f"CSV error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PIPELINE ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    converted = df[df["converted"]==1]
    not_conv  = df[df["converted"]==0]
    conv_rate = len(converted)/len(df)*100
    avg_eng   = df["engagement_score"].mean()
    top_src   = df.groupby("lead_source")["converted"].mean().idxmax()

    k1,k2,k3,k4 = st.columns(4)
    for col, val, lbl in [
        (k1, f"{len(df):,}",      "TOTAL LEADS"),
        (k2, f"{conv_rate:.1f}%", "CONV. RATE"),
        (k3, f"{avg_eng:.1f}/10", "AVG ENGAGEMENT"),
        (k4, top_src,             "BEST SOURCE"),
    ]:
        with col:
            st.markdown(f"""<div class="metric-tile">
              <div class="metric-val">{val}</div>
              <div class="metric-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)

    with r1c1:
        src_conv = df.groupby("lead_source")["converted"].mean().reset_index()
        src_conv.columns = ["Source","Conv. Rate"]
        src_conv = src_conv.sort_values("Conv. Rate", ascending=True)
        fig1 = px.bar(src_conv, x="Conv. Rate", y="Source", orientation="h",
                      color="Conv. Rate",
                      color_continuous_scale=["#134e4a","#10B981","#6ee7b7"],
                      title="CONVERSION RATE BY SOURCE")
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8",family="Poppins"),
            title_font=dict(family="Montserrat",size=13,color="#10B981"),
            coloraxis_showscale=False,
            xaxis=dict(tickformat=".0%",gridcolor="#1E293B"),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            margin=dict(l=10,r=10,t=40,b=10), height=280)
        st.plotly_chart(fig1, use_container_width=True)

    with r1c2:
        cat_df = df.groupby("product_category").agg(
            Total=("converted","count"), Converted=("converted","sum")).reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Total", x=cat_df["product_category"], y=cat_df["Total"],
                              marker_color="rgba(139,92,246,0.35)",
                              marker_line_color="#8B5CF6", marker_line_width=1))
        fig2.add_trace(go.Bar(name="Converted", x=cat_df["product_category"],
                              y=cat_df["Converted"], marker_color="#10B981"))
        fig2.update_layout(
            barmode="overlay", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8",family="Poppins"),
            title=dict(text="LEADS BY PRODUCT CATEGORY",
                       font=dict(family="Montserrat",size=13,color="#8B5CF6")),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            yaxis=dict(gridcolor="#1E293B"),
            margin=dict(l=10,r=10,t=40,b=10), height=280)
        st.plotly_chart(fig2, use_container_width=True)

    r2c1, r2c2 = st.columns(2)

    with r2c1:
        fig3 = go.Figure()
        fig3.add_trace(go.Histogram(x=converted["engagement_score"], name="Converted",
                                    marker_color="#10B981", opacity=0.75, xbins=dict(size=1)))
        fig3.add_trace(go.Histogram(x=not_conv["engagement_score"], name="Not Converted",
                                    marker_color="#EF4444", opacity=0.55, xbins=dict(size=1)))
        fig3.update_layout(
            barmode="overlay", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8",family="Poppins"),
            title=dict(text="ENGAGEMENT SCORE DISTRIBUTION",
                       font=dict(family="Montserrat",size=13,color="#F59E0B")),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="#1E293B",title="Engagement Score"),
            yaxis=dict(gridcolor="#1E293B",title="Count"),
            margin=dict(l=10,r=10,t=40,b=10), height=280)
        st.plotly_chart(fig3, use_container_width=True)

    with r2c2:
        tier_df = df.groupby("location_tier").agg(
            Total=("converted","count"), Converted=("converted","sum")).reset_index()
        tier_df["Rate"] = tier_df["Converted"]/tier_df["Total"]*100
        fig4 = px.funnel(tier_df, x="Total", y="location_tier",
                         color_discrete_sequence=["#F59E0B"],
                         title="PIPELINE FUNNEL BY LOCATION TIER")
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8",family="Poppins"),
            title_font=dict(family="Montserrat",size=13,color="#F59E0B"),
            margin=dict(l=10,r=10,t=40,b=10), height=280)
        st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.scatter(df.sample(min(400,len(df))),
                      x="engagement_score", y="time_on_site_sec",
                      color="converted", size="pages_visited",
                      color_continuous_scale=["#EF4444","#10B981"],
                      title="ENGAGEMENT vs TIME ON SITE  (size = pages visited)",
                      labels={"engagement_score":"Engagement Score",
                              "time_on_site_sec":"Time on Site (sec)",
                              "converted":"Converted"})
    fig5.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8",family="Poppins"),
        title_font=dict(family="Montserrat",size=13,color="#E2E8F0"),
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="#1E293B"),
        yaxis=dict(gridcolor="#1E293B"),
        margin=dict(l=10,r=10,t=45,b=10), height=320)
    st.plotly_chart(fig5, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MODEL INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)

    m1,m2,m3,m4 = st.columns(4)
    kpi_data = [
        (f"{metrics['accuracy']*100:.1f}%", "MODEL ACCURACY"),
        (f"{metrics['roc_auc']:.4f}",        "ROC-AUC SCORE"),
        (f"{metrics['precision']*100:.1f}%",  "PRECISION"),
        (f"{metrics['recall']*100:.1f}%",     "RECALL"),
    ]
    for col, (val,lbl) in zip([m1,m2,m3,m4], kpi_data):
        with col:
            st.markdown(f"""<div class="metric-tile">
              <div class="metric-val">{val}</div>
              <div class="metric-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    mc1, mc2 = st.columns(2)

    with mc1:
        fi = pd.DataFrame({"Feature": feature_names,
                           "Importance": metrics["feature_importances"]})
        fi = fi.sort_values("Importance")
        fig_fi = px.bar(fi, x="Importance", y="Feature", orientation="h",
                        color="Importance",
                        color_continuous_scale=["#134e4a","#10B981","#d1fae5"],
                        title="FEATURE IMPORTANCE")
        fig_fi.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8",family="Poppins"),
            title_font=dict(family="Montserrat",size=13,color="#10B981"),
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="#1E293B"),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            margin=dict(l=10,r=10,t=40,b=10), height=320)
        st.plotly_chart(fig_fi, use_container_width=True)

    with mc2:
        cm = metrics["confusion_matrix"]
        fig_cm = px.imshow(cm,
                           labels=dict(x="Predicted", y="Actual", color="Count"),
                           x=["Not Converted","Converted"],
                           y=["Not Converted","Converted"],
                           color_continuous_scale=["#060A0F","#10B981"],
                           text_auto=True,
                           title="CONFUSION MATRIX")
        fig_cm.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8",family="Poppins"),
            title_font=dict(family="Montserrat",size=13,color="#8B5CF6"),
            coloraxis_showscale=False,
            margin=dict(l=10,r=10,t=40,b=10), height=320)
        st.plotly_chart(fig_cm, use_container_width=True)

    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(x=metrics["fpr"], y=metrics["tpr"], mode="lines",
                                 name=f"ROC (AUC={metrics['roc_auc']:.3f})",
                                 line=dict(color="#10B981", width=2.5)))
    fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines",
                                 line=dict(color="#EF4444", dash="dash", width=1.5),
                                 name="Random Classifier"))
    fig_roc.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8",family="Poppins"),
        title=dict(text="ROC CURVE", font=dict(family="Montserrat",size=13,color="#F59E0B")),
        xaxis=dict(title="False Positive Rate", gridcolor="#1E293B"),
        yaxis=dict(title="True Positive Rate", gridcolor="#1E293B"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10,r=10,t=40,b=10), height=300)
    st.plotly_chart(fig_roc, use_container_width=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Montserrat',sans-serif;font-size:0.68rem;
                letter-spacing:0.2em;color:#10B981;margin-bottom:14px;">⚙ MODEL SPECIFICATIONS</div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;font-size:0.82rem;">
      <div><span style="color:#64748B;">Algorithm</span><br>
           <b style="color:#E2E8F0;">Gradient Boosting Classifier</b></div>
      <div><span style="color:#64748B;">Estimators</span><br>
           <b style="color:#E2E8F0;">200 Trees</b></div>
      <div><span style="color:#64748B;">Max Depth</span><br>
           <b style="color:#E2E8F0;">4</b></div>
      <div><span style="color:#64748B;">Learning Rate</span><br>
           <b style="color:#E2E8F0;">0.1</b></div>
      <div><span style="color:#64748B;">Features</span><br>
           <b style="color:#E2E8F0;">10 (mixed types)</b></div>
      <div><span style="color:#64748B;">Training Data</span><br>
           <b style="color:#E2E8F0;">1,200 synthetic leads</b></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    ac1, ac2 = st.columns([1.6, 1])

    with ac1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Montserrat',sans-serif;font-size:0.68rem;
                    letter-spacing:0.2em;color:#10B981;margin-bottom:16px;">
          ● ABOUT THIS PROJECT
        </div>
        <h2 style="font-family:'Montserrat',sans-serif;font-weight:900;font-size:1.5rem;
                   margin:0 0 12px;background:linear-gradient(135deg,#10B981,#F59E0B);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
          SALES LEAD SCORER
        </h2>
        <p style="color:#94A3B8;line-height:1.8;font-size:0.88rem;">
          An AI-powered lead prioritisation engine inspired by MyGlamm's D2C sales funnel.
          Uses a <b style="color:#10B981;">Gradient Boosting Classifier</b> trained on 1,200
          synthetic leads across 10 behavioural and demographic features to predict conversion
          probability in real time.
        </p>
        <p style="color:#94A3B8;line-height:1.8;font-size:0.88rem;">
          Sales teams can score individual leads or upload a CSV to batch-score their entire
          pipeline, enabling data-driven prioritisation and higher close rates.
        </p>
        <div style="margin-top:20px;">
          <div style="font-family:'Montserrat',sans-serif;font-size:0.68rem;
                      letter-spacing:0.2em;color:#F59E0B;margin-bottom:10px;">▲ KEY FEATURES</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;
                      font-size:0.82rem;color:#CBD5E1;">
            <div>🎯 Real-time lead scoring</div>
            <div>📊 Pipeline analytics dashboard</div>
            <div>📂 Batch CSV upload</div>
            <div>🧠 ROC curve + confusion matrix</div>
            <div>🔥 Hot / Warm / Cold tiering</div>
            <div>📈 Feature importance explainability</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with ac2:
        st.markdown('<div class="amber-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Montserrat',sans-serif;font-size:0.68rem;
                    letter-spacing:0.2em;color:#F59E0B;margin-bottom:16px;">● BUILDER</div>
        <div style="text-align:center;padding:10px 0;">
          <div style="font-size:3rem;margin-bottom:10px;">👨‍💻</div>
          <div style="font-family:'Montserrat',sans-serif;font-size:1.3rem;
                      font-weight:900;color:#E2E8F0;letter-spacing:0.06em;">SOURAV BURMAN</div>
          <div style="color:#64748B;font-size:0.78rem;letter-spacing:0.12em;margin-top:4px;">
            CS ENGINEER · AI/ML</div>
          <div style="margin-top:16px;font-size:0.8rem;color:#94A3B8;line-height:1.9;">
            <a href="https://github.com/thesouravburman" target="_blank"
               style="color:#94A3B8;text-decoration:none;display:flex;align-items:center;
                      justify-content:center;gap:6px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                   fill="currentColor">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57
                         0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41
                         -1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815
                         2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925
                         0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23
                         .96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65
                         .24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925
                         .435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57
                         A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
              </svg>
              github.com/thesouravburman
            </a>
            <a href="https://www.linkedin.com/in/sourav-burman/" target="_blank"
               style="color:#94A3B8;text-decoration:none;display:flex;align-items:center;
                      justify-content:center;gap:6px;margin-top:4px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                   fill="currentColor">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136
                         1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85
                         3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0
                         1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452z
                         M22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451
                         C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
              linkedin.com/in/sourav-burman
            </a>
            <a href="mailto:thesouravburman@gmail.com"
               style="color:#94A3B8;text-decoration:none;display:flex;align-items:center;
                      justify-content:center;gap:6px;margin-top:4px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                   fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                   stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              thesouravburman@gmail.com
            </a>
          </div>
        </div>
        """, unsafe_allow_html=True)
        # ── CHANGE 2: Samsung R&D Institute block removed ──────────────────────
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="purple-card" style="margin-top:0;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Montserrat',sans-serif;font-size:0.68rem;
                    letter-spacing:0.2em;color:#8B5CF6;margin-bottom:12px;">⚡ TECH STACK</div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
        """, unsafe_allow_html=True)
        for t in ["Python 3.11","Streamlit","scikit-learn","Gradient Boosting",
                  "Plotly","Pandas","NumPy"]:
            st.markdown(
                f'<span style="background:rgba(139,92,246,0.15);border:1px solid '
                f'rgba(139,92,246,0.3);border-radius:6px;padding:3px 10px;'
                f'font-size:0.73rem;color:#A78BFA;">{t}</span>',
                unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="emerald-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:12px 0 4px;font-family:'Montserrat',sans-serif;
            font-size:0.68rem;letter-spacing:0.2em;color:#334155;">
  BUILT BY <span style="color:#10B981;">SOURAV BURMAN</span> ·
  <span style="color:#F59E0B;">SALES LEAD SCORER</span> ·
  <span style="color:#8B5CF6;">GRADIENT BOOSTING · STREAMLIT · PLOTLY</span>
</div>
""", unsafe_allow_html=True)
