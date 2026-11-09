import streamlit as st
import sympy as sp
import random

# ==========================================
# 1. PAGE CONFIGURATION & DUOLINGO-STYLE CSS
# ==========================================
st.set_page_config(
    page_title="Integration Quest",
    page_icon="⚡",
    layout="centered"
)

DUOLINGO_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
        background-color: #131f24;
        color: #ffffff;
    }

    .stApp {
        background-color: #131f24;
    }

    /* Card styling */
    .duo-card {
        background-color: #1f2e35;
        border: 2px solid #2c424a;
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 6px 0 #111a1f;
        margin-bottom: 20px;
    }

    /* Level Node Styling */
    .level-node {
        background: #2b70c9;
        border: 4px solid #1cb0f6;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: 900;
        color: white;
        margin: 0 auto;
        box-shadow: 0 6px 0 #185a9d;
        cursor: pointer;
    }

    .level-node-locked {
        background: #37464f;
        border: 4px solid #4d606b;
        box-shadow: 0 6px 0 #222d33;
        color: #7b8d96;
    }

    /* Stat Header */
    .stat-badge {
        background: #1f2e35;
        border: 2px solid #2c424a;
        border-radius: 12px;
        padding: 8px 16px;
        font-weight: 800;
        display: inline-block;
        margin: 0 5px;
    }
