import streamlit as st
import json
import os
import sympy as sp

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================

st.set_page_config(
    page_title="Integration Quest - IB Math AA HL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
:root {
    --bg-dark: #0b0f19;
    --card-bg: #151c2c;
    --card-border: #243047;
    --accent-purple: #9d4edd;
    --accent-cyan: #00f5d4;
    --text-main: #f8f9fa;
    --text-muted: #a0aec0;
}

body {
    background-color: var(--bg-dark);
    color: var(--text-main);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.stApp {
    background-color: var(--bg-dark);
}

.quest-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.quest-card:hover {
    border-color: var(--accent-purple);
    transform: translateY(-2px);
}

.card-header {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--accent-cyan);
    margin-bottom: 8px;
}

.card-subtitle {
    font-size: 0.9rem;
    color: var(--text-muted);
}

.level-locked {
    opacity: 0.5;
    filter: grayscale(80%);
    border-style: dashed;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# 2. EMBEDDED DATA STRUCTURES
# ==========================================

LEVELS_DATA = [
    {
        "id": 1,
        "title": "Level 1: Fundamentals",
        "topic": "Basic Anti-derivatives & Power Rule",
        "description": "Master the inverse operation of differentiation and standard polynomial integrals."
    },
    {
        "id": 2,
        "title": "Level 2: Standard Integration",
        "topic": "Exponential & Trigonometric Functions",
        "description": "Integrate e^(ax+b), sin(ax+b), cos(ax+b), and 1/(ax+b)."
    },
    {
        "id": 3,
        "title": "Level 3: Integration Techniques",
        "topic": "Integration by Substitution",
        "description": "Learn to reverse the chain rule using algebraic substitutions."
    },
    {
        "id": 4,
        "title": "Level 4: Advanced Techniques",
        "topic": "Integration by Parts & Identity Tricks",
        "description": "Master integral product rules and trigonometric identity transformations."
    },
    {
        "id": 5,
        "title": "Level 5: Definite Integrals",
        "topic": "Fundamental Theorem of Calculus",
        "description": "Evaluate definite integrals with exact values and limits of integration."
    },
    {
        "id": 6,
        "title": "Level 6: Applications & Areas",
        "topic": "Area Between Curves & Kinematics",
        "description": "Calculate areas enclosed by functions and model physical motion."
    },
    {
        "id": 7,
        "title": "Level 7: Exam Boss Battle",
        "topic": "IB AA HL Exam-Style Questions",
        "description": "Tackle multi-step, paper-style Calculus questions under pressure."
    }
]

NOTES_DATA = [
    {
        "category": "Standard Integrals",
        "title": "Power Rule",
        "formula": "\\int x^n dx = \\frac{x^{n+1}}{n+1} + C, \\quad n \\neq -1",
        "note": "Valid for rational powers except n = -1."
    },
    {
        "category": "Standard Integrals",
        "title": "Logarithmic Form",
        "formula": "\\int \\frac{1}{x} dx = \\ln|x| + C",
        "note": "Extends to linear functions: \\int \\frac{1}{ax+b} dx = \\frac{1}{a} \\ln|ax+b| + C."
    },
    {
        "category": "Standard Integrals",
        "title": "Exponentials",
        "formula": "\\int e^{ax+b} dx = \\frac{1}{a} e^{ax+b} + C",
        "note": "For general base: \\int a^x dx = \\frac{a^x}{\\ln a} + C."
    },
    {
        "category": "Trigonometric Integrals",
        "title": "Sine & Cosine",
        "formula": "\\int \\cos(ax) dx = \\frac{1}{a}\\sin(ax) + C, \\quad \\int \\sin(ax) dx = -\\frac{1}{a}\\cos(ax) + C",
        "note": "Pay attention to negative signs when integrating sine."
    },
    {
        "category": "Trigonometric Integrals",
        "title": "Secant Squared",
        "formula": "\\int \\sec^2(x) dx = \\tan(x) + C",
        "note": "Direct result from tangent differentiation."
    },
    {
        "category": "Advanced Methods",
        "title": "Integration by Parts",
        "formula": "\\int u \\frac{dv}{dx} dx = uv - \\int v \\frac{du}{dx} dx",
        "note": "Use LATE priority rule for choosing u: Logarithmic, Inverse trig, Algebraic, Trig, Exponential."
    },
    {
        "category": "Advanced Methods",
        "title": "Substitution Method",
        "formula": "\\int f(g(x))g'(x) dx = \\int f(u) du",
        "note": "Substitute u = g(x) and du = g'(x)dx."
    }
]

QUESTIONS_DATA = [
    {
        "level_id": 1,
        "concept": "The Power Rule for Integration is the inverse of the Power Rule for differentiation. Add 1 to the exponent and divide by the new exponent.",
        "formula": "\\int x^n dx = \\frac{x^{n+1}}{n+1} + C",
        "method": "1. Identify n.\n2. Calculate n+1.\n3. Divide term by (n+1).\n4. Add + C.",
        "worked_example": "Find \\int 3x^2 dx. Solution: 3 \\cdot \\frac{x^3}{3} + C = x^3 + C.",
        "guided_question": "Find \\int 4x^3 dx.",
        "guided_hint": "Add 1 to exponent 3 to get 4, then divide coefficient 4 by 4.",
        "guided_answer": "x^4 + C",
        "independent_question": "Find \\int (6x^2 + 2x) dx.",
        "independent_answer": "2*x^3 + x^2 + C",
        "xp": 100
    },
    {
        "level_id": 2,
        "concept": "Integrating exponential and linear composite functions requires adjusting by the inner linear derivative coefficient a.",
        "formula": "\\int e^{ax+b} dx = \\frac{1}{a}e^{ax+b} + C",
        "method": "1. Identify coefficient a.\n2. Keep exponent intact.\n3. Multiply by 1/a.",
        "worked_example": "Find \\int e^{3x} dx. Solution: \\frac{1}{3}e^{3x} + C.",
        "guided_question": "Find \\int e^{5x} dx.",
        "guided_hint": "Divide by the coefficient of x, which is 5.",
        "guided_answer": "(1/5)*exp(5*x) + C",
        "independent_question": "Find \\int (\\cos(2x) + e^{4x}) dx.",
        "independent_answer": "(1/2)*sin(2*x) + (1/4)*exp(4*x) + C",
        "xp": 150
    },
    {
        "level_id": 3,
        "concept": "Integration by Substitution reverses the chain rule by mapping complex composite functions into simpler u-terms.",
        "formula": "\\int f(g(x))g'(x)dx = \\int f(u)du",
        "method": "1. Set u = g(x).\n2. Compute du = g'(x)dx.\n3. Rewrite integral completely in u.\n4. Integrate and substitute back.",
        "worked_example": "Find \\int 2x(x^2+1)^3 dx. Let u = x^2+1, du = 2xdx. Integral becomes \\int u^3 du = \\frac{u^4}{4} + C = \\frac{(x^2+1)^4}{4} + C.",
        "guided_question": "Find \\int 3x^2(x^3 + 5)^4 dx.",
        "guided_hint": "Let u = x^3 + 5, so du = 3x^2 dx.",
        "guided_answer": "(x^3 + 5)^5 / 5 + C",
        "independent_question": "Find \\int \\frac{2x}{x^2 + 1} dx.",
        "independent_answer": "ln(x^2 + 1) + C",
        "xp": 200
    },
    {
        "level_id": 4,
        "concept": "Integration by Parts handles products of two distinct function classes (e.g., algebraic and trigonometric/exponential).",
        "formula": "\\int u \\frac{dv}{dx} dx = uv - \\int v \\frac{du}{dx} dx",
        "method": "1. Select u using LATE rule.\n2. Differentiate u to get du.\n3. Integrate dv to get v.\n4. Apply formula.",
        "worked_example": "Find \\int x e^x dx. u = x, dv = e^x dx -> du = dx, v = e^x. Ans: x e^x - e^x + C.",
        "guided_question": "Find \\int x \\cos(x) dx.",
        "guided_hint": "Let u = x (so du = dx) and dv = cos(x)dx (so v = sin(x)).",
        "guided_answer": "x*sin(x) + cos(x) + C",
        "independent_question": "Find \\int x e^{2x} dx.",
        "independent_answer": "(x/2)*exp(2*x) - (1/4)*exp(2*x) + C",
        "xp": 250
    },
    {
        "level_id": 5,
        "concept": "Definite Integrals compute net accumulated change over an interval [a, b] without the constant of integration C.",
        "formula": "\\int_{a}^{b} f(x) dx = F(b) - F(a)",
        "method": "1. Find anti-derivative F(x).\n2. Evaluate F(b).\n3. Evaluate F(a).\n4. Subtract F(b) - F(a).",
        "worked_example": "Evaluate \\int_{0}^{2} 3x^2 dx. F(x) = x^3. F(2) - F(0) = 8 - 0 = 8.",
        "guided_question": "Evaluate \\int_{1}^{3} 2x dx.",
        "guided_hint": "Anti-derivative is x^2. Evaluate 3^2 - 1^2.",
        "guided_answer": "8",
        "independent_question": "Evaluate \\int_{0}^{1} (3x^2 + 2x) dx.",
        "independent_answer": "2",
        "xp": 300
    },
    {
        "level_id": 6,
        "concept": "Definite integrals yield the total area between curves f(x) and g(x) over [a, b].",
        "formula": "A = \\int_{a}^{b} (f(x) - g(x)) dx \\quad \\text{where } f(x) \\ge g(x)",
        "method": "1. Find intersection points (limits a and b).\n2. Determine top function f(x) and bottom g(x).\n3. Set up integral \\int_{a}^{b} (top - bottom) dx.\n4. Evaluate.",
        "worked_example": "Find area between y = x and y = x^2 from x=0 to x=1. Top: x, Bottom: x^2. \\int_0^1 (x - x^2) dx = [x^2/2 - x^3/3]_0^1 = 1/6.",
        "guided_question": "Find the area bounded by y = 4 - x^2 and the x-axis between x = -2 and x = 2.",
        "guided_hint": "Integrate (4 - x^2) from -2 to 2.",
        "guided_answer": "32/3",
        "independent_question": "Find the area between y = 2x and y = x^2.",
        "independent_answer": "4/3",
        "xp": 350
    },
    {
        "level_id": 7,
        "concept": "IB AA HL Boss Battle: Multi-step Integration combining substitution, definite limits, and precise symbolic evaluation.",
        "formula": "\\text{Combined Techniques}",
        "method": "Execute substitution, adjust integration limits accordingly, and simplify final exact values.",
        "worked_example": "Evaluate \\int_{0}^{\\sqrt{\\pi}} 2x \\cos(x^2) dx. Let u = x^2 -> Limits: 0 to \\pi. \\int_0^\\pi \\cos(u) du = [\\sin u]_0^\\pi = 0.",
        "guided_question": "Evaluate \\int_{0}^{1} x e^{x^2} dx.",
        "guided_hint": "Let u = x^2, du = 2x dx. Limits change from 0 to 1.",
        "guided_answer": "(exp(1) - 1)/2",
        "independent_question": "Find \\int_{1}^{e} \\frac{\\ln(x)}{x} dx.",
        "independent_answer": "1/2",
        "xp": 500
    }
]

# ==========================================
# 3. UTILITY FUNCTIONS (Progress & SymPy)
# ==========================================

PROGRESS_FILE = "user_progress.json"
DEFAULT_PROGRESS = {
    "xp": 0,
    "streak": 0,
    "unlocked_level": 1,
    "completed_levels": [],
    "questions_answered": 0,
    "correct_answers": 0,
    "history": []
}

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        save_progress(DEFAULT_PROGRESS)
        return DEFAULT_PROGRESS.copy()
    try:
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_PROGRESS.copy()

def save_progress(progress_data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress_data, f, indent=4)

def record_answer(is_correct, xp_gained=0):
    progress = load_progress()
    progress["questions_answered"] += 1
    if is_correct:
        progress["correct_answers"] += 1
        progress["streak"] += 1
        progress["xp"] += xp_gained
    else:
        progress["streak"] = 0
    save_progress(progress)
    return progress

def unlock_next_level(current_level):
    progress = load_progress()
    if current_level not in progress["completed_levels"]:
        progress["completed_levels"].append(current_level)
    if progress["unlocked_level"] <= current_level:
        progress["unlocked_level"] = current_level + 1
    save_progress(progress)
    return progress

def clean_input(expr_str: str) -> str:
    expr_str = expr_str.strip()
    expr_str = expr_str.replace("\\ln", "ln").replace("\\sin", "sin").replace("\\cos", "cos")
    expr_str = expr_str.replace("^", "**")
    expr_str = expr_str.replace("e**", "exp")
    expr_str = expr_str.replace("\\frac{", "(").replace("}{", ")/(").replace("}", ")")
    return expr_str

def evaluate_equivalence(user_ans: str, correct_ans: str, is_definite: bool = False) -> bool:
    try:
        x, C = sp.symbols('x C', real=True)
        user_clean = clean_input(user_ans)
        correct_clean = clean_input(correct_ans)

        u_sym = sp.sympify(user_clean)
        c_sym = sp.sympify(correct_clean)

        if not is_definite:
            diff_u = sp.diff(u_sym, x)
            diff_c = sp.diff(c_sym, x)
            diff_diff = sp.simplify(diff_u - diff_c)
            if diff_diff == 0:
                return True
            return bool(sp.trigsimp(diff_diff) == 0)
        else:
            diff = sp.simplify(u_sym - c_sym)
            if diff == 0:
                return True
            return bool(sp.trigsimp(diff) == 0)
    except Exception:
        return user_ans.replace(" ", "").lower() == correct_ans.replace(" ", "").lower()

# ==========================================
# 4. UI COMPONENTS & PAGES
# ==========================================

def render_sidebar():
    st.sidebar.title("⚡ Integration Quest")
    st.sidebar.markdown("**IB Mathematics AA HL**")
    st.sidebar.divider()

    progress = load_progress()
    st.sidebar.subheader("👤 Student Profile")
    st.sidebar.metric(label="Total XP", value=f"{progress['xp']} XP")
    st.sidebar.metric(label="Current Streak", value=f"🔥 {progress['streak']} Days")
    st.sidebar.metric(label="Unlocked Level", value=f"Level {progress['unlocked_level']}")
    
    st.sidebar.divider()
    st.sidebar.info("💡 **Tip:** Use `exp(x)` for $e^x$, `*` for multiplication, and `^` or `**` for exponents when typing math answers.")

def render_level_card(level_data, is_unlocked, is_completed):
    status_badge = "✅ Completed" if is_completed else ("🔓 Unlocked" if is_unlocked else "🔒 Locked")
    card_class = "quest-card" if is_unlocked else "quest-card level-locked"

    st.markdown(
        f"""
        <div class="{card_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="card-header">{level_data['title']}</div>
                <span style="font-size: 0.85rem; font-weight: bold; color: {'#00f5d4' if is_unlocked else '#a0aec0'};">
                    {status_badge}
                </span>
            </div>
            <div style="color: #9d4edd; font-weight: 600; margin-bottom: 4px;">{level_data['topic']}</div>
            <div class="card-subtitle">{level_data['description']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_pedagogical_flow(q_data):
    st.markdown(f"## 🎯 {q_data.get('topic', 'Level Integration Challenge')}")

    tabs = st.tabs([
        "1. Concept Learn",
        "2. Formula Sheet",
        "3. Method",
        "4. Worked Example",
        "5. Guided Practice",
        "6. Independent Practice",
        "7. Level Mastery"
    ])

    with tabs[0]:
        st.subheader("💡 Concept")
        st.write(q_data["concept"])

    with tabs[1]:
        st.subheader("📜 IB Formula Sheet Reference")
        st.latex(q_data["formula"])

    with tabs[2]:
        st.subheader("🛠️ Step-by-Step Method")
        st.markdown(q_data["method"])

    with tabs[3]:
        st.subheader("✍️ Worked Example")
        st.info(q_data["worked_example"])

    with tabs[4]:
        st.subheader("🤝 Guided Practice")
        st.write(q_data["guided_question"])
        with st.expander("💡 Need a Hint?"):
            st.write(q_data["guided_hint"])

        guided_input = st.text_input("Your Answer (Guided):", key=f"guided_{q_data['level_id']}")
        if st.button("Check Guided Answer", key=f"btn_g_{q_data['level_id']}"):
            is_def = q_data["level_id"] in [5, 6, 7]
            if evaluate_equivalence(guided_input, q_data["guided_answer"], is_definite=is_def):
                st.success("Correct! Great job following the guided steps.")
            else:
                st.error("Not quite. Review the hint and try again!")

    with tabs[5]:
        st.subheader("🚀 Independent Practice")
        st.write(q_data["independent_question"])

        ind_input = st.text_input("Your Final Answer:", key=f"ind_{q_data['level_id']}")
        if st.button("Submit Independent Answer", key=f"btn_ind_{q_data['level_id']}"):
            is_def = q_data["level_id"] in [5, 6, 7]
            if evaluate_equivalence(ind_input, q_data["independent_answer"], is_definite=is_def):
                st.success("🎯 Perfect! You solved it correctly!")
                record_answer(True, xp_gained=q_data["xp"])
                st.session_state[f"level_{q_data['level_id']}_passed"] = True
            else:
                st.error("Incorrect answer. Double check your calculus operations!")
                record_answer(False)

    with tabs[6]:
        st.subheader("🏆 Level Completion")
        if st.session_state.get(f"level_{q_data['level_id']}_passed", False):
            st.success(f"Level {q_data['level_id']} Completed! You earned {q_data['xp']} XP.")
            if st.button("Unlock Next Level 🔓"):
                unlock_next_level(q_data["level_id"])
                st.success("Next level unlocked! Return to the Dashboard to proceed.")
        else:
            st.warning("Complete the Independent Practice question correctly to master this level and unlock the next!")

# ==========================================
# 5. PAGE VIEWS
# ==========================================

def show_dashboard():
    st.title("🗺️ Quest Dashboard")
    st.markdown("Welcome to your IB Mathematics AA HL Integration Journey.")

    progress = load_progress()

    for lvl in LEVELS_DATA:
        lvl_id = lvl["id"]
        is_unlocked = lvl_id <= progress["unlocked_level"]
        is_completed = lvl_id in progress["completed_levels"]

        col1, col2 = st.columns([4, 1])
        with col1:
            render_level_card(lvl, is_unlocked, is_completed)
        with col2:
            st.write("")
            st.write("")
            if is_unlocked:
                if st.button(f"Enter L{lvl_id}", key=f"enter_{lvl_id}"):
                    st.session_state["selected_level"] = lvl_id
                    st.session_state["nav_page"] = "Integration Quest"
                    st.rerun()
            else:
                st.button("🔒 Locked", key=f"lock_{lvl_id}", disabled=True)

def show_integration():
    st.title("🧮 Integration Quest Arena")
    level_id = st.session_state.get("selected_level", 1)
    q_data = next((q for q in QUESTIONS_DATA if q["level_id"] == level_id), QUESTIONS_DATA[0])

    st.caption(f"Currently Playing: Level {level_id}")
    render_pedagogical_flow(q_data)

def show_differentiation():
    st.title("⚡ Differentiation Module")
    st.info("🔒 This module is currently locked. It will be released in a future content expansion for IB Math AA HL!")
    st.markdown(
        """
        <div class="quest-card" style="text-align: center; padding: 40px;">
            <h3>🚧 Coming Soon 🚧</h3>
            <p>Topics including Product Rule, Quotient Rule, Chain Rule, Implicit Differentiation, and Related Rates will be unlocked here.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def show_notes():
    st.title("📚 Notes & Formula Reference")
    st.markdown("Searchable IB Mathematics AA HL Formula Drawer.")

    search_term = st.text_input("🔍 Search formulas, topics, or methods:", "")

    filtered_notes = [
        n for n in NOTES_DATA 
        if search_term.lower() in n["title"].lower() 
        or search_term.lower() in n["category"].lower()
        or search_term.lower() in n["note"].lower()
    ]

    for item in filtered_notes:
        with st.expander(f"📌 [{item['category']}] {item['title']}"):
            st.latex(item["formula"])
            st.write(f"**Note:** {item['note']}")

def show_practice():
    st.title("🏋️ Free Practice Arena")
    st.markdown("Test your skills across all IB Integration question types.")

    selected_q_idx = st.selectbox(
        "Select a Practice Problem:", 
        options=range(len(QUESTIONS_DATA)),
        format_func=lambda i: f"Level {QUESTIONS_DATA[i]['level_id']}: {QUESTIONS_DATA[i]['concept'][:40]}..."
    )

    q = QUESTIONS_DATA[selected_q_idx]
    st.markdown(f"### Question (Level {q['level_id']})")
    st.write(q["independent_question"])

    user_ans = st.text_input("Your Answer:", key="free_practice_ans")
    if st.button("Submit Answer"):
        is_def = q["level_id"] in [5, 6, 7]
        if evaluate_equivalence(user_ans, q["independent_answer"], is_definite=is_def):
            st.success("🎉 Correct!")
            record_answer(True, xp_gained=25)
        else:
            st.error("❌ Incorrect. Try again!")
            record_answer(False)

def show_progress():
    st.title("📊 Progress & Analytics")
    progress = load_progress()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total XP", f"{progress['xp']} XP")
    with col2:
        st.metric("Current Streak", f"{progress['streak']} Days")
    with col3:
        total_q = progress["questions_answered"]
        acc = f"{(progress['correct_answers'] / total_q * 100):.1f}%" if total_q > 0 else "0%"
        st.metric("Overall Accuracy", acc)

    st.divider()
    st.subheader("Level Completion History")
    st.write(f"Completed Levels: {progress['completed_levels']}")
    st.write(f"Highest Level Unlocked: Level {progress['unlocked_level']}")

# ==========================================
# 6. MAIN ROUTING & EXECUTION
# ==========================================

render_sidebar()

if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "Dashboard"

nav_options = [
    "Dashboard",
    "Integration Quest",
    "Differentiation (Coming Soon)",
    "Notes & Formulas",
    "Free Practice",
    "Progress & Analytics"
]

selected_page = st.sidebar.radio("Navigation", nav_options, index=nav_options.index(st.session_state["nav_page"]))
st.session_state["nav_page"] = selected_page

if selected_page == "Dashboard":
    show_dashboard()
elif selected_page == "Integration Quest":
    show_integration()
elif selected_page == "Differentiation (Coming Soon)":
    show_differentiation()
elif selected_page == "Notes & Formulas":
    show_notes()
elif selected_page == "Free Practice":
    show_practice()
elif selected_page == "Progress & Analytics":
    show_progress()
