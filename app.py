import streamlit as st
import sympy as sp
import time

# ==========================================
# 1. PAGE CONFIGURATION & PASTEL THEME CSS
# ==========================================
st.set_page_config(
    page_title="Integration Quest",
    page_icon="✨",
    layout="centered"
)

PASTEL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
        background-color: #f7f9fc;
        color: #2c3e50;
    }

    .stApp {
        background-color: #f7f9fc;
    }

    /* Pastel Card Styling */
    .pastel-card {
        background-color: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 24px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
    }

    /* Header Badges */
    .stat-badge {
        background: #eef2f7;
        border: 1px solid #cbd5e1;
        border-radius: 14px;
        padding: 8px 16px;
        font-weight: 700;
        color: #475569;
        display: inline-block;
        text-align: center;
    }
</style>
"""
st.markdown(PASTEL_CSS, unsafe_allow_html=True)

# ==========================================
# 2. EXPANDED INTEGRATION STAGES (Winding Path)
# ==========================================
STAGES = [
    {
        "id": 1,
        "name": "Stage 1: Polynomial Foundations",
        "icon": "🌱",
        "color": "#a7f3d0", # Pastel Mint
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
        "name": "Stage 2: Exponentials",
        "icon": "☁️",
        "color": "#bae6fd", # Pastel Blue
        "questions": [
            {
                "prompt": "Find the integral of the exponential function:",
                "latex_expr": "\\int e^{2x} \\, dx",
                "options": ["2e^{2x} + C", "\\frac{1}{2}e^{2x} + C", "e^{2x} + C", "\\frac{1}{4}e^{2x} + C"],
                "answer": "\\frac{1}{2}e^{2x} + C"
            },
            {
                "prompt": "Find the general exponential integral:",
                "latex_expr": "\\int e^{5x} \\, dx",
                "options": ["5e^{5x} + C", "\\frac{1}{5}e^{5x} + C", "e^{5x} + C", "\\frac{1}{25}e^{5x} + C"],
                "answer": "\\frac{1}{5}e^{5x} + C"
            }
        ]
    },
    {
        "id": 3,
        "name": "Stage 3: Trigonometric Integrals",
        "icon": "🌸",
        "color": "#fed7aa", # Pastel Peach
        "questions": [
            {
                "prompt": "Integrate the trigonometric function:",
                "latex_expr": "\\int \\cos(3x) \\, dx",
                "options": ["-3\\sin(3x) + C", "\\frac{1}{3}\\sin(3x) + C", "3\\sin(3x) + C", "-\\frac{1}{3}\\sin(3x) + C"],
                "answer": "\\frac{1}{3}\\sin(3x) + C"
            },
            {
                "prompt": "Find the integral of sine:",
                "latex_expr": "\\int \\sin(2x) \\, dx",
                "options": ["-\\frac{1}{2}\\cos(2x) + C", "\\frac{1}{2}\\cos(2x) + C", "-2\\cos(2x) + C", "2\\cos(2x) + C"],
                "answer": "-\\frac{1}{2}\\cos(2x) + C"
            }
        ]
    },
    {
        "id": 4,
        "name": "Stage 4: Substitution Method",
        "icon": "🍯",
        "color": "#fbcfe8", # Pastel Pink
        "questions": [
            {
                "prompt": "Evaluate using substitution ($u = x^2 + 1$):",
                "latex_expr": "\\int 2x(x^2 + 1)^3 \\, dx",
                "options": ["\\frac{1}{4}(x^2+1)^4 + C", "(x^2+1)^4 + C", "\\frac{1}{2}(x^2+1)^4 + C", "4(x^2+1)^4 + C"],
                "answer": "\\frac{1}{4}(x^2+1)^4 + C"
            },
            {
                "prompt": "Evaluate the logarithmic substitution integral:",
                "latex_expr": "\\int \\frac{2x}{x^2 + 1} \\, dx",
                "options": ["\\ln(x^2 + 1) + C", "\\frac{1}{x^2+1} + C", "2\\ln(x) + C", "\\ln(|x|) + C"],
                "answer": "\\ln(x^2 + 1) + C"
            }
        ]
    },
    {
        "id": 5,
        "name": "Stage 5: Definite Integrals",
        "icon": "⭐",
        "color": "#e9d5ff", # Pastel Purple
        "questions": [
            {
                "prompt": "Evaluate the definite integral:",
                "latex_expr": "\\int_{0}^{2} 3x^2 \\, dx",
                "options": ["6", "8", "12", "4"],
                "answer": "8"
            },
            {
                "prompt": "Evaluate the linear definite integral:",
                "latex_expr": "\\int_{1}^{3} 2x \\, dx",
                "options": ["4", "6", "8", "10"],
                "answer": "8"
            }
        ]
    }
]

# ==========================================
# 3. SESSION STATE MANAGEMENT
# ==========================================
if "screen" not in st.session_state:
    st.session_state.screen = "map"
if "current_stage" not in st.session_state:
    st.session_state.current_stage = 1
if "unlocked_stage" not in st.session_state:
    st.session_state.unlocked_stage = 1
if "hearts" not in st.session_state:
    st.session_state.hearts = 3
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0

# ==========================================
# 4. PATH MAP SCREEN (Duolingo Style Zig-Zag)
# ==========================================
if st.session_state.screen == "map":
    # Header status bar
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='stat-badge' style='width:100%'>❤️ {st.session_state.hearts} / 3</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-badge' style='width:100%'>✨ {st.session_state.xp} XP</div>", unsafe_allow_html=True)
    with c3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.unlocked_stage = 1
            st.session_state.hearts = 3
            st.session_state.xp = 0
            st.rerun()

    st.markdown("<h2 style='text-align: center; margin-top: 25px; color: #334155;'>Integration Journey</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Complete stages along the pastel path to master calculus.</p>", unsafe_allow_html=True)
    st.write("")

    # Zig-zag layout rendering
    for i, stage in enumerate(STAGES):
        is_unlocked = stage["id"] <= st.session_state.unlocked_stage
        
        # Calculate offset alignment to mimic winding path
        alignment = [2, 1, 3, 2, 1][i % 5]
        cols = st.columns([1, 1, 1])
        
        with cols[alignment - 1]:
            bg_col = stage["color"] if is_unlocked else "#e2e8f0"
            text_col = "#1e293b" if is_unlocked else "#94a3b8"
            
            st.markdown(
                f"""
                <div style="background-color: {bg_col}; border-radius: 20px; padding: 16px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.03); margin-bottom: 10px;">
                    <span style="font-size: 28px;">{stage['icon']}</span>
                    <div style="font-weight: 700; color: {text_col}; font-size: 14px; margin-top: 5px;">Stage {stage['id']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if is_unlocked:
                if st.button(f"Start S{stage['id']}", key=f"stage_{stage['id']}", use_container_width=True):
                    st.session_state.current_stage = stage["id"]
                    st.session_state.q_index = 0
                    st.session_state.screen = "lesson"
                    st.rerun()
            else:
                st.button(f"🔒 Locked", key=f"lock_{stage['id']}", disabled=True, use_container_width=True)

        st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)

