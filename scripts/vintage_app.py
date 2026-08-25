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

# Theme state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Colors
if st.session_state.dark_mode:
    bg_app = "#1A1816"
    bg_card = "#221F1C"
    bg_alt = "#2C2824"
    border = "#38322C"
    border_dark = "#4C443C"
    text_main = "#D4C9B4"
    text_muted = "#9E9281"
    text_sub = "#B8AA96"
    heading = "#F5EAD4"
    
    b_succ_bg, b_succ_tx, b_succ_bd = "#233023", "#86B386", "#364736"
    b_warn_bg, b_warn_tx, b_warn_bd = "#3D3520", "#CCA752", "#5C5030"
    b_dang_bg, b_dang_tx, b_dang_bd = "#3D2525", "#D67474", "#5C3838"
    b_info_bg, b_info_tx, b_info_bd = "#242D33", "#7A9DB5", "#36444D"
    b_neut_bg, b_neut_tx, b_neut_bd = "#332E29", "#A39481", "#4D453D"
else:
    bg_app = "#FDFBF7"
    bg_card = "#FCFAF5"
    bg_alt = "#F0ECE1"
    border = "#E6DFD3"
    border_dark = "#D4C9B4"
    text_main = "#2C241B"
    text_muted = "#5D5041"
    text_sub = "#4A3F35"
    heading = "#1A1510"
    
    b_succ_bg, b_succ_tx, b_succ_bd = "#E6F0E6", "#3A5A3A", "#C2D6C2"
    b_warn_bg, b_warn_tx, b_warn_bd = "#FDF6E3", "#8C6B14", "#E8D5A5"
    b_dang_bg, b_dang_tx, b_dang_bd = "#F9EBEA", "#8B3A3A", "#E0C2C2"
    b_info_bg, b_info_tx, b_info_bd = "#E8F0F2", "#3A5A70", "#C2D6DC"
    b_neut_bg, b_neut_tx, b_neut_bd = "#F0ECE1", "#5D5041", "#D4C9B4"

# Custom CSS for Minimal Vintage UI
css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&family=Lora:ital,wght@0,400;0,500;0,600;1,400&display=swap');

/* Base Styles */
html, body, [class*="css"], .stApp {{
    font-family: 'Inter', sans-serif;
    background-color: {bg_app} !important; 
    color: {text_main} !important;
}}

/* Hide default streamlit header */
header[data-testid="stHeader"] {{
    display: none !important;
    background: transparent !important;
}}

/* Headings */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Lora', serif !important;
    font-weight: 500 !important;
    color: {heading} !important;
    letter-spacing: -0.01em;
}}

/* Header */
.minimal-header {{
    background-color: {bg_card};
    border-bottom: 1px solid {border};
    padding: 24px 32px;
    margin-bottom: 32px;
    margin-top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 4px;
}}
.minimal-header h1 {{
    font-size: 1.75rem !important;
    margin: 0;
    font-weight: 600;
    color: {heading};
}}
.minimal-header p {{
    font-size: 0.875rem;
    color: {text_muted};
    margin: 4px 0 0 0;
    font-family: 'Lora', serif;
    font-style: italic;
}}
.header-badges {{
    display: flex;
    gap: 12px;
    align-items: center;
}}

/* Badges / Micro Labels */
.badge {{
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 3px;
    display: inline-flex;
    align-items: center;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    border: 1px solid transparent;
}}
.badge.success {{ background-color: {b_succ_bg}; color: {b_succ_tx}; border-color: {b_succ_bd}; }}
.badge.warning {{ background-color: {b_warn_bg}; color: {b_warn_tx}; border-color: {b_warn_bd}; }}
.badge.danger {{ background-color: {b_dang_bg}; color: {b_dang_tx}; border-color: {b_dang_bd}; }}
.badge.info {{ background-color: {b_info_bg}; color: {b_info_tx}; border-color: {b_info_bd}; }}
.badge.neutral {{ background-color: {b_neut_bg}; color: {b_neut_tx}; border-color: {b_neut_bd}; }}

/* Section Divider */
.section-header {{
    font-family: 'Lora', serif;
    font-size: 1.25rem;
    font-weight: 500;
    color: {heading};
    margin-bottom: 16px;
    margin-top: 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid {border};
    padding-bottom: 8px;
}}

