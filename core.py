from typing import Any, Dict, List
import os
import subprocess
import streamlit as st

from privacy import is_title_safe
from tracker import get_active_window_title


def initialize_state() -> None:
    """Ensure the session state contains the required temporary memory values."""
    st.session_state.setdefault("ephemeral_mode", False)
    st.session_state.setdefault("session_logs", [])
    st.session_state.setdefault("current_snapshot", {})
    st.session_state.setdefault("focus_mode_active", False)


def classify_application(title: str) -> str:
    """Classify window titles by scanning for exact auth page profiles and brand layers."""
    normalized = (title or "").lower().strip()

    # Core Keyword Databases
    restricted_keywords = (
        "login", "signin", "sign-in", "signup", "sign-up", "register", "password", 
        "auth", "credentials", "bank", "checkout", "pay", "stripe", "paypal", 
        "wallet", "crypto", "gmail", "accounts.google", "myaccount.google"
    )
    
    # Contextual check for landing screens that default to unauthenticated portals
    brand_auth_landing_screens = ("instagram", "facebook", "twitter", "x.com", "linkedin")
    
    productive_keywords = ("visual studio code", "vs code", "vscode", "notepad", "pycharm", "jupyter", "terminal", "code", "python")
    social_keywords = ("discord", "whatsapp", "reddit", "insta reel", "insta feed", "facebook feed")
    entertainment_keywords = ("youtube", "netflix", "spotify", "steam", "twitch", "game", "vlc")
    research_keywords = ("google search", "bing search", "stackoverflow", "github", "documentation", "wikipedia")

    # 1. First priority: Check standard system authorization and banking words
    if any(kw in normalized for kw in restricted_keywords):
        return "restricted"
        
    # 2. Second priority: Context validation for unauthenticated brand homepages
    if any(brand in normalized for brand in brand_auth_landing_screens):
        if normalized.startswith("instagram -") or normalized.startswith("facebook -") or "log in" in normalized or "sign up" in normalized:
            return "restricted"
        return "social"

    # 3. Standard Fallback Priority Routing
    if any(kw in normalized for kw in social_keywords):
        return "social"
    if any(kw in normalized for kw in entertainment_keywords):
        return "entertainment"
    if any(kw in normalized for kw in productive_keywords):
        return "productive"
    if any(kw in normalized for kw in research_keywords):
        return "research"
        
    # Standard Browser Fallback
    if "chrome" in normalized or "edge" in normalized or "brave" in normalized or "firefox" in normalized:
        return "research"
        
    return "unknown"


def calculate_attention_score(app_class: str) -> int:
    """Return a hardcoded attention coefficient based on core app classification mapping."""
    score_map = {
        "productive": 95,
        "research": 72,
        "unknown": 50,
        "social": 35,
        "entertainment": 18,
        "restricted": 0
    }
    return score_map.get(app_class, 50)


def enforce_focused_mode(app_class: str, current_title: str) -> None:
    """Actively terminates specific background processes if the user violates Focus Mode."""
    if not st.session_state.get("focus_mode_active", False):
        return

    # Trigger background process execution block rules if distraction rules are breached
    if app_class in ["entertainment", "social"]:
        try:
            target_process = ""
            lower_title = current_title.lower()
            
            if "youtube" in lower_title or "netflix" in lower_title or "chrome" in lower_title:
                target_process = "chrome.exe"
            elif "discord" in lower_title:
                target_process = "Discord.exe"
            elif "spotify" in lower_title:
                target_process = "Spotify.exe"
                
            if target_process:
                # Issue direct Windows OS task manager kill commands
                subprocess.Popen(
                    f"taskkill /F /IM {target_process}", 
                    shell=True, 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL
                )
        except Exception:
            pass


def build_dashboard_payload() -> Dict[str, Any]:
    """Build the central dashboard payload from tracker, privacy, and state data."""
    initialize_state()

    title = get_active_window_title()
    app_class = classify_application(title)
    
    is_dashboard = "privacy pulse" in title.lower() or "localhost" in title.lower()
    is_safe = (app_class != "restricted")

    if "threat_latch" not in st.session_state:
        st.session_state.threat_latch = False

    # Manage sticky safety latch states
    if not is_safe and not is_dashboard:
        st.session_state.threat_latch = True
    elif not is_dashboard:
        st.session_state.threat_latch = False

    if st.session_state.threat_latch:
        attention_score = 0
        shield_locked = True
        display_safe = False
        display_title = "🔒 SENSITIVE CONTEXT ENCOUNTERED (LOG PURGED)"
        app_class = "restricted"
    else:
        attention_score = calculate_attention_score(app_class)
        shield_locked = False
        display_safe = True
        display_title = title

    snapshot = {
        "title": display_title,
        "is_safe": display_safe,
        "attention_score": attention_score,
        "shield_locked": shield_locked,
        "application_class": app_class,
    }

    st.session_state.current_snapshot = snapshot

    # Manage history databases
    if st.session_state.ephemeral_mode:
        st.session_state.session_logs.clear()
    else:
        if not st.session_state.session_logs or st.session_state.session_logs[-1]["title"] != snapshot["title"]:
            st.session_state.session_logs.append(snapshot)
        if len(st.session_state.session_logs) > 20:
            st.session_state.session_logs.pop(0)

    # Invoke our underlying process blocker hook automatically 
    enforce_focused_mode(snapshot["application_class"], snapshot["title"])

    return snapshot


def get_sidebar_state() -> bool:
    """Return the current toggle state from session state."""
    initialize_state()
    return bool(st.session_state.ephemeral_mode)


def set_sidebar_state(enabled: bool) -> None:
    """Persist the toggle state in session memory."""
    initialize_state()
    st.session_state.ephemeral_mode = bool(enabled)


def get_insight_items() -> List[Dict[str, str]]:
    """Return structured insight data for the dashboard expander."""
    return [
        {"label": "Focus Mode", "value": "92%", "delta": "+8%"},
        {"label": "Flow State", "value": "3.4 hrs", "delta": "stable"},
        {"label": "Smart Suggestions", "value": "14 queued", "delta": "new"},
    ]
