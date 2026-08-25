import streamlit as st
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import plotly.express as px
from src.engine import run_diagnosis
from src.audit import get_kpis, load_audit_log, log_decision
import time

# Load environment variables
load_dotenv()

# Setup page
st.set_page_config(page_title="NetSage AI | Ops", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Neo-Brutalist UI Refinement
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=Inter:wght@400;700;900&family=Space+Grotesk:wght@600;700;900&display=swap');

/* Base Styles */
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    background-color: #F4F1DE; 
    color: #111111;
}

/* Hide default streamlit header */
header[data-testid="stHeader"] {
    display: none;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    text-transform: uppercase;
    font-weight: 900 !important;
    color: #111111 !important;
}

/* Header */
.brutalist-header {
    background-color: #FFDE00;
    border: 4px solid #111111;
    box-shadow: 8px 8px 0px #111111;
    padding: 30px;
    margin-top: 20px;
    margin-bottom: 50px;
    position: relative;
    background-image: radial-gradient(#111111 1px, transparent 1px);
    background-size: 20px 20px;
}
.brutalist-header-inner {
    background-color: #FFDE00;
    padding: 10px;
    display: inline-block;
    border: 4px solid #111111;
}
.brutalist-header h1 {
    font-size: 4.5rem !important;
    margin: 0;
    line-height: 1;
    letter-spacing: -2px;
}
.brutalist-header p {
    font-size: 1.5rem;
    font-weight: 900;
    margin-top: 10px;
    margin-bottom: 0;
    letter-spacing: 2px;
}

/* Micro Labels */
.micro-label {
    background-color: #111111;
    color: #FFFFFF;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 4px 10px;
    display: inline-block;
    border: 2px solid #111111;
    text-transform: uppercase;
}
.micro-label.success { background-color: #39FF88; color: #111111; }
.micro-label.warning { background-color: #FFDE00; color: #111111; }
.micro-label.danger { background-color: #FF3B30; color: #FFFFFF; }
.micro-label.info { background-color: #FFFFFF; color: #111111; }

/* Section Divider */
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 900;
    border-bottom: 6px solid #111111;
    margin-bottom: 30px;
    padding-bottom: 5px;
    margin-top: 70px;
    text-transform: uppercase;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}
.section-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.2rem;
    background: #111111;
    color: #FFFFFF;
    padding: 2px 10px;
    margin-right: 15px;
    position: relative;
    top: -4px;
}

/* Metric Blocks / KPIs */
.kpi-container {
    display: flex;
    gap: 25px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}
.kpi-card {
    background-color: #FFFFFF;
    border: 4px solid #111111;
    box-shadow: 8px 8px 0px #111111;
    padding: 20px;
    flex: 1;
    min-width: 220px;
    position: relative;
}
.kpi-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1rem;
    font-weight: 700;
    border-bottom: 3px solid #111111;
    padding-bottom: 8px;
    margin-bottom: 15px;
    text-transform: uppercase;
}
.kpi-value {
    font-size: 4rem;
    font-weight: 900;
    font-family: 'Space Grotesk', sans-serif;
    line-height: 1;
}

/* General Cards */
.brutalist-card {
    background-color: #FFFFFF;
    border: 4px solid #111111;
    box-shadow: 8px 8px 0px #111111;
    padding: 30px;
    margin-bottom: 30px;
    position: relative;
    margin-top: 20px;
}
.brutalist-card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.2rem;
    font-weight: 900;
    background-color: #FFDE00;
    padding: 8px 15px;
    border: 3px solid #111111;
    position: absolute;
    top: -20px;
    left: -4px;
    box-shadow: 4px 4px 0px #111111;
    text-transform: uppercase;
}

/* CLI Output */
.cli-output {
    background-color: #111111;
    color: #39FF88;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    padding: 20px;
    border: 4px solid #111111;
    white-space: pre-wrap;
    box-shadow: inset 0px 0px 20px rgba(0,0,0,1);
    font-size: 1rem;
    margin-top: 10px;
    line-height: 1.5;
}

/* Selectbox styling */
.stSelectbox label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: #111111 !important;
    text-transform: uppercase !important;
    background: #FFDE00;
    padding: 2px 8px;
    border: 2px solid #111111;
    display: inline-block;
    margin-bottom: 10px;
}
div[data-baseweb="select"] > div {
    border: 4px solid #111111 !important;
    border-radius: 0 !important;
    box-shadow: 6px 6px 0px #111111 !important;
    background-color: #FFFFFF !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.4rem !important;
}

