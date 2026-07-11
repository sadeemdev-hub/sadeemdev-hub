import streamlit as st
from streamlit_autorefresh import st_autorefresh

from core import (
    build_dashboard_payload,
    get_insight_items,
    get_sidebar_state,
    set_sidebar_state,
)

# 🔄 THE MAGIC FIX: Force the background dashboard script to auto-refresh every 2 seconds
st_autorefresh(interval=2000, key="datarefresh")

st.set_page_config(
    page_title="Privacy Pulse",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root { color-scheme: dark; }
        .stApp {
            background: radial-gradient(circle at top left, #111827 0%, #030712 70%, #000000 100%);
            color: #f8fafc;
        }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.25);
        }
        div[data-testid="stMetricLabel"] { font-size: 0.95rem; color: #94a3b8; }
        div[data-testid="stMetricValue"] { font-size: 1.2rem; font-weight: 700; color: #f8fafc; }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_header() -> None:
    st.markdown(
        """
        <div style="padding: 0.2rem 0 1.2rem 0;">
            <h1 style="margin:0; font-size:2.2rem; color:#f8fafc;">🛡️ Privacy Pulse</h1>
            <p style="margin:0.4rem 0 0 0; color:#8b97ac; font-size:1rem;">
                Enterprise-grade window awareness with a premium, hacker-inspired control panel.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.header("Controls")
        
        # Read the current session state cache cleanly from core.py
        current_toggle_val = get_sidebar_state()
        
        enabled = st.toggle(
            "🗑️ Ephemeral Session Mode (Auto-Delete Logs)",
            value=current_toggle_val,
        )
        # Inside app.py -> inside render_sidebar():
        st.write("---")
        st.subheader("🎯 Work Mode Configuration")

        # Initialize the state variable inside cache memory safely
        if "focus_mode_active" not in st.session_state:
            st.session_state.focus_mode_active = False

        focus_toggle = st.toggle(
            "🚀 Engage High-Intensity Focus Lock",
            value=st.session_state.focus_mode_active,
            help="When active, the background system will automatically terminate known distracting apps."
        )
        st.session_state.focus_mode_active = focus_toggle

        # Update your core processor array configuration state seamlessly
        if enabled != current_toggle_val:
            set_sidebar_state(enabled)
            st.rerun()
            
        st.caption(
            "When enabled, the latest window snapshot is removed from temporary session memory immediately after display."
        )


def render_status_panel(snapshot: dict) -> None:
    status_text = "Active" if snapshot["is_safe"] else "Threat Detected"
    accent = "#00F5A0" if snapshot["is_safe"] else "#FF6B35"
    subtitle = "Your current context looks clean." if snapshot["is_safe"] else "A login or sensitive screen was detected."
    
    # Clean the window text string to handle nested HTML quotes inside browsers safely
    safe_display_title = str(snapshot['title']).replace('"', '&quot;').replace("'", "'")

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(0,245,160,0.16), rgba(3,7,18,0.95));
                    border: 1px solid {accent};
                    border-radius: 18px;
                    padding: 1.2rem 1.3rem;
                    margin: 0.3rem 0 1.2rem 0;
                    box-shadow: 0 0 22px rgba(0,245,160,0.16);">
            <div style="font-size:0.95rem; color:#8b97ac; margin-bottom:0.35rem;">Privacy Guard</div>
            <div style="font-size:1.7rem; color:#f8fafc; font-weight:700;">{status_text}</div>
            <div style="font-size:1rem; color:{accent}; margin-top:0.35rem;">{subtitle}</div>
            <div style="margin-top:0.7rem; font-size:0.92rem; color:#cbd5e1;">Current title: <strong>{safe_display_title}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insights(snapshot: dict) -> None:
    with st.expander("📝 View Your Custom AI Productivity Insights", expanded=True):
        cols = st.columns(3)
        
        # Pull live values from our snapshot payload dictionary to refresh widgets instantly
        current_class = snapshot["application_class"].upper()
        focus_metric = f"{snapshot['attention_score']}%"
        
        with cols[0]:
            st.metric("Current Mode", current_class, delta="Dynamic State")
        with cols[1]:
            st.metric("Attention Value", focus_metric, delta="Live Sync")
        with cols[2]:
            st.metric("Threat Filter", "ACTIVE" if snapshot["is_safe"] else "LOCKED", delta="Shield")

        st.markdown(
            f"""
            <div style="margin-top:0.8rem; padding:1rem 1.1rem; border-radius:14px;
                        background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);">
                <h4 style="margin:0 0 0.4rem 0; color:#7CFF5A;">AI Snapshot Engine</h4>
                <ul style="margin:0; padding-left:1.2rem; color:#B7FF7A;">
                    <li>Background system hooks actively validating active threads.</li>
                    <li>Current processing allocation class detected as: <b>{current_class}</b></li>
                    <li>Security parameters: {"Shield compliant." if snapshot["is_safe"] else "Data streams masked."}</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --- EXECUTION PIPELINE ---
render_header()
render_sidebar()

# Fetch payload dictionaries directly from the central core processing engine
snapshot = build_dashboard_payload()

col_left, col_right = st.columns([2, 1])
with col_left:
    st.metric("Active Window Title", snapshot["title"])
with col_right:
    render_status_panel(snapshot)

# --- 🎯 VISUAL ATTENTION METER SECTION ---
st.markdown(
    f"""
    <div style="margin: 0.2rem 0 1.2rem 0;">
        <div style="font-size:0.92rem; color:#8b97ac; margin-bottom:0.35rem;">🎯 Focus & Attention Meter</div>
        <div style="background:#0f172a; border:1px solid rgba(255,255,255,0.08); border-radius:999px; padding:0.2rem;">
            <div style="width:{snapshot['attention_score']}%; background:linear-gradient(90deg,#00F5A0,#7CFF5A); height:0.8rem; border-radius:999px;"></div>
        </div>
        <div style="margin-top:0.35rem; color:#f8fafc; font-weight:700;">{snapshot['attention_score']}/100</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 📊 NEW: TIME-SERIES VISUAL ATTENTION GRAPH ---
# --- 📊 NEW: TIME-SERIES VISUAL ATTENTION GRAPH ---
st.write("---")
st.subheader("📊 Focus & Analytics Trend Timeline")

import plotly.graph_objects as go

# Read historical snapshot list out of core session state storage
history_logs = st.session_state.get("session_logs", [])

if history_logs and len(history_logs) > 1:
    # Extract data streams cleanly
    scores_timeline = [log["attention_score"] for log in history_logs]
    x_indices = list(range(len(scores_timeline)))
    
    # Construct a high-end, cyberpunk style neon path chart
    fig = go.Figure()
    
    # Add the core focus area path line
    fig.add_trace(go.Scatter(
        x=x_indices, 
        y=scores_timeline,
        mode='lines+markers',
        line=dict(color='#00F5A0', width=3), # Sharp electric neon green line
        marker=dict(size=6, color='#7CFF5A', symbol='circle'),
        fill='tozeroy',
        fillcolor='rgba(0, 245, 160, 0.08)', # Soft translucent neon background glow [22]
        hoverinfo='y+text',
        name='Focus'
    ))
    
    # Premium dark system formatting to completely blend into your layout
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', # Full background transparency
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=10, b=20),
        height=220,
        showlegend=False,
        xaxis=dict(
            showgrid=False, 
            zeroline=False, 
            showticklabels=False, # Hide messy timestamp numbers
            linecolor='rgba(255,255,255,0.05)'
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(255,255,255,0.03)', # Extremely subtle horizontal layout grids
            zeroline=False, 
            range=[0, 105],
            tickfont=dict(color='#8b97ac', size=10)
        )
    )
    
    # Render the advanced dashboard layout
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
else:
    st.info("Gathering active data stream... Switch windows to generate your timeline analytics trend chart.")

# --- 🛡️ NEW: MODULAR PAST ACTIVITIES BLOCK TIMELINE ---
# --- 🛡️ NEW: MODULAR PAST ACTIVITIES BLOCK TIMELINE ---
st.write("---")
st.subheader("📜 Historical Activity Stream (Multi-Tier Timeline)")

if not history_logs:
    st.caption("No historical logs recorded. Enable log tracking or switch applications.")
else:
    for idx, log in enumerate(reversed(history_logs)):
        app_type = log["application_class"]
        
        # 🎨 Advanced Color Mapping Dictionary for true professional UI styling
        theme_map = {
            "productive": {"color": "#00F5A0", "label": "🚀 PRODUCTIVE", "glow": "rgba(0, 245, 160, 0.05)"},
            "research": {"color": "#00D2FF", "label": "🌐 RESEARCH", "glow": "rgba(0, 210, 255, 0.05)"},
            "social": {"color": "#FF007F", "label": "💬 SOCIAL", "glow": "rgba(255, 0, 127, 0.05)"},
            "entertainment": {"color": "#FFCC00", "label": "🎬 ENTERTAIN", "glow": "rgba(255, 204, 0, 0.05)"},
            "restricted": {"color": "#FF4136", "label": "🔒 RESTRICTED", "glow": "rgba(255, 65, 54, 0.05)"},
            "unknown": {"color": "#94a3b8", "label": "🔍 UNKNOWN", "glow": "rgba(148, 163, 184, 0.05)"}
        }
        
        # Get active theme parameters, default to unknown styling if bucket fails
        cfg = theme_map.get(app_type, theme_map["unknown"])
        
        clean_item_title = str(log['title']).replace('"', '&quot;').replace("'", "&#39;")
        
        # Injecting dynamic styling attributes seamlessly
        st.markdown(
            f"""
            <div style="background: linear-gradient(90deg, {cfg['glow']}, #030712);
                        border: 1px solid rgba(255,255,255,0.06);
                        border-left: 4px solid {cfg['color']};
                        border-radius: 12px;
                        padding: 0.8rem 1.2rem;
                        margin-bottom: 0.6rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <div style="flex-grow: 1; min-width: 0; padding-right: 15px;">
                    <span style="background: {cfg['color']}22; color: {cfg['color']}; 
                                 font-size: 0.72rem; font-weight: 700; padding: 0.2rem 0.5rem; 
                                 border-radius: 6px; margin-right: 0.8rem; border: 1px solid {cfg['color']}44;
                                 white-space: nowrap;">
                        {cfg['label']}
                    </span>
                    <strong style="color: #f8fafc; font-size: 0.95rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: inline-block; max-width: 70%; vertical-align: middle;">
                        {clean_item_title}
                    </strong>
                </div>
                <div style="color: {cfg['color']}; font-weight: 700; font-size: 1.1rem; text-align: right; min-width: 70px;">
                    {log['attention_score']}/100
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# Render old static insights container under our new visual data tools
st.write("---")
# At the very bottom line of app.py: change from render_insights() to:
render_insights(snapshot)

