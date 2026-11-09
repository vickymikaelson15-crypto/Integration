import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Integration Quest - IB Math AA",
    page_icon="積分",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for strict Dark Mode and high contrast visibility
st.markdown("""
    <style>
    /* Global Dark Theme Styling */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        color: #e0e0e0;
    }
    
    /* Input & Widget styling */
    div.stMarkdown, div.stButton, div.stRadio, div.stSelectbox {
        color: #e0e0e0;
    }
    
    /* Fix text visibility in headers, labels, and text */
    h1, h2, h3, h4, h5, h6, p, span, label, .stRadio label {
        color: #f0f6fc !important;
    }
    
    /* Success / Info boxes */
    .stAlert {
        background-color: #1f2937;
        color: #f3f4f6;
        border: 1px solid #374151;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("积分 Integration Quest 🚀 (IB Math AA HL/SL)")
st.markdown("Master indefinite integrals, substitution, integration by parts, definite integrals, areas, volumes, and differential equations with interactive practice and comprehensive formula stops.")

# Sidebar Navigation
st.sidebar.title("🧭 Navigation")
app_mode = st.sidebar.radio("Choose Section", ["📚 Notes & Formula Stops", "📝 Practice Question Bank", "🏆 Quest Dashboard"])

# ---------------------------------------------------------
# SECTION 1: NOTES & FORMULA STOPS
# ---------------------------------------------------------
if app_mode == "📚 Notes & Formula Stops":
    st.header("📚 Calculus Notes & Formula Stops")
    st.markdown("Comprehensive reference guide compiled from IB Math AA lecture notes (Christos Nikolaidis).")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Basic & Standard", "Substitution & Parts", "Definite & Areas/Volumes", "Differential Equations", "Maclaurin Series"])
    
    with tab1:
        st.subheader("1. Basic Indefinite Integrals & Standard Formulas")
        st.markdown("An indefinite integral reverses differentiation, adding a constant of integration $C$.")
        
        st.markdown("""
        * $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C \\quad (n \\neq -1)$[cite: 461]
        * $\\int \\frac{1}{x} dx = \\ln|x| + C$[cite: 463]
        * $\\int e^x dx = e^x + C$[cite: 461]
        * $\\int \\sin x dx = -\\cos x + C$[cite: 461]
        * $\\int \\cos x dx = \\sin x + C$[cite: 461]
        * $\\int \\sec^2 x dx = \\tan x + C$[cite: 525]
        * $\\int \\csc^2 x dx = -\\cot x + C$[cite: 525]
        * $\\int \\frac{1}{a^2 + x^2} dx = \\frac{1}{a} \\arctan\\left(\\frac{x}{a}\\right) + C$[cite: 523]
        * $\\int \\frac{1}{\\sqrt{a^2 - x^2}} dx = \\arcsin\\left(\\frac{x}{a}\\right) + C$[cite: 523]
        """)
        
        st.markdown("#### Linearity Rules")
        st.markdown("""
        * $\\int [f(x) \\pm g(x)] dx = \\int f(x)dx \\pm \\int g(x)dx$[cite: 463]
        * $\\int k f(x) dx = k \\int f(x) dx$[cite: 463]
        """)

    with tab2:
        st.subheader("2. Integration Techniques (Substitution & By Parts)")
        
        st.markdown("#### Integration by Substitution (Anti-Chain Rule)")
        st.markdown("""
        * $\\int [f(x)]^n f'(x) dx = \\frac{[f(x)]^{n+1}}{n+1} + C$[cite: 528]
        * $\\int \\frac{f'(x)}{f(x)} dx = \\ln|f(x)| + C$[cite: 527]
        * Linear case: $\\int f(ax+b)dx = \\frac{1}{a} F(ax+b) + C$[cite: 465]
        """)
        
        st.markdown("#### Integration by Parts")
        st.markdown("""
        $$\\int u \\frac{dv}{dx} dx = uv - \\int v \\frac{du}{dx} dx$$[cite: 533]
        * **Priority list for $v'$ (integration choice):** 
          1. $e^{ax}, \\sin(ax), \\cos(ax)$[cite: 521]
          2. $x^n$ (polynomials)[cite: 521]
          3. $\\ln x, \\arctan x, \\arcsin x$[cite: 521]
        """)

    with tab3:
        st.subheader("3. Definite Integrals, Areas & Volumes of Revolution")
        st.markdown("""
        * **Definite Integral:** $\\int_a^b f(x)dx = [F(x)]_a^b = F(b) - F(a)$[cite: 473]
        * **Area between curve and x-axis:** $A = \\int_a^b |f(x)| dx$[cite: 480]
        * **Area between two curves:** $A = \\int_a^b |f(x) - g(x)| dx$[cite: 484]
        * **Volume of Revolution (about x-axis):** $V = \\pi \\int_a^b y^2 dx$[cite: 541]
        * **Volume of Revolution (about y-axis):** $V = \\pi \\int_c^d x^2 dy$[cite: 542]
        """)

    with tab4:
        st.subheader("4. Differential Equations")
        st.markdown("""
        * **Separable Variables:** Separate $x$ and $y$ to opposite sides: $f(y)dy = g(x)dx \\implies \\int f(y)dy = \\int g(x)dx$[cite: 546]
        * **First Order Linear D.E.:** $\\frac{dy}{dx} + P(x)y = Q(x)$[cite: 550]
          * **Integrating Factor:** $\\mathcal{I} = e^{\\int P(x)dx}$[cite: 550]
          * **Solution:** $\\mathcal{I} \\cdot y = \\int \\mathcal{I} \\cdot Q(x) dx$[cite: 550]
        * **Euler's Numerical Method:** $x_{n+1} = x_n + h$, \\quad $y_{n+1} = y_n + h \\cdot f(x_n, y_n)$[cite: 552]
        """)

    with tab5:
        st.subheader("5. Maclaurin Series & Binomial Extension")
        st.markdown("""
        * **Maclaurin Series Formula:**
          $$f(x) = f(0) + f'(0)x + \\frac{f''(0)}{2!}x^2 + \\frac{f'''(0)}{3!}x^3 + \\dots$$[cite: 555]
        * **Standard Expansions:**
          * $e^x = 1 + x + \\frac{x^2}{2!} + \\frac{x^3}{3!} + \\dots$[cite: 557]
          * $\\sin x = x - \\frac{x^3}{3!} + \\frac{x^5}{5!} - \\dots$[cite: 557]
          * $\\cos x = 1 - \\frac{x^2}{2!} + \\frac{x^4}{4!} - \\dots$[cite: 557]
        * **Extended Binomial Theorem:**
          $$(1+x)^n = 1 + nx + \\frac{n(n-1)}{2!}x^2 + \\frac{n(n-1)(n-2)}{3!}x^3 + \\dots$$[cite: 561]
        """)

# ---------------------------------------------------------
# SECTION 2: PRACTICE QUESTION BANK
# ---------------------------------------------------------
elif app_mode == "📝 Practice Question Bank":
    st.header("📝 Practice Question Bank")
    st.markdown("Test your skills across all calculus topics with instant verification and step-by-step solutions.")
    
    category = st.selectbox("Select Topic Category", [
        "Basic Indefinite Integrals",
        "Substitution Method",
        "Integration by Parts",
        "Definite Integrals & Areas",
        "Differential Equations & Kinematics"
    ])
    
    if category == "Basic Indefinite Integrals":
        q1 = st.radio("Question 1: Find $\\int (6x^2 + 2x) dx$", [
            "A) $2x^3 + x^2 + C$",
            "B) $6x^3 + 2x^2 + C$",
            "C) $3x^3 + x^2 + C$",
            "D) $x^3 + x^2 + C$"
        ])
        if st.button("Submit Q1 Answer"):
            if "A) $2x^3" in q1:
                st.success("Correct! $\\int 6x^2 dx = 6\\frac{x^3}{3} = 2x^3$, and $\\int 2x dx = 2\\frac{x^2}{2} = x^2$. Result: $2x^3 + x^2 + C$.")
            else:
                st.error("Incorrect. Remember power rule: $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$[cite: 461].")
                
        q2 = st.radio("Question 2: Find $\\int \\left(5 \\sin x - 3 \\cos x - 7e^x + \\frac{1}{x}\\right) dx$", [
            "A) $-5\\cos x - 3\\sin x - 7e^x + \\ln|x| + C$",
            "B) $5\\cos x + 3\\sin x - 7e^x + \\ln|x| + C$",
            "C) $-5\\sin x - 3\\cos x - 7e^x + \\frac{1}{x^2} + C$",
            "D) $5\\sin x - 3\\cos x - 7e^x + \\ln|x| + C$"
        ])
        if st.button("Submit Q2 Answer"):
            if "A) $-5\\cos x" in q2:
                st.success("Correct! $\\int \\sin x dx = -\\cos x$ and $\\int \\cos x dx = \\sin x$[cite: 461].")
            else:
                st.error("Incorrect. Note that $\\int \\sin x dx = -\\cos x$[cite: 461].")

    elif category == "Substitution Method":
        q1 = st.radio("Question 1: Find $\\int 2x\\sqrt{x^2+3} dx$ using $u = x^2+3$", [
            "A) $\\frac{2}{3}(x^2+3)^{3/2} + C$",
            "B) $\\frac{1}{3}(x^2+3)^{3/2} + C$",
            "C) $\\sqrt{x^2+3} + C$",
            "D) $\\frac{3}{2}(x^2+3)^{3/2} + C$"
        ])
        if st.button("Submit Substitution Answer"):
            if "B) $\\frac{1}{3}" in q1:
                st.success("Correct! With $u = x^2+3$, $du = 2x dx$, the integral becomes $\\int u^{1/2} du = \\frac{2}{3}u^{3/2} = \\frac{1}{3}(x^2+3)^{3/2} + C$[cite: 469].")
            else:
                st.error("Incorrect. Remember the coefficient $\\frac{1}{3}$ from integration of $u^{1/2}$[cite: 462, 469].")

    elif category == "Integration by Parts":
        q1 = st.radio("Question 1: Find $\\int 2x e^x dx$", [
            "A) $2xe^x - 2e^x + C$",
            "B) $2xe^x + 2e^x + C$",
            "C) $x^2e^x + C$",
            "D) $2e^x - 2xe^x + C$"
        ])
        if st.button("Submit By Parts Answer"):
            if "A) $2xe^x - 2e^x" in q1:
                st.success("Correct! Using integration by parts with $u = 2x$ and $dv = e^x dx$, we get $2xe^x - \\int 2e^x dx = 2xe^x - 2e^x + C$[cite: 533].")
            else:
                st.error("Incorrect. Check the sign change when integrating $\\int v du$[cite: 533].")

    elif category == "Definite Integrals & Areas":
        q1 = st.radio("Question 1: Evaluate $\\int_0^1 (2x + 3) dx$", [
            "A) 3",
            "B) 4",
            "C) 5",
            "D) 6"
        ])
        if st.button("Submit Definite Integral Answer"):
            if "B) 4" in q1:
                st.success("Correct! $[x^2 + 3x]_0^1 = (1 + 3) - 0 = 4$[cite: 473].")
            else:
                st.error("Incorrect. $\\int_0^1 (2x+3)dx = [x^2+3x]_0^1 = 4$[cite: 473].")

    elif category == "Differential Equations & Kinematics":
        q1 = st.radio("Question 1: Solve $\\frac{dy}{dx} = 4x + 1$ with $y(3) = 1$", [
            "A) $y = 2x^2 + x - 18$",
            "B) $y = 2x^2 + x + 1$",
            "C) $y = 4x^2 + x - 35$",
            "D) $y = 2x^2 + x - 20$"
        ])
        if st.button("Submit D.E. Answer"):
            if "A) $y = 2x^2 + x - 18$" in q1:
                st.success("Correct! $y = \\int (4x+1)dx = 2x^2 + x + C$[cite: 498]. Plugging $y(3)=1 \\implies 2(9) + 3 + C = 1 \\implies 21 + C = 1 \\implies C = -18$[cite: 498].")
            else:
                st.error("Incorrect. Re-evaluate the integration constant $C$ using $y(3)=1$[cite: 498].")

# ---------------------------------------------------------
# SECTION 3: QUEST DASHBOARD
# ---------------------------------------------------------
elif app_mode == "🏆 Quest Dashboard":
    st.header("🏆 Quest Dashboard & Progress")
    st.markdown("Track your calculus mastery and streak!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("❤️ Hearts / Lives", "3 / 3")
    with col2:
        st.metric("✨ Sparkle Points", "30 XP")
    with col3:
        st.metric("🔥 Current Streak", "5 Days")
        
    st.markdown("---")
    st.subheader("🎯 Badges Unlocked")
    st.markdown("""
    * 🟢 **Integration Novice** - Completed Basic Integrals
    * 🟡 **Substitution Master** - Mastered Anti-Chain Rule
    * 🔵 **Differential Expert** - Solved Separable D.E.s
    """)