/* Pipeline visualization */
.pipeline-box {
    text-align: center; 
    margin: 60px 0; 
    font-family: 'Space Grotesk', sans-serif; 
    font-weight: 900; 
    font-size: 1.6rem; 
    background: #111111; 
    color: #FFFFFF;
    border: 4px solid #111111; 
    padding: 25px; 
    box-shadow: 8px 8px 0px #FF5C35;
    letter-spacing: 4px;
}
.pipeline-arrow {
    color: #FF5C35;
    margin: 0 15px;
}

/* Buttons */
div.stButton > button {
    background-color: #FFFFFF !important;
    color: #111111 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 900 !important;
    font-size: 1.4rem !important;
    text-transform: uppercase !important;
    border: 4px solid #111111 !important;
    box-shadow: 6px 6px 0px #111111 !important;
    border-radius: 0 !important;
    padding: 15px 30px !important;
    transition: transform 0.1s, box-shadow 0.1s !important;
    width: 100%;
}
div.stButton > button:active {
    box-shadow: 0px 0px 0px #111111 !important;
    transform: translate(6px, 6px) !important;
}

/* Form Styles */
.stTextArea label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
}
.stTextArea textarea {
    border: 4px solid #111111 !important;
    border-radius: 0 !important;
    box-shadow: inset 4px 4px 0px rgba(0,0,0,0.05) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.1rem !important;
}

