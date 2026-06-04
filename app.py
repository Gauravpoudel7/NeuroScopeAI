import streamlit as st

from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroScope AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# STYLING
# ─────────────────────────────────────────────
st.markdown("""
<style>

/* =========================
   GLOBAL BACKGROUND
========================= */
.stApp {
    background: radial-gradient(circle at 20% 10%, #0b1220, #05070d);
    font-family: 'Inter', sans-serif;
}

/* Floating neon blobs */
.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    width: 450px;
    height: 450px;
    border-radius: 50%;
    filter: blur(140px);
    opacity: 0.35;
    z-index: -1;
    animation: float 14s infinite ease-in-out;
}

.stApp::before {
    background: #00e5ff;
    top: 10%;
    left: -10%;
}

.stApp::after {
    background: #7c4dff;
    bottom: 10%;
    right: -10%;
    animation-delay: 6s;
}

@keyframes float {
    0% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(40px) scale(1.1); }
    100% { transform: translateY(0px) scale(1); }
}

/* =========================
   HERO
========================= */
.hero {
    text-align: center;
    padding: 3rem 1rem 1.5rem;
}

.hero h1 {
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: -2px;
}

.hero h1 span {
    background: linear-gradient(90deg, #00e5ff, #7c4dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #a9b8d1;
    max-width: 700px;
    margin: auto;
    font-size: 1.05rem;
}

/* =========================
   CARD (GLASSMORPHISM)
========================= */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1.5rem;
    backdrop-filter: blur(18px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 30px 80px rgba(0,0,0,0.6);
}

/* =========================
   INPUT
========================= */
.stTextInput input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: white !important;
    padding: 12px !important;
}

/* =========================
   BUTTON
========================= */
.stButton button {
    background: linear-gradient(135deg, #00e5ff, #7c4dff);
    color: #0b0f1a;
    font-weight: 700;
    border-radius: 12px;
    width: 100%;
    padding: 0.7rem;
    border: none;
    box-shadow: 0 10px 30px rgba(124,77,255,0.25);
    transition: all 0.2s ease;
}

.stButton button:hover {
    transform: scale(1.03);
    box-shadow: 0 15px 40px rgba(0,229,255,0.25);
}

/* =========================
   PIPELINE STEPS
========================= */
.step {
    padding: 1rem;
    margin-bottom: 0.6rem;
    border-radius: 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.2s ease;
}

.step.done {
    border-color: #00e5ff;
    background: rgba(0,229,255,0.08);
    box-shadow: 0 0 20px rgba(0,229,255,0.15);
}

.step:hover {
    transform: translateX(5px);
}

/* =========================
   OUTPUT BOX
========================= */
.result {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 1.8rem;
    border-radius: 18px;
    backdrop-filter: blur(16px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Neuro<span>Scope</span> AI</h1>
    <p>
        Enterprise-grade multi-agent intelligence system for autonomous research, reasoning, and structured report generation.
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────
left, right = st.columns([5, 4])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    topic = st.text_input(
        "Enter Research Topic",
        placeholder="Example: Future of Generative AI"
    )

    run_btn = st.button("Run Intelligence Pipeline")

    st.markdown('</div>', unsafe_allow_html=True)

with right:

    st.markdown("### Agent Pipeline")

    results = st.session_state.get("results", {})

    def pipeline_step(label, key):
        if key in results:
            st.markdown(
                f'<div class="step done">{label} ✔</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="step">{label}</div>',
                unsafe_allow_html=True
            )

    pipeline_step("Search Agent", "search")
    pipeline_step("Reader Agent", "reader")
    pipeline_step("Writer Agent", "writer")
    pipeline_step("Critic Agent", "critic")

# ─────────────────────────────────────────────
# RUN PIPELINE
# ─────────────────────────────────────────────
if run_btn and topic:

    st.session_state.results = {}

    # SEARCH
    try:

        with st.spinner("🔍 Search Agent Working..."):

            search_agent = build_search_agent()

            search_response = search_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            topic
                        )
                    ]
                }
            )

            st.session_state.results["search"] = (
                search_response["messages"][-1].content
            )

    except Exception as e:
        st.error(f"Search Agent Error:\n{e}")

    # READER
    try:

        with st.spinner("📚 Reader Agent Working..."):

            reader_agent = build_reader_agent()

            reader_response = reader_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"""
Analyze and summarize the following research:

{st.session_state.results.get('search', '')}
"""
                        )
                    ]
                }
            )

            st.session_state.results["reader"] = (
                reader_response["messages"][-1].content
            )

    except Exception as e:
        st.error(f"Reader Agent Error:\n{e}")

    # WRITER
    try:

        with st.spinner("✍️ Writing Report..."):

            research_text = f"""
SEARCH RESULTS:

{st.session_state.results.get('search', '')}

READER ANALYSIS:

{st.session_state.results.get('reader', '')}
"""

            report = writer_chain.invoke(
                {
                    "topic": topic,
                    "research": research_text,
                }
            )

            st.session_state.results["writer"] = report

    except Exception as e:
        st.error(f"Writer Error:\n{e}")

    # CRITIC
    try:

        with st.spinner("🧐 Critiquing Report..."):

            critique = critic_chain.invoke(
                {
                    "report": st.session_state.results.get(
                        "writer",
                        ""
                    )
                }
            )

            st.session_state.results["critic"] = critique

    except Exception as e:
        st.error(f"Critic Error:\n{e}")

# ─────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────
results = st.session_state.get("results", {})

if "writer" in results:

    st.markdown("## 📄 Final Research Report")

    st.markdown(
        f"""
<div class="result">
{results['writer']}
</div>
""",
        unsafe_allow_html=True
    )

if "critic" in results:

    st.markdown("## 🧐 Critic Feedback")

    st.markdown(
        f"""
<div class="result">
{results['critic']}
</div>
""",
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────
# DEBUG SECTION
# ─────────────────────────────────────────────
if results:

    with st.expander("Search Agent Output"):
        st.write(results.get("search", ""))

    with st.expander("Reader Agent Output"):
        st.write(results.get("reader", ""))