/* Metric Blocks / KPIs */
.kpi-container {{
    display: flex;
    gap: 20px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}}
.kpi-card {{
    background-color: {bg_card};
    border: 1px solid {border};
    border-radius: 4px;
    padding: 20px;
    flex: 1;
    min-width: 200px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}}
.kpi-title {{
    font-family: 'Lora', serif;
    font-size: 0.875rem;
    font-weight: 500;
    color: {text_muted};
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.kpi-value {{
    font-family: 'Lora', serif;
    font-size: 2.25rem;
    font-weight: 400;
    color: {heading} !important;
    line-height: 1;
}}

/* General Cards */
.minimal-card {{
    background-color: {bg_card};
    border: 1px solid {border};
    border-radius: 4px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}}
.card-header {{
    font-family: 'Lora', serif;
    font-size: 1.125rem;
    font-weight: 500;
    color: {heading};
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

/* CLI Output (Typewriter effect) */
.cli-output {{
    background-color: {bg_alt};
    color: {text_main};
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.875rem;
    padding: 16px;
    border-radius: 4px;
    border: 1px solid {border_dark};
    white-space: pre-wrap;
    line-height: 1.6;
    overflow-x: auto;
}}

/* Component Classes */
.comp-label {{
    font-size: 0.75rem; 
    color: {text_muted}; 
    font-weight: 600; 
    margin-bottom: 8px; 
    letter-spacing: 0.05em; 
    text-transform: uppercase;
}}
.comp-value {{
    font-family: 'Lora', serif; 
    font-size: 1rem; 
    color: {heading}; 
    font-weight: 500;
}}
.comp-grid-item {{
    background: {bg_alt}; 
    padding: 16px; 
    border-radius: 4px; 
    border: 1px solid {border_dark};
}}
.review-pending {{ text-align: center; border-color: {b_warn_bd}; background: {b_warn_bg}; color: {b_warn_tx}; padding: 24px; border-radius: 4px; border: 1px solid {b_warn_bd}; }}
.review-approved {{ text-align: center; border-color: {b_succ_bd}; background: {b_succ_bg}; color: {b_succ_tx}; padding: 24px; border-radius: 4px; border: 1px solid {b_succ_bd}; font-family: 'Lora', serif; font-size: 1.1rem; }}
.review-edited {{ text-align: center; border-color: {b_warn_bd}; background: {b_warn_bg}; color: {b_warn_tx}; padding: 24px; border-radius: 4px; border: 1px solid {b_warn_bd}; font-family: 'Lora', serif; font-size: 1.1rem; }}
.review-rejected {{ text-align: center; border-color: {b_dang_bd}; background: {b_dang_bg}; color: {b_dang_tx}; padding: 24px; border-radius: 4px; border: 1px solid {b_dang_bd}; font-family: 'Lora', serif; font-size: 1.1rem; }}

/* Form Styles */
.stSelectbox label, .stTextArea label, .stCheckbox label {{
    font-family: 'Lora', serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: {text_sub} !important;
    margin-bottom: 8px;
}}
div[data-baseweb="select"] > div {{
    border: 1px solid {border_dark} !important;
    border-radius: 4px !important;
    background-color: {bg_card} !important;
}}
.stTextArea textarea {{
    border: 1px solid {border_dark} !important;
    border-radius: 4px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
    background-color: {bg_card} !important;
    color: {text_main} !important;
}}
.stTextArea textarea:focus {{
    border-color: {text_muted} !important;
    box-shadow: 0 0 0 1px {text_muted} !important;
}}

/* Buttons */
div.stButton > button {{
    background-color: {bg_card} !important;
    color: {text_sub} !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    border: 1px solid {border_dark} !important;
    border-radius: 4px !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
div.stButton > button:hover {{
    background-color: {bg_alt} !important;
    border-color: {text_muted} !important;
    color: {heading} !important;
}}

/* Primary Button Override for actions */
div.stButton > button[kind="primary"] {{
    background-color: {text_muted} !important;
    color: {bg_card} !important;
    border: 1px solid {text_main} !important;
}}
div.stButton > button[kind="primary"]:hover {{
    background-color: {text_main} !important;
    color: {bg_app} !important;
}}

/* Table styles for Audit Log */
table.minimal-table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Inter', sans-serif;
    font-size: 0.875rem;
    background-color: {bg_card};
    border: 1px solid {border};
    border-radius: 4px;
    overflow: hidden;
}}
table.minimal-table th {{
    background-color: {bg_alt};
    color: {text_sub};
    font-weight: 500;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid {border_dark};
    font-family: 'Lora', serif;
}}
table.minimal-table td {{
    padding: 12px 16px;
    border-bottom: 1px solid {border};
    color: {text_main} !important;
    vertical-align: top;
}}
table.minimal-table tr:last-child td {{
    border-bottom: none;
}}
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
# HEADER WITH THEME TOGGLE
# ---------------------------------------------------------
col_theme1, col_theme2 = st.columns([9, 1])
with col_theme2:
    mode = st.toggle("🌙 Dark", value=st.session_state.dark_mode)
    if mode != st.session_state.dark_mode:
        st.session_state.dark_mode = mode
        st.rerun()

st.markdown(f"""
<div class="minimal-header">
    <div>
        <h1>NetSage AI</h1>
        <p>Network Diagnostic System // Est. 2026</p>
    </div>
    <div class="header-badges">
        <span class="badge success">System Online</span>
        <span class="badge info">AI Engine Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not df.empty:
    # ---------------------------------------------------------
    # 01 // KPI METRICS
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span>Overview</span></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-title">Total Cases</div>
            <div class="kpi-value">{kpis['total']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">High Severity</div>
            <div class="kpi-value" style="color: {b_dang_tx} !important;">{len(df[df['severity'] == 'HIGH'])}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">AI Agreement</div>
            <div class="kpi-value" style="color: {b_info_tx} !important;">{kpis['agreement_percent']}%</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Human Overrides</div>
            <div class="kpi-value" style="color: {b_warn_tx} !important;">{kpis['overrides']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 02 // CASE EXPLORER
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span>Case Explorer</span></div>', unsafe_allow_html=True)
    
    case_options = df['case_id'].tolist()
    selected_case_id = st.selectbox("Select Case", case_options)
    selected_case = df[df['case_id'] == selected_case_id].iloc[0]
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown(f"""
        <div class="minimal-card" style="height: calc(100% - 24px);">
            <div class="card-header">Case Details</div>
            <div style="margin-bottom: 20px;">
                <div class="comp-label">Symptom</div>
                <div class="comp-value">{selected_case['symptom']}</div>
            </div>
            <div style="margin-bottom: 24px;">
                <div class="comp-label">Topology</div>
                <div style="font-size: 0.875rem; color: {text_sub};">{selected_case['topology_note']}</div>
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span class="badge {'danger' if selected_case['severity'] == 'HIGH' else 'warning'}">Sev: {selected_case['severity']}</span>
                <span class="badge neutral">{selected_case['concept_tag']}</span>
                <span class="badge neutral">{selected_case['osi_layer']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="minimal-card" style="height: calc(100% - 24px); padding: 0; overflow: hidden;">
            <div class="card-header" style="padding: 16px 24px; margin-bottom: 0; border-bottom: 1px solid {border}; background: {bg_alt};">Evidence (CLI)</div>
            <div class="cli-output" style="border-radius: 0; height: calc(100% - 53px); margin: 0; border: none; background-color: {bg_card};">{selected_case['show_command_output']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    # ---------------------------------------------------------
    # RUN DIAGNOSTICS
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span>Diagnostic Engine</span></div>', unsafe_allow_html=True)
    
    if st.button("Initiate Diagnosis", type="primary", key=f"init_diag_{selected_case_id}"):
        with st.spinner("Analyzing case..."):
            st.session_state[f"diagnosis_{selected_case_id}"] = run_diagnosis(selected_case.to_dict())
            
    if f"diagnosis_{selected_case_id}" not in st.session_state:
        st.markdown(f'<div class="minimal-card" style="text-align: center; color: {text_muted}; padding: 40px; font-family: \'Lora\', serif; font-style: italic;">Select a case and click Initiate Diagnosis to begin.</div>', unsafe_allow_html=True)
    else:
        diagnosis_results = st.session_state[f"diagnosis_{selected_case_id}"]
        checker_result = diagnosis_results['checker_result']
        ai_result = diagnosis_results['ai_result']
        
        # ---------------------------------------------------------
        # 03 // RULE CHECKER SECTION
        # ---------------------------------------------------------
        c_status = checker_result["status"]
        status_display = "Errors Detected" if c_status == "ERRORS_DETECTED" else c_status.capitalize()
        status_badge = "success" if c_status == "PASS" else ("danger" if c_status == "ERRORS_DETECTED" else "warning")
        
        st.markdown(f"""
        <div class="minimal-card">
            <div class="card-header">
                Rule Checker
                <span class="badge {status_badge}">{status_display}</span>
            </div>
        """, unsafe_allow_html=True)
        
        if checker_result["findings"]:
            for finding in checker_result["findings"]:
                f_badge = "danger" if finding["severity"] in ["HIGH", "CRITICAL"] else "warning"
                st.markdown(f"""<div style="border: 1px solid {border}; border-radius: 4px; padding: 16px; margin-bottom: 16px; background-color: {bg_card};">
<div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
<span style="font-family: 'Lora', serif; font-weight: 600; font-size: 0.95rem; color: {heading};">Rule {finding['rule_id']}</span>
<span class="badge {f_badge}">{finding['type'].replace('_', ' ')}</span>
</div>
<div style="margin-bottom: 12px;">
<div class="comp-label">Evidence</div>
<div class="cli-output" style="padding: 10px; font-size: 0.75rem; background-color: {bg_app};">{finding['evidence']}</div>
</div>
<div>
<div class="comp-label">Recommendation</div>
<div style="font-size: 0.875rem; color: {text_main};">{finding['recommendation']}</div>
</div>
</div>""", unsafe_allow_html=True)
                
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # 04 // AI DIAGNOSIS
        # ---------------------------------------------------------
        demo_tag = """<span class="badge warning">Simulation Mode</span>""" if ai_result.get("is_demo") else ""
        evidence_html = "".join([f"<li style='margin-bottom: 6px;'>{ev}</li>" for ev in ai_result.get("evidence", [])])
        next_cmd_html = "<br>".join(ai_result.get("next_command", []))
        fix_steps_html = "<br>".join(ai_result.get("fix_steps", []))

        st.markdown(f"""<div class="minimal-card">
<div class="card-header">
AI Diagnosis
{demo_tag}
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;">
<div class="comp-grid-item">
<div class="comp-label">Root Cause</div>
<div class="comp-value">{ai_result.get("root_cause", "N/A")}</div>
</div>
<div class="comp-grid-item">
<div class="comp-label">OSI Layer</div>
<div class="comp-value">{ai_result.get("osi_layer", "N/A")}</div>
</div>
<div class="comp-grid-item" style="background: {b_info_bg}; border-color: {b_info_bd};">
<div class="comp-label" style="color: {b_info_tx};">Confidence</div>
<div class="comp-value" style="font-size: 1.5rem; color: {b_info_tx};">{ai_result.get("confidence", 0)}%</div>
</div>
</div>
<div style="margin-bottom: 20px;">
<div class="comp-label">Verified Evidence</div>
<ul style="font-size: 0.875rem; color: {text_main}; margin: 0; padding-left: 20px; font-family: 'Lora', serif;">
{evidence_html}
</ul>
</div>
<div style="margin-bottom: 20px;">
<div class="comp-label">Next Commands</div>
<div class="cli-output" style="padding: 12px; font-size: 0.875rem;">{next_cmd_html}</div>
</div>
<div style="background: {b_dang_bg}; border: 1px solid {b_dang_bd}; padding: 16px; border-radius: 4px;">
<div class="comp-label" style="color: {b_dang_tx}; margin-bottom: 12px;">Proposed Remediation</div>
<div class="cli-output" style="background: {bg_card}; color: {text_main}; border: 1px solid {b_dang_bd}; padding: 12px; font-size: 0.875rem; margin-bottom: 12px;">{fix_steps_html}</div>
<div style="font-size: 0.8rem; color: {b_dang_tx}; font-family: 'Lora', serif; font-style: italic;">{ai_result.get("safety_note", "")}</div>
</div>
</div>""", unsafe_allow_html=True)

        # ---------------------------------------------------------
        # 05 // HUMAN REVIEW GATE
        # ---------------------------------------------------------
        st.markdown('<div class="section-header"><span>Review Required</span></div>', unsafe_allow_html=True)
        
        state_key = f"review_state_{selected_case_id}"
        if state_key not in st.session_state:
            st.session_state[state_key] = "PENDING"
            
        current_state = st.session_state[state_key]
        
        if current_state == "PENDING":
            st.markdown(f"""<div class="review-pending">
<div style="font-family: 'Lora', serif; font-size: 1.25rem; font-weight: 600; margin-bottom: 8px;">Human Verification Required</div>
<div style="font-size: 0.875rem;">Please review the AI diagnosis before finalizing the case.</div>
</div>""", unsafe_allow_html=True)
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                if st.button("Approve", key=f"btn_approve_{selected_case_id}", type="primary"):
                    log_decision(selected_case_id, ai_result, checker_result, "APPROVE")
                    st.session_state[state_key] = "APPROVED"
                    st.rerun()
            with col_btn2:
                if st.button("Edit", key=f"btn_edit_{selected_case_id}"):
                    st.session_state[state_key] = "EDITING"
                    st.rerun()
            with col_btn3:
                if st.button("Reject", key=f"btn_reject_{selected_case_id}"):
                    st.session_state[state_key] = "REJECTING"
                    st.rerun()
                    
        elif current_state == "EDITING":
            st.markdown('<div class="minimal-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header">Edit Diagnosis</div>', unsafe_allow_html=True)
            with st.form(key=f"edit_form_{selected_case_id}"):
                new_root_cause = st.text_area("Root Cause", value=ai_result.get("root_cause", ""))
                new_next_cmd = st.text_area("Next Commands (One per line)", value="\\n".join(ai_result.get("next_command", [])))
                new_fix_steps = st.text_area("Fix Steps (One per line)", value="\\n".join(ai_result.get("fix_steps", [])))
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("Submit Edit", type="primary"):
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
            st.markdown(f'<div class="minimal-card"><div class="card-header" style="color: {b_dang_tx};">Reject Diagnosis</div>', unsafe_allow_html=True)
            with st.form(key=f"reject_form_{selected_case_id}"):
                comment = st.text_area("Reason for rejection (Required)", placeholder="Explain why the AI diagnosis is incorrect...")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("Submit Reject", type="primary"):
                    if comment.strip():
                        log_decision(selected_case_id, ai_result, checker_result, "REJECT", reviewer_comment=comment)
                        st.session_state[state_key] = "REJECTED"
                        st.rerun()
                    else:
                        st.error("A comment is required.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif current_state == "APPROVED":
            st.markdown('<div class="review-approved">✓ Approved by Human Operator</div>', unsafe_allow_html=True)
            
        elif current_state == "EDITED":
            st.markdown('<div class="review-edited">✎ Edited by Human Operator</div>', unsafe_allow_html=True)

        elif current_state == "REJECTED":
            st.markdown('<div class="review-rejected">✕ Rejected by Human Operator</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 06 // AUDIT LOG TABLE
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span>Audit Log</span></div>', unsafe_allow_html=True)
    
    if audit_log:
        audit_records = []
        for row in sorted(audit_log, key=lambda x: x['timestamp'], reverse=True):
            audit_records.append({
                "Timestamp": row["timestamp"][:19].replace("T", " "),
                "Case": row["case_id"],
                "AI Decision": row["ai_diagnosis"].get("root_cause", "N/A"),
                "Human Decision": row["decision"],
                "Override": "Yes" if row["decision"] in ["EDIT", "REJECT"] else "No",
                "Comment": row["reviewer_comment"] if row["reviewer_comment"] else "-"
            })
        
        audit_df = pd.DataFrame(audit_records)
        
        table_html = "<div style='overflow-x: auto; margin-bottom: 32px;'><table class='minimal-table'><thead><tr>"
        for col in audit_df.columns:
            table_html += f"<th>{col}</th>"
        table_html += "</tr></thead><tbody>"
        
        for _, row in audit_df.head(10).iterrows(): 
            table_html += "<tr>"
            for col in audit_df.columns:
                val = row[col]
                if col == "Human Decision":
                    badge_class = "success" if val == "APPROVE" else ("warning" if val == "EDIT" else "danger")
                    table_html += f"<td><span class='badge {badge_class}'>{val.capitalize()}</span></td>"
                elif col == "Override":
                    txt_color = b_dang_tx if val == "Yes" else text_muted
                    table_html += f"<td style='color: {txt_color} !important;'>{val}</td>"
                else:
                    table_html += f"<td>{val}</td>"
            table_html += "</tr>"
        table_html += "</tbody></table></div>"
        
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='color: {text_muted}; font-size: 0.875rem; font-family: 'Lora', serif; font-style: italic;'>No audit records found.</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 07 // ANALYTICS
    # ---------------------------------------------------------
    st.markdown('<div class="section-header"><span>Analytics</span></div>', unsafe_allow_html=True)
    
    def apply_minimal_style(fig):
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family="Inter, sans-serif",
            font_color=text_sub,
            title_font_family="Lora, serif",
            title_font_size=18,
            title_font_color=heading,
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(showline=True, linewidth=1, linecolor=border_dark, gridcolor=border, title_font_weight=500, tickfont_weight=400),
            yaxis=dict(showline=True, linewidth=1, linecolor=border_dark, gridcolor=border, title_font_weight=500, tickfont_weight=400)
        )
        return fig
    
    if audit_log:
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            sev_counts = df['severity'].value_counts().reset_index()
            sev_counts.columns = ['Severity', 'Count']
            color_map = {"CRITICAL": b_dang_tx, "HIGH": b_dang_tx, "MEDIUM": b_warn_tx, "LOW": b_succ_tx}
            
            fig1 = px.bar(sev_counts, x='Severity', y='Count', title="Severity Distribution", color='Severity', color_discrete_map=color_map)
            fig1.update_traces(marker_line_width=0)
            fig1 = apply_minimal_style(fig1)
            st.markdown('<div class="minimal-card">', unsafe_allow_html=True)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            dec_counts = pd.Series([r['decision'] for r in audit_log]).value_counts().reset_index()
            dec_counts.columns = ['Decision', 'Count']
            color_map2 = {"APPROVE": b_succ_tx, "EDIT": b_warn_tx, "REJECT": b_dang_tx}
            
            fig3 = px.pie(dec_counts, names='Decision', values='Count', title="Human Review Actions", color='Decision', color_discrete_map=color_map2)
            fig3.update_traces(marker_line_width=0, textinfo='percent+label', hole=0.4)
            fig3 = apply_minimal_style(fig3)
            fig3.update_layout(xaxis=dict(showline=False), yaxis=dict(showline=False))
            st.markdown('<div class="minimal-card">', unsafe_allow_html=True)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_c2:
            concept_counts = df['concept_tag'].value_counts().reset_index()
            concept_counts.columns = ['Concept', 'Count']
            fig2 = px.bar(concept_counts, y='Concept', x='Count', orientation='h', title="Cases by Concept", color_discrete_sequence=[text_muted])
            fig2.update_traces(marker_line_width=0)
            fig2 = apply_minimal_style(fig2)
            st.markdown('<div class="minimal-card">', unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            osi_counts = df['osi_layer'].value_counts().reset_index()
            osi_counts.columns = ['OSI Layer', 'Count']
            fig4 = px.bar(osi_counts, x='OSI Layer', y='Count', title="OSI Layer Distribution", color_discrete_sequence=[b_info_tx])
            fig4.update_traces(marker_line_width=0)
            fig4 = apply_minimal_style(fig4)
            st.markdown('<div class="minimal-card">', unsafe_allow_html=True)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("No cases found in data/cases.csv")

# ---------------------------------------------------------
# RESET SYSTEM
# ---------------------------------------------------------
st.markdown('<div class="section-header"><span>System Controls</span></div>', unsafe_allow_html=True)
if st.button("Reset System Stats (Clear Audit Log)"):
    from src.audit import save_audit_log
    save_audit_log([])
    st.session_state.clear()
    st.rerun()