# ==========================================
# 5. LESSON SCREEN
# ==========================================
elif st.session_state.screen == "lesson":
    stage_data = STAGES[st.session_state.current_stage - 1]
    questions = stage_data["questions"]
    
    col_back, col_h, col_x = st.columns([1, 2, 1])
    with col_back:
        if st.button("← Back"):
            st.session_state.screen = "map"
            st.rerun()
    with col_h:
        st.markdown(f"<div style='text-align: center; font-weight: 700; color:#ef4444;'>❤️ {st.session_state.hearts}</div>", unsafe_allow_html=True)
    with col_x:
        st.markdown(f"<div style='text-align: right; font-weight: 700; color: #10b981;'>✨ {st.session_state.xp}</div>", unsafe_allow_html=True)

    # Check if questions finished
    if st.session_state.q_index >= len(questions):
        st.markdown("<div class='pastel-card'>", unsafe_allow_html=True)
        st.balloons()
        st.markdown("<h2 style='color: #0f766e;'>🎉 Stage Complete!</h2>", unsafe_allow_html=True)
        st.write(f"Wonderful job conquering **{stage_data['name']}**!")
        
        # Unlock next stage
        if st.session_state.current_stage >= st.session_state.unlocked_stage and st.session_state.current_stage < len(STAGES):
            st.session_state.unlocked_stage = st.session_state.current_stage + 1
            
        if st.button("Return to Path", use_container_width=True):
            st.session_state.screen = "map"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        q = questions[st.session_state.q_index]
        
        st.markdown("<div class='pastel-card'>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='color: #334155;'>{q['prompt']}</h4>", unsafe_allow_html=True)
        st.write("")
        st.latex(q["latex_expr"])
        st.markdown("</div>", unsafe_allow_html=True)

        selected_option = None
        for opt in q["options"]:
            if st.button(f"$${opt}$$", key=f"opt_{opt}", use_container_width=True):
                selected_option = opt

        if selected_option is not None:
            if selected_option == q["answer"]:
                st.success("✨ Correct! Amazing work.")
                st.session_state.xp += 20
                st.session_state.q_index += 1
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