/* Table styles for Audit Log */
table.audit-table {
    width: 100%;
    border-collapse: collapse;
    border: 4px solid #111111;
    background-color: #FFFFFF;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.95rem;
}
table.audit-table th {
    background-color: #111111;
    color: #FFFFFF;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    padding: 15px;
    text-align: left;
    border: 3px solid #111111;
    text-transform: uppercase;
}
table.audit-table td {
    padding: 15px;
    border: 3px solid #111111;
    font-weight: 600;
    vertical-align: top;
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
@st.cache_data
def load_data():
    try:
        data_path = Path(__file__).parent.parent / "data" / "cases.csv"
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        st.error(f"Failed to load cases.csv: {e}")
        return pd.DataFrame()

df = load_data()
kpis = get_kpis()
audit_log = load_audit_log()

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("""
<div class="brutalist-header">
    <div class="brutalist-header-inner">
        <h1>NETSAGE AI</h1>
        <p>NETWORK DIAGNOSTIC SYSTEM</p>
    </div>
    <div style="display: flex; gap: 15px; margin-top: 25px; flex-wrap: wrap;">
        <span class="micro-label success">SYSTEM // ONLINE</span>
        <span class="micro-label info">AI + RULE ENGINE + HUMAN REVIEW</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not df.empty:
    # ---------------------------------------------------------
    # 01 // KPI METRICS
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span class="section-num">[01]</span> KPI METRICS <span class="micro-label" style="font-size: 0.8rem; background: transparent; color: #111111; margin-left: auto;">REALTIME</span></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-title">TOTAL CASES</div>
            <div class="kpi-value">{kpis['total']}</div>
        </div>
        <div class="kpi-card" style="background-color: #FF5C35;">
            <div class="kpi-title">HIGH SEVERITY</div>
            <div class="kpi-value">{len(df[df['severity'] == 'HIGH'])}</div>
        </div>
        <div class="kpi-card" style="background-color: #5B5BFF; color: #FFFFFF;">
            <div class="kpi-title" style="border-color: #FFFFFF;">AI AGREEMENT</div>
            <div class="kpi-value">{kpis['agreement_percent']}%</div>
        </div>
        <div class="kpi-card" style="background-color: #FFDE00;">
            <div class="kpi-title">HUMAN OVERRIDES</div>
            <div class="kpi-value">{kpis['overrides']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 02 // CASE EXPLORER
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span class="section-num">[02]</span> CASE EXPLORER <span class="micro-label" style="font-size: 0.8rem; background: transparent; color: #111111; margin-left: auto;">PACKET TRACER</span></div>', unsafe_allow_html=True)
    
    case_options = df['case_id'].tolist()
    selected_case_id = st.selectbox("ACTIVE CASE SELECTION", case_options)
    selected_case = df[df['case_id'] == selected_case_id].iloc[0]
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown(f"""
        <div class="brutalist-card" style="margin-top: 30px; height: calc(100% - 30px);">
            <div class="brutalist-card-title">CASE DETAILS</div>
            <div style="margin-top: 15px;">
                <span class="micro-label info" style="margin-bottom: 10px;">SYMPTOM</span>
                <p style="font-size: 1.4rem; font-weight: 900; margin-bottom: 25px;">{selected_case['symptom']}</p>
                
                <span class="micro-label info" style="margin-bottom: 10px;">TOPOLOGY</span>
                <p style="font-size: 1.1rem; font-weight: 600; margin-bottom: 25px; font-family: 'IBM Plex Mono', monospace;">{selected_case['topology_note']}</p>
                
                <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                    <div style="background: #111111; color: #FFFFFF; padding: 10px 15px; border: 3px solid #111111; font-family: 'IBM Plex Mono', monospace; font-weight: 700;">
                        SEV: <span style="color: #FF3B30;">{selected_case['severity']}</span>
                    </div>
                    <div style="background: #FFFFFF; color: #111111; padding: 10px 15px; border: 3px solid #111111; font-family: 'IBM Plex Mono', monospace; font-weight: 700;">
                        TAG: {selected_case['concept_tag']}
                    </div>
                    <div style="background: #FFFFFF; color: #111111; padding: 10px 15px; border: 3px solid #111111; font-family: 'IBM Plex Mono', monospace; font-weight: 700;">
                        OSI: {selected_case['osi_layer']}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="brutalist-card" style="margin-top: 30px; height: calc(100% - 30px); border-color: #111111;">
            <div class="brutalist-card-title" style="background-color: #111111; color: #FFFFFF;">EVIDENCE // RAW CLI</div>
            <div class="cli-output" style="height: calc(100% - 50px); overflow-y: auto;">{selected_case['show_command_output']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    # ---------------------------------------------------------
    # PIPELINE VISUALIZATION
    # ---------------------------------------------------------
    st.markdown("""
    <div class="pipeline-box">
        INPUT <span class="pipeline-arrow">&rarr;</span> RULE CHECK <span class="pipeline-arrow">&rarr;</span> AI <span class="pipeline-arrow">&rarr;</span> HUMAN <span class="pipeline-arrow">&rarr;</span> AUDIT
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # RUN DIAGNOSTICS
    # ---------------------------------------------------------
    diagnosis_results = run_diagnosis(selected_case.to_dict())
    checker_result = diagnosis_results['checker_result']
    ai_result = diagnosis_results['ai_result']
    
    # ---------------------------------------------------------
    # 03 // RULE CHECKER SECTION
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span class="section-num">[03]</span> RULE CHECKER <span class="micro-label" style="font-size: 0.8rem; background: transparent; color: #111111; margin-left: auto;">ENGINE // DETERMINISTIC</span></div>', unsafe_allow_html=True)

    status_colors = {
        "PASS": "#39FF88",
        "WARNING": "#FFDE00",
        "ERRORS_DETECTED": "#FF3B30"
    }
    
    c_status = checker_result["status"]
    bg_color = status_colors.get(c_status, "#FFFFFF")
    text_color = "#FFFFFF" if c_status == "ERRORS_DETECTED" else "#111111"
    status_display = "ERROR DETECTED" if c_status == "ERRORS_DETECTED" else c_status
    
    st.markdown(f"""
    <div class="brutalist-card" style="border-color: {bg_color}; border-width: 5px;">
        <div class="brutalist-card-title" style="background-color: {bg_color}; color: {text_color}; border-color: {bg_color};">RULE CHECKER</div>
        <div style="margin-top: 15px;">
            <span class="micro-label info">STATUS</span>
            <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 900; color: {bg_color}; font-size: 3rem; margin-bottom: 30px; text-transform: uppercase; line-height: 1; margin-top: 10px; text-shadow: 2px 2px 0px #111111;">
                {status_display}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if checker_result["findings"]:
        for finding in checker_result["findings"]:
            finding_color = status_colors.get("ERRORS_DETECTED") if finding["severity"] in ["HIGH", "CRITICAL"] else status_colors.get("WARNING")
            finding_status = "ERROR DETECTED" if finding["severity"] in ["HIGH", "CRITICAL"] else "WARNING"
            st.markdown(f"""
            <div style="border: 4px solid #111111; padding: 30px; margin-bottom: 25px; background-color: #F4F1DE; box-shadow: 8px 8px 0px #111111;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid #111111; padding-bottom: 15px; margin-bottom: 25px;">
                    <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 900; font-size: 1.6rem; text-transform: uppercase;">
                        RULE // {finding['rule_id']}
                    </div>
                    <div style="font-family: 'IBM Plex Mono', monospace; font-weight: 700; font-size: 1.1rem; background: #111111; color: #FFFFFF; padding: 4px 12px; text-transform: uppercase;">
                        {finding['type'].replace('_', ' ')}
                    </div>
                </div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 900; color: {finding_color}; font-size: 1.4rem; margin-bottom: 25px; background-color: #111111; display: inline-block; padding: 6px 18px; text-shadow: 1px 1px 0px #000;">
                    {finding_status}
                </div>
                <br>
                <span class="micro-label info" style="margin-bottom: 10px;">EVIDENCE</span>
                <div class="cli-output" style="margin-bottom: 25px;">{finding['evidence']}</div>
                
                <span class="micro-label info" style="margin-bottom: 10px;">RECOMMENDATION</span>
                <p style="font-family: 'IBM Plex Mono', monospace; font-size: 1.2rem; margin-top: 5px; font-weight: 700; background: #FFFFFF; padding: 20px; border: 4px solid #111111; box-shadow: inset 4px 4px 0px rgba(0,0,0,0.05);">{finding['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 04 // AI DIAGNOSIS
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span class="section-num">[04]</span> AI DIAGNOSIS <span class="micro-label" style="font-size: 0.8rem; background: transparent; color: #111111; margin-left: auto;">AI // GEMINI</span></div>', unsafe_allow_html=True)

    demo_tag = ""
    if ai_result.get("is_demo"):
        demo_tag = """<span class="micro-label warning" style="margin-bottom: 25px; font-size: 1.1rem;">MODE // DEMO SIMULATION</span>"""

    evidence_html = "".join([f"<li style='margin-bottom: 10px;'>{ev}</li>" for ev in ai_result.get("evidence", [])])
    next_cmd_html = "<br>".join(ai_result.get("next_command", []))
    fix_steps_html = "<br>".join(ai_result.get("fix_steps", []))

    st.markdown(f"""
    <div class="brutalist-card" style="background-color: #F4F1DE; border-width: 5px;">
        <div class="brutalist-card-title" style="background-color: #5B5BFF; color: #FFFFFF; border-color: #5B5BFF;">AI DIAGNOSIS</div>
        <div style="margin-top: 15px;">{demo_tag}</div>
        
        <div style="display: flex; gap: 25px; flex-wrap: wrap; margin-bottom: 35px;">
            <div style="border: 4px solid #111111; padding: 25px; background: #FFFFFF; flex: 2; min-width: 250px; box-shadow: 8px 8px 0px #111111;">
                <span class="micro-label info">ROOT CAUSE</span>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; font-weight: 900; margin-top: 15px;">{ai_result.get("root_cause", "N/A")}</div>
            </div>
            <div style="border: 4px solid #111111; padding: 25px; background: #FFFFFF; flex: 1; min-width: 150px; box-shadow: 8px 8px 0px #111111;">
                <span class="micro-label info">OSI LAYER</span>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; font-weight: 900; margin-top: 15px;">{ai_result.get("osi_layer", "N/A")}</div>
            </div>
            <div style="border: 4px solid #111111; padding: 25px; background: #111111; color: #FFFFFF; flex: 1; min-width: 150px; box-shadow: 8px 8px 0px #5B5BFF;">
                <span class="micro-label info">CONFIDENCE</span>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 3rem; font-weight: 900; color: #39FF88; margin-top: 15px; line-height: 1;">{ai_result.get("confidence", 0)}%</div>
            </div>
        </div>
        
        <div style="background: #FFFFFF; border: 4px solid #111111; padding: 30px; margin-bottom: 35px; box-shadow: 8px 8px 0px #111111;">
            <span class="micro-label info">EVIDENCE // VERIFIED</span>
            <ul style="font-family: 'IBM Plex Mono', monospace; font-size: 1.2rem; margin-top: 20px; font-weight: 600;">
                {evidence_html}
            </ul>
        </div>
        
        <div style="background: #FFFFFF; border: 4px solid #111111; padding: 30px; margin-bottom: 35px; box-shadow: 8px 8px 0px #111111;">
            <span class="micro-label info">NEXT COMMAND</span>
            <div class="cli-output" style="margin-top: 15px;">{next_cmd_html}</div>
        </div>
        
        <div style="background: #FFDE00; border: 4px solid #111111; padding: 30px; box-shadow: 8px 8px 0px #111111;">
            <span class="micro-label danger" style="font-size: 1.2rem;">REVIEW // REQUIRED</span>
            <div class="cli-output" style="margin-top: 20px; background: #FFFFFF; color: #111111; box-shadow: inset 4px 4px 0px rgba(0,0,0,0.05); border-color: #111111;">{fix_steps_html}</div>
            <p style="font-family: 'Inter', sans-serif; font-weight: 900; font-size: 1.1rem; margin-top: 20px; margin-bottom: 0;"><em>{ai_result.get("safety_note", "")}</em></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 05 // HUMAN REVIEW GATE
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span class="section-num">[05]</span> HUMAN REVIEW GATE <span class="micro-label" style="font-size: 0.8rem; background: transparent; color: #111111; margin-left: auto;">REVIEW // REQUIRED</span></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="brutalist-card" style="text-align: center; background-color: #111111; color: #FFFFFF; margin-top: 40px; border-width: 6px;">
        <div class="brutalist-card-title" style="background-color: #FF3B30; color: #FFFFFF; border-color: #FF3B30;">HUMAN REVIEW</div>
        <h2 style="color: #FFFFFF !important; font-size: 3.5rem; margin-top: 30px; letter-spacing: -1px;">AI HAS NO FINAL AUTHORITY</h2>
        <p style="font-family: 'Space Grotesk', sans-serif; color: #FFDE00; font-size: 1.4rem; font-weight: 700; margin-bottom: 30px; border-top: 2px solid #FFDE00; border-bottom: 2px solid #FFDE00; display: inline-block; padding: 10px 0;">AI OUTPUT CANNOT BE APPLIED WITHOUT HUMAN APPROVAL</p>
    </div>
    """, unsafe_allow_html=True)
    
    state_key = f"review_state_{selected_case_id}"
    if state_key not in st.session_state:
        st.session_state[state_key] = "PENDING"
        
    current_state = st.session_state[state_key]
    
    if current_state == "PENDING":
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("APPROVE", key=f"btn_approve_{selected_case_id}"):
                log_decision(selected_case_id, ai_result, checker_result, "APPROVE")
                st.session_state[state_key] = "APPROVED"
                st.rerun()
        with col_btn2:
            if st.button("EDIT", key=f"btn_edit_{selected_case_id}"):
                st.session_state[state_key] = "EDITING"
                st.rerun()
        with col_btn3:
            if st.button("REJECT", key=f"btn_reject_{selected_case_id}"):
                st.session_state[state_key] = "REJECTING"
                st.rerun()
                
    elif current_state == "EDITING":
        st.markdown('<div class="brutalist-card" style="border-color: #FFDE00; border-width: 5px;">', unsafe_allow_html=True)
        st.markdown('<span class="micro-label info" style="margin-bottom: 20px;">EDIT DIAGNOSIS</span>', unsafe_allow_html=True)
        with st.form(key=f"edit_form_{selected_case_id}"):
            new_root_cause = st.text_area("ROOT CAUSE", value=ai_result.get("root_cause", ""))
            new_next_cmd = st.text_area("NEXT COMMAND (One per line)", value="\\n".join(ai_result.get("next_command", [])))
            new_fix_steps = st.text_area("FIX STEPS (One per line)", value="\\n".join(ai_result.get("fix_steps", [])))
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("SUBMIT EDIT"):
                edited_res = {
                    "root_cause": new_root_cause,
                    "next_command": [cmd.strip() for cmd in new_next_cmd.split("\\n") if cmd.strip()],
                    "fix_steps": [step.strip() for step in new_fix_steps.split("\\n") if step.strip()]
                }
                log_decision(selected_case_id, ai_result, checker_result, "EDIT", edited_diagnosis=edited_res)
                st.session_state[state_key] = "EDITED"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif current_state == "REJECTING":
        st.markdown('<div class="brutalist-card" style="border-color: #FF3B30; border-width: 5px;">', unsafe_allow_html=True)
        st.markdown('<span class="micro-label danger" style="margin-bottom: 20px;">REJECT DIAGNOSIS</span>', unsafe_allow_html=True)
        with st.form(key=f"reject_form_{selected_case_id}"):
            comment = st.text_area("REVIEWER COMMENT (Required to override AI)", placeholder="Explain why the AI diagnosis is incorrect...")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("SUBMIT REJECT"):
                if comment.strip():
                    log_decision(selected_case_id, ai_result, checker_result, "REJECT", reviewer_comment=comment)
                    st.session_state[state_key] = "REJECTED"
                    st.rerun()
                else:
                    st.error("A reviewer comment is required to reject a diagnosis.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif current_state == "APPROVED":
        st.markdown('<div style="background-color: #39FF88; border: 5px solid #111111; padding: 30px; font-family: Space Grotesk; font-weight: 900; font-size: 2.2rem; text-align: center; box-shadow: 8px 8px 0px #111111; margin-top: 40px; text-transform: uppercase;">APPROVED // HUMAN VERIFIED</div>', unsafe_allow_html=True)
        
    elif current_state == "EDITED":
        st.markdown('<div style="background-color: #FFDE00; border: 5px solid #111111; padding: 30px; font-family: Space Grotesk; font-weight: 900; font-size: 2.2rem; text-align: center; box-shadow: 8px 8px 0px #111111; margin-top: 40px; text-transform: uppercase;">EDITED // HUMAN CORRECTION</div>', unsafe_allow_html=True)

    elif current_state == "REJECTED":
        st.markdown('<div style="background-color: #FF3B30; color: #FFFFFF; border: 5px solid #111111; padding: 30px; font-family: Space Grotesk; font-weight: 900; font-size: 2.2rem; text-align: center; box-shadow: 8px 8px 0px #111111; margin-top: 40px; text-transform: uppercase;">REJECTED // AI OVERRIDDEN</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 06 // AUDIT LOG TABLE
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span class="section-num">[06]</span> AUDIT LOG <span class="micro-label" style="font-size: 0.8rem; background: transparent; color: #111111; margin-left: auto;">AUDIT // LOGGED</span></div>', unsafe_allow_html=True)
    
    if audit_log:
        audit_records = []
        for row in sorted(audit_log, key=lambda x: x['timestamp'], reverse=True):
            audit_records.append({
                "Timestamp": row["timestamp"][:19].replace("T", " "),
                "Case": row["case_id"],
                "AI Decision": row["ai_diagnosis"].get("root_cause", "N/A"),
                "Human Decision": row["decision"],
                "Override": "YES" if row["decision"] in ["EDIT", "REJECT"] else "NO",
                "Comment": row["reviewer_comment"] if row["reviewer_comment"] else "-"
            })
        
        audit_df = pd.DataFrame(audit_records)
        
        table_html = "<div style='overflow-x: auto; box-shadow: 8px 8px 0px #111111; margin-bottom: 20px;'><table class='audit-table'><thead><tr>"
        for col in audit_df.columns:
            table_html += f"<th>{col.upper()}</th>"
        table_html += "</tr></thead><tbody>"
        
        for _, row in audit_df.head(10).iterrows(): 
            table_html += "<tr>"
            for col in audit_df.columns:
                val = row[col]
                if col == "Human Decision":
                    color = "#39FF88" if val == "APPROVE" else ("#FFDE00" if val == "EDIT" else "#FF3B30")
                    table_html += f"<td><span style='background: {color}; padding: 4px 10px; font-weight: 900; font-family: Space Grotesk; color: #111111; border: 3px solid #111111;'>{val}</span></td>"
                else:
                    table_html += f"<td>{val}</td>"
            table_html += "</tr>"
        table_html += "</tbody></table></div>"
        
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.markdown("<div>No audit records found.</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 07 // ANALYTICS
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span class="section-num">[07]</span> NETWORK FAULT ANALYTICS <span class="micro-label" style="font-size: 0.8rem; background: transparent; color: #111111; margin-left: auto;">DATA // REALTIME</span></div>', unsafe_allow_html=True)
    
    def apply_brutalist_style(fig):
        fig.update_layout(
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font_family="Space Grotesk, sans-serif",
            font_color="#111111",
            title_font_size=22,
            title_font_color="#111111",
            margin=dict(l=40, r=40, t=80, b=40),
            xaxis=dict(showline=True, linewidth=4, linecolor='#111111', gridcolor='rgba(17,17,17,0.1)', mirror=True, title_font_weight="900", tickfont_weight="700"),
            yaxis=dict(showline=True, linewidth=4, linecolor='#111111', gridcolor='rgba(17,17,17,0.1)', mirror=True, title_font_weight="900", tickfont_weight="700")
        )
        return fig
    
    if audit_log:
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            sev_counts = df['severity'].value_counts().reset_index()
            sev_counts.columns = ['Severity', 'Count']
            color_map = {"CRITICAL": "#FF3B30", "HIGH": "#FF5C35", "MEDIUM": "#FFDE00", "LOW": "#39FF88"}
            
            fig1 = px.bar(sev_counts, x='Severity', y='Count', title="SEVERITY DISTRIBUTION", color='Severity', color_discrete_map=color_map)
            fig1.update_traces(marker_line_color='#111111', marker_line_width=4)
            fig1 = apply_brutalist_style(fig1)
            st.markdown('<div style="border: 4px solid #111111; box-shadow: 8px 8px 0px #111111; margin-bottom: 30px;">', unsafe_allow_html=True)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            dec_counts = pd.Series([r['decision'] for r in audit_log]).value_counts().reset_index()
            dec_counts.columns = ['Decision', 'Count']
            color_map2 = {"APPROVE": "#39FF88", "EDIT": "#FFDE00", "REJECT": "#FF3B30"}
            
            fig3 = px.pie(dec_counts, names='Decision', values='Count', title="ACCEPTED / EDITED / REJECTED", color='Decision', color_discrete_map=color_map2)
            fig3.update_traces(marker_line_color='#111111', marker_line_width=4, textinfo='percent+label', textfont_weight="900")
            fig3 = apply_brutalist_style(fig3)
            fig3.update_layout(xaxis=dict(showline=False), yaxis=dict(showline=False))
            st.markdown('<div style="border: 4px solid #111111; box-shadow: 8px 8px 0px #111111; margin-bottom: 30px;">', unsafe_allow_html=True)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_c2:
            concept_counts = df['concept_tag'].value_counts().reset_index()
            concept_counts.columns = ['Concept', 'Count']
            fig2 = px.bar(concept_counts, y='Concept', x='Count', orientation='h', title="CASES BY CONCEPT", color_discrete_sequence=['#5B5BFF'])
            fig2.update_traces(marker_line_color='#111111', marker_line_width=4)
            fig2 = apply_brutalist_style(fig2)
            st.markdown('<div style="border: 4px solid #111111; box-shadow: 8px 8px 0px #111111; margin-bottom: 30px;">', unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            osi_counts = df['osi_layer'].value_counts().reset_index()
            osi_counts.columns = ['OSI Layer', 'Count']
            fig4 = px.bar(osi_counts, x='OSI Layer', y='Count', title="OSI LAYER DISTRIBUTION", color_discrete_sequence=['#111111'])
            fig4.update_traces(marker_line_color='#111111', marker_line_width=4)
            fig4 = apply_brutalist_style(fig4)
            st.markdown('<div style="border: 4px solid #111111; box-shadow: 8px 8px 0px #111111; margin-bottom: 30px;">', unsafe_allow_html=True)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("No cases found in data/cases.csv")
