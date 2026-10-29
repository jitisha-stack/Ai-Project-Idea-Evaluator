import streamlit as st
import pandas as pd
import plotly.express as px
from evaluator import evaluate_idea, build_ai_analysis, generate_report_text

st.set_page_config(page_title="AI Project Idea Evaluator", page_icon="🧭", layout="wide")
st.markdown("""
<style>

.stApp {
    background: #f8fafc;
    color: #172033;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Professional title box */
.hero {
    background: linear-gradient(115deg, #111827, #075e70, #0f766e);
    padding: 30px 32px;
    border-radius: 18px;
    color: #ffffff;
    border: 1px solid #2c8791;
    box-shadow: 0 8px 24px rgba(16, 35, 63, 0.18);
    margin-bottom: 28px;
}

.hero h1 {
    color: #ffffff !important;
    font-size: 2.25rem;
    font-weight: 800;
    margin: 0 0 10px 0;
}

.hero p {
    color: #e8f5fa !important;
    font-size: 1.125rem;
    margin: 0;
}

/* Dark, readable sidebar */
section[data-testid="stSidebar"] {
    background: #1E1B2E;
    border-right: 1px solid #263d59;
}

section[data-testid="stSidebar"] * {
    color: #f1f5f9;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 750;
}

section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #cbd5e1 !important;
}

/* Main headings */
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #14243b !important;
    font-weight: 950;
}

/* Form labels and normal text */
.stApp label,
.stApp [data-testid="stMarkdownContainer"] p {
    color: #26364d;
}

/* Input fields */
.stApp input,
.stApp textarea {
    color: #172033 !important;
    background: #ffffff !important;
    border: 3px solid #a9b8ca !important;
    border-radius: 8px !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #d5dfeb;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 4px 12px rgba(15, 35, 60, 0.07);
}

div[data-testid="stMetricLabel"] {
    color: #475569 !important;
}

div[data-testid="stMetricValue"] {
    color: #10233f !important;
    font-weight: 800;
}

/* Primary buttons */
.stApp button[kind="primary"],
.stApp button[data-testid="stFormSubmitButton"] {
    background: #087f8c;
    color: #ffffff !important;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}

.stApp button[kind="primary"]:hover {
    background: #066570;
    border: none;
}

/* More readable form controls */
.stApp [data-baseweb="select"] > div {
    border-radius: 8px;
}

.stApp [data-testid="stSlider"] {
    padding-top: 6px;
}
</style>
<div class="hero"><h1> 🧭 AI Project Idea Evaluator</h1>
<p>Evaluate feasibility, cost, risk, data readiness and delivery options before building.</p></div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Evaluation settings")
    use_ai = st.toggle("Use AI explanation (optional)", value=False)
    st.caption(" Rule-based scoring works without an API key. AI explanations are optional.")
    st.divider()
    st.markdown("**Six pillars**")
    st.caption("Finance · Risk & Safety · Team · Data · Build vs Buy · Maintenance")
    st.caption("Scores are estimates, not guarantees.")

st.subheader("-> Describe your idea")
with st.form("idea_form"):
    c1, c2 = st.columns(2)
    with c1:
        idea_name = st.text_input("Project name", "AI College Attendance Predictor")
        problem = st.text_area("What problem will it solve?",
            "Help college staff identify attendance patterns early and alert students at risk of low attendance.", height=100)
        users = st.text_input("Who will use it?", "Students and college administrators")
        budget = st.number_input("Estimated initial budget (₹)", min_value=0, value=50000, step=5000)
        annual_benefit = st.number_input("Estimated annual savings or revenue (₹)", min_value=0, value=120000, step=10000)
    with c2:
        build_weeks = st.slider("Estimated build time (weeks)", 1, 52, 6)
        data_quality = st.slider("Data readiness (1 = poor, 5 = excellent)", 1, 5, 3)
        team_readiness = st.slider("Team and stakeholder readiness (1–5)", 1, 5, 3)
        maintenance_readiness = st.slider("Post-launch monitoring plan (1–5)", 1, 5, 3)
        risk_level = st.selectbox("Impact if AI is wrong", ["Low", "Medium", "High", "Critical"], index=1)
        sensitive_data = st.checkbox("Uses personal or sensitive data", value=True)
        build_or_buy = st.radio("Preferred approach", ["Not sure", "Build custom", "Buy/use existing tool"])
    submitted = st.form_submit_button("Evaluate project", type="primary", use_container_width=True)

if submitted:
    st.success("Button clicked! Idea Evaluated. ^_^")
    idea = {"name": idea_name.strip() or "Untitled idea", "problem": problem.strip(), "users": users.strip(),
            "budget": float(budget), "annual_benefit": float(annual_benefit), "build_weeks": int(build_weeks),
            "data_quality": int(data_quality), "team_readiness": int(team_readiness),
            "maintenance_readiness": int(maintenance_readiness), "risk_level": risk_level,
            "sensitive_data": sensitive_data, "build_or_buy": build_or_buy}
    result = evaluate_idea(idea)
    ai_text = None
    if use_ai:
        with st.spinner("Preparing an AI-assisted explanation..."):
            ai_text = build_ai_analysis(idea, result)

    st.divider()
    st.subheader("2. Evaluation results")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Feasibility score", f"{result['score']}/100")
    m2.metric("Annual benefit − budget", f"₹{result['net_benefit']:,.0f}")
    m3.metric("Simple payback", result["payback"])
    m4.metric("Recommendation", result["verdict"])

    left, right = st.columns(2)
    with left:
        st.markdown("#### Score by pillar")
        chart_df = pd.DataFrame({"Pillar": list(result["pillar_scores"].keys()), "Score": list(result["pillar_scores"].values())})
        fig = px.bar(chart_df, x="Pillar", y="Score", range_y=[0,100],
                     color="Score", color_continuous_scale=["#f59e0b","#0d9488","#2563eb"])
        fig.update_layout(showlegend=False,plot_bgcolor="#ffffff",paper_bgcolor="#ffffff",
                          font=dict(family="Arial",size=13,color="#172033"),
                          title_font=dict(size=18, color="#10233f"),xaxis=dict(title_font=dict(color="#10233f", size=14),
                                                                               tickfont=dict(color="#26364d", size=11),showgrid=False),yaxis=dict(
        title_font=dict(color="#10233f", size=14),
        tickfont=dict(color="#26364d", size=12),gridcolor="#dbe4ee",zerolinecolor="#94a3b8"),margin=dict(l=15, r=15, t=25, b=20))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown("#### Estimated cost-benefit")
        cost_df = pd.DataFrame({"Measure":["Initial budget","Annual benefit","Annual benefit − budget"],
                                "Amount (₹)":[idea["budget"],idea["annual_benefit"],result["net_benefit"]]})
        fig2 = px.bar(cost_df, x="Measure", y="Amount (₹)", color="Measure",
                      color_discrete_sequence=["#2563eb","#0d9488","#f59e0b"])
        fig2.update_layout(showlegend=False,
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(
        family="Arial",
        size=13,
        color="#172033"
    ),
    xaxis=dict(
        title_font=dict(color="#10233f", size=14),
        tickfont=dict(color="#26364d", size=11),
        showgrid=False
    ),
    yaxis=dict(
        title_font=dict(color="#10233f", size=14),
        tickfont=dict(color="#26364d", size=12),
        gridcolor="#dbe4ee",
        zerolinecolor="#94a3b8"
    ),
    margin=dict(l=15, r=15, t=25, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Key findings")
    for item in result["strengths"]: st.success(item)
    for item in result["concerns"]: st.warning(item)
    st.markdown("#### Suggested next steps")
    for i, item in enumerate(result["next_steps"], 1): st.write(f"{i}. {item}")
    st.markdown("#### Build vs Buy guidance")
    st.info(result["build_buy_advice"])
    if ai_text:
        st.markdown("#### AI-assisted explanation")
        st.write(ai_text)
    st.download_button("⬇️ Download evaluation report (.txt)", data=generate_report_text(idea,result,ai_text),
        file_name="ai_project_evaluation_report.txt", mime="text/plain", use_container_width=True)
    st.caption("Prototype only. Validate estimates with real evidence and stakeholders before making investment decisions.")
else:
    st.info("Change the example values if needed, then select **Evaluate project**.")
    st.markdown("### Example demonstration")
    st.write("The default example evaluates an AI college attendance predictor with a ₹50,000 budget and ₹1,20,000 estimated annual benefit.")
    st.write("After evaluation, the app displays the score, verdict, charts, risks, next steps and a downloadable report.")