</style>
"""
st.markdown(DUOLINGO_CSS, unsafe_allow_html=True)

# ==========================================
# 2. GAME DATA (4 Focused Integration Levels)
# ==========================================
LEVELS = [
    {
        "id": 1,
        "name": "Basics & Power Rule",
        "icon": "🌱",
        "description": "Master basic polynomial anti-derivatives.",
        "questions": [
            {
                "prompt": "Find the indefinite integral:",
                "latex_expr": "\\int (6x^2 + 2x) \\, dx",
                "options": ["2x^3 + x^2 + C", "6x^3 + 2x^2 + C", "3x^3 + x^2 + C", "x^3 + x^2 + C"],
                "answer": "2x^3 + x^2 + C"
            },
            {
                "prompt": "Evaluate the basic power rule integral:",
                "latex_expr": "\\int 4x^3 \\, dx",
                "options": ["x^4 + C", "12x^2 + C", "4x^4 + C", "\\frac{1}{4}x^4 + C"],
                "answer": "x^4 + C"
            }
        ]
    },
    {
        "id": 2,
        "name": "Exponentials & Trig",
        "icon": "⚡",
        "description": "Integrate exponential and trigonometric functions.",
        "questions": [
            {
                "prompt": "Find the integral of the exponential function:",
                "latex_expr": "\\int e^{2x} \\, dx",
                "options": ["2e^{2x} + C", "\\frac{1}{2}e^{2x} + C", "e^{2x} + C", "\\frac{1}{4}e^{2x} + C"],
                "answer": "\\frac{1}{2}e^{2x} + C"
            },
            {
                "prompt": "Integrate the trigonometric function:",
                "latex_expr": "\\int \\cos(3x) \\, dx",
                "options": ["-3\\sin(3x) + C", "\\frac{1}{3}\\sin(3x) + C", "3\\sin(3x) + C", "-\\frac{1}{3}\\sin(3x) + C"],
                "answer": "\\frac{1}{3}\\sin(3x) + C"
            }
        ]
    },
    {
        "id": 3,
        "name": "Substitution Rule",
        "icon": "🔥",
        "description": "Reverse the chain rule using u-substitution.",
        "questions": [
            {
                "prompt": "Evaluate using substitution ($u = x^2 + 1$):",
                "latex_expr": "\\int 2x(x^2 + 1)^3 \\, dx",
                "options": ["\\frac{1}{4}(x^2+1)^4 + C", "(x^2+1)^4 + C", "\\frac{1}{2}(x^2+1)^4 + C", "4(x^2+1)^4 + C"],
                "answer": "\\frac{1}{4}(x^2+1)^4 + C"
            }
        ]
    },
    {
        "id": 4,
        "name": "Definite Integrals",
        "icon": "🏆",
        "description": "Calculate exact accumulated area values.",
        "questions": [
            {
                "prompt": "Evaluate the definite integral:",
                "latex_expr": "\\int_{0}^{2} 3x^2 \\, dx",
                "options": ["6", "8", "12", "4"],
                "answer": "8"
            }
        ]
    }
]

# ==========================================
# 3. SESSION STATE MANAGEMENT
# ==========================================
if "screen" not in st.session_state:
    st.session_state.screen = "map"  # "map" or "lesson"
if "current_level" not in st.session_state:
    st.session_state.current_level = 1
if "unlocked_level" not in st.session_state:
    st.session_state.unlocked_level = 1
if "hearts" not in st.session_state:
    st.session_state.hearts = 3
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0

# ==========================================
# 4. SCREEN: LEVEL MAP (Duolingo Style Path)
# ==========================================
if st.session_state.screen == "map":
    # Top Bar (Stats)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='stat-badge'>❤️ {st.session_state.hearts} / 3</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-badge'>⚡ {st.session_state.xp} XP</div>", unsafe_allow_html=True)
    with col3:
        if st.button("🔄 Reset"):
            st.session_state.unlocked_level = 1
            st.session_state.hearts = 3
            st.session_state.xp = 0
            st.rerun()

    st.markdown("<h1 style='text-align: center; margin-top: 20px;'>Integration Quest</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8af2ff;'>Choose a level to start practicing calculus!</p>", unsafe_allow_html=True)
    st.write("")

    # Render Path Nodes
    for lvl in LEVELS:
        is_unlocked = lvl["id"] <= st.session_state.unlocked_level
        
        col_left, col_mid, col_right = st.columns([1, 2, 1])
        with col_mid:
            st.markdown(f"<div style='text-align: center; font-weight: 800; color: #a0aec0; margin-bottom: 5px;'>Level {lvl['id']}: {lvl['name']}</div>", unsafe_allow_html=True)
            
            if is_unlocked:
                if st.button(f"{lvl['icon']} Play L{lvl['id']}", key=f"lvl_btn_{lvl['id']}", use_container_width=True):
                    st.session_state.current_level = lvl["id"]
                    st.session_state.q_index = 0
                    st.session_state.screen = "lesson"
                    st.rerun()
            else:
                st.button(f"🔒 Level {lvl['id']}", key=f"lock_btn_{lvl['id']}", disabled=True, use_container_width=True)
        
        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

# ==========================================
# 5. SCREEN: INTERACTIVE LESSON
# ==========================================
elif st.session_state.screen == "lesson":
    lvl_data = LEVELS[st.session_state.current_level - 1]
    questions = lvl_data["questions"]
    
    # Back button & Stats header
    col_back, col_h, col_x = st.columns([1, 2, 1])
    with col_back:
        if st.button("← Exit"):
            st.session_state.screen = "map"
            st.rerun()
    with col_h:
        st.markdown(f"<div style='text-align: center; font-weight: 700;'>❤️ {st.session_state.hearts}</div>", unsafe_allow_html=True)
    with col_x:
        st.markdown(f"<div style='text-align: right; font-weight: 700; color: #00f5d4;'>⚡ {st.session_state.xp}</div>", unsafe_allow_html=True)

    # Check if lesson finished
    if st.session_state.q_index >= len(questions):
        st.markdown("<div class='duo-card'>", unsafe_allow_html=True)
        st.balloons()
        st.markdown("<h2>🎉 Level Completed!</h2>", unsafe_allow_html=True)
        st.write(f"You successfully conquered **{lvl_data['name']}**!")
        
        # Unlock next level if applicable
        if st.session_state.current_level >= st.session_state.unlocked_level and st.session_state.current_level < len(LEVELS):
            st.session_state.unlocked_level = st.session_state.current_level + 1
            
        if st.button("Continue to Map", use_container_width=True):
            st.session_state.screen = "map"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        q = questions[st.session_state.q_index]
        
        st.markdown("<div class='duo-card'>", unsafe_allow_html=True)
        st.markdown(f"<h4>{q['prompt']}</h4>", unsafe_allow_html=True)
        st.write("")
        # Clean LaTeX rendering
        st.latex(q["latex_expr"])
        st.markdown("</div>", unsafe_allow_html=True)

        # Options layout (Duolingo pill style buttons)
        selected_option = None
        for opt in q["options"]:
            if st.button(f"$${opt}$$", key=f"opt_{opt}", use_container_width=True):
                selected_option = opt

        if selected_option is not None:
            if selected_option == q["answer"]:
                st.success("✨ Correct! Amazing job.")
                st.session_state.xp += 15
                st.session_state.q_index += 1
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Not quite right. Try again!")
                st.session_state.hearts -= 1
                if st.session_state.hearts <= 0:
                    st.warning("💔 Out of hearts! Returning to map to recover.")
                    st.session_state.hearts = 3
                    st.session_state.screen = "map"
                    st.rerun()

# ==========================================
# 6. REQUIREMENTS (For your reference)
# ==========================================
# To run this app locally:
# 1. pip install streamlit sympy
# 2. streamlit run app.py
