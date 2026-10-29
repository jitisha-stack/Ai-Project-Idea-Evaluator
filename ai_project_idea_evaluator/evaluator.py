import os
import json
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

load_dotenv()

PILLAR_WEIGHTS = {
    "Financial fit": 20, "Risk & safety": 20, "Team readiness": 15,
    "Data readiness": 20, "Build vs buy": 10, "Post-launch plan": 15
}

def scale_1_to_5(value):
    return round((value - 1) / 4 * 100)

def evaluate_idea(idea):
    """Transparent educational scoring rules; not a validated industry standard."""
    budget = max(float(idea.get("budget", 0)), 0)
    benefit = max(float(idea.get("annual_benefit", 0)), 0)
    risk = idea.get("risk_level", "Medium")
    sensitive = bool(idea.get("sensitive_data", False))
    data_score = scale_1_to_5(int(idea.get("data_quality", 3)))
    team_score = scale_1_to_5(int(idea.get("team_readiness", 3)))
    maintenance_score = scale_1_to_5(int(idea.get("maintenance_readiness", 3)))

    if budget == 0 and benefit > 0: financial_score = 100
    elif budget == 0 and benefit == 0: financial_score = 40
    else: financial_score = min(100, max(10, round((benefit / budget) * 40)))

    penalties = {"Low": 0, "Medium": 15, "High": 30, "Critical": 45}
    risk_score = 100 - penalties.get(risk, 15)
    if sensitive: risk_score = max(0, risk_score - 15)

    approach = idea.get("build_or_buy", "Not sure")
    build_buy_score = 85 if approach == "Buy/use existing tool" else 65 if approach == "Build custom" else 75
    pillars = {"Financial fit": financial_score, "Risk & safety": risk_score, "Team readiness": team_score,
               "Data readiness": data_score, "Build vs buy": build_buy_score, "Post-launch plan": maintenance_score}
    score = round(sum(pillars[k] * PILLAR_WEIGHTS[k] for k in PILLAR_WEIGHTS) / sum(PILLAR_WEIGHTS.values()))
    net_benefit = benefit - budget

    if budget <= 0: payback = "Not calculable"
    elif benefit <= 0: payback = "No payback estimated"
    else: payback = f"{budget / benefit * 12:.1f} months"

    verdict = "Proceed to pilot" if score >= 75 else "Improve first" if score >= 55 else "Pause and reassess"
    strengths, concerns, next_steps = [], [], []
    if benefit > budget: strengths.append("Stated annual benefit exceeds the stated initial budget.")
    else: concerns.append("Stated annual benefit does not exceed the initial budget; revisit the business case.")
    if data_score >= 75: strengths.append("Data readiness is rated relatively high.")
    else:
        concerns.append("Check data access, quality, permissions and representative coverage.")
        next_steps.append("Audit missing values, duplicates, labels, permissions and bias.")
    if team_score >= 75: strengths.append("Team readiness is rated relatively high.")
    else:
        concerns.append("Stakeholder readiness may slow delivery.")
        next_steps.append("Confirm a project owner and align Engineering, users, IT, Finance and Legal as needed.")
    if risk in ("High", "Critical"):
        concerns.append(f"Impact if wrong is {risk.lower()}; stronger testing and human review are needed.")
        next_steps.append("Test failure cases and define when a human must review or override output.")
    if sensitive:
        concerns.append("Personal or sensitive data is involved; privacy and access controls need explicit review.")
        next_steps.append("Minimise personal data, restrict access, define retention and review applicable policies.")
    if maintenance_score < 75:
        next_steps.append("Define monitoring, incident escalation, periodic review and a named human owner.")
    if int(idea.get("build_weeks", 6)) > 12:
        concerns.append("Estimated build time exceeds 12 weeks; validate scope and consider a smaller MVP.")
    if not next_steps: next_steps.append("Run a small pilot with measurable success criteria before scaling.")

    if approach == "Buy/use existing tool":
        advice = "Start with a limited existing-tool/API pilot; verify data handling, integrations, recurring fees and vendor lock-in."
    elif approach == "Build custom":
        advice = "Build custom only if privacy, integration, customization or differentiation justify the added cost and maintenance."
    else:
        advice = "Compare one existing tool/API with a small custom prototype using the same test cases, total cost and timeline."

    return {"score": int(score), "verdict": verdict, "pillar_scores": pillars, "net_benefit": net_benefit,
            "payback": payback, "strengths": strengths, "concerns": concerns, "next_steps": next_steps,
            "build_buy_advice": advice}




def build_ai_analysis(idea, result):
    """Optional AI layer. Rule-based results remain available if AI is not configured."""
    api_key = os.getenv("GROQ_API_KEY")

    try:
        api_key = api_key or st.secrets["GROQ_API_KEY"]
    except (AttributeError, KeyError, FileNotFoundError):
        pass
    try:
        from openai import OpenAI
        client = OpenAI(api_key= api_key, 
            base_url="https://api.groq.com/openai/v1")
        
        payload = {"idea": idea, "rule_based_result": result,
                   
            "instructions": ["Explain results in plain language for a student team.",
            "Do not invent market facts, quotes or performance data.",
            "Label the score as a prototype estimate, not objective truth.",
            "Give three specific questions to validate with stakeholders.",
            "Discuss privacy, security, fairness and human oversight when relevant.",
            "Keep the answer under 350 words."]}
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b", 
            messages=[{"role": "system","content": ("You are a cautious AI project feasibility reviewer. ""Distinguish facts from assumptions.")
                       },
                       {
                           "role": "user",
                           "content": json.dumps(payload, ensure_ascii=False)
                           }
                    ],
                    max_tokens=700,temperature=0.3)
        return response.choices[0].message.content
    except Exception as exc:
        return ("AI explanation could not be generated. Check API key, internet connection, model access and packages. "
                f"Rule-based results are still available. Technical detail: {type(exc).__name__}: {exc}")

def generate_report_text(idea, result, ai_text=None):
    lines = ["AI PROJECT IDEA EVALUATION REPORT", "=" * 34,
             
        f"Project: {idea.get('name','Untitled idea')}", f"Problem: {idea.get('problem','')}",

        f"Target users: {idea.get('users','')}", "", f"Feasibility score: {result['score']}/100",

        f"Recommendation: {result['verdict']}", f"Annual benefit minus initial budget: ₹{result['net_benefit']:,.0f}",

        f"Simple payback estimate: {result['payback']}", "", "PILLAR SCORES"]
    
    lines += [f"- {name}: {score}/100" for name, score in result["pillar_scores"].items()]
    lines += ["", "STRENGTHS"] + [f"- {x}" for x in result["strengths"]]
    lines += ["", "CONCERNS"] + [f"- {x}" for x in result["concerns"]]
    lines += ["", "NEXT STEPS"] + [f"- {x}" for x in result["next_steps"]]
    lines += ["", "BUILD VS BUY", result["build_buy_advice"]]

    if ai_text: lines += ["", "AI-ASSISTED EXPLANATION", ai_text]
    lines += ["", "Disclaimer: Prototype decision-support output. Validate assumptions before real decisions."]
    return "\n".join(lines)
