import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroScope AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── NEW MODERN UI THEME ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #e8f0ff;
}

/* Background */
.stApp {
    background: radial-gradient(circle at 20% 10%, #0f1b2d, #05070d);
}

/* Hide Streamlit UI */
#MainMenu, footer, header { visibility: hidden; }

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
}

.hero h1 {
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -1px;
}

.hero h1 span {
    color: #00e5ff;
}

.hero p {
    color: #9fb3c8;
    max-width: 600px;
    margin: auto;
}

/* ── INPUT CARD ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
}

/* INPUT */
.stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: white !important;
}

/* BUTTON */
.stButton button {
    background: linear-gradient(90deg, #00e5ff, #7c4dff);
    color: #000;
    font-weight: 700;
    border-radius: 10px;
    width: 100%;
}

/* PIPELINE */
.step {
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.08);
}
.step.done { border-color: #00e5ff; }
.step.active { border-color: #7c4dff; }

/* RESULT BOX */
.result {
    background: rgba(255,255,255,0.03);
    padding: 1.5rem;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Neuro<span>Scope</span> AI</h1>
    <p>Multi-agent intelligence system that researches, analyzes, and generates structured knowledge reports.</p>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT ───────────────────────────────────────────────────
col1, col2 = st.columns([5, 4])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    topic = st.text_input("Enter Research Topic")
    run_btn = st.button("Run Intelligence Pipeline")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### Agent Pipeline")

    r = st.session_state.get("results", {})

    def step(name):
        if name in r:
            st.markdown(f'<div class="step done">{name} ✔</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="step">{name}</div>', unsafe_allow_html=True)

    step("Search Agent")
    step("Reader Agent")
    step("Writer Agent")
    step("Critic Agent")

# ── RUN PIPELINE ─────────────────────────────────────────────
if run_btn and topic:
    st.session_state.results = {}

    with st.spinner("Searching knowledge base..."):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", topic)]
        })
        st.session_state.results["search"] = sr["messages"][-1].content

    with st.spinner("Reading sources..."):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user", st.session_state.results["search"])]
        })
        st.session_state.results["reader"] = rr["messages"][-1].content

    with st.spinner("Writing report..."):
        st.session_state.results["writer"] = writer_chain.invoke({
            "topic": topic,
            "research": str(st.session_state.results)
        })

    with st.spinner("Critiquing output..."):
        st.session_state.results["critic"] = critic_chain.invoke({
            "report": st.session_state.results["writer"]
        })

# ── OUTPUT ───────────────────────────────────────────────────
r = st.session_state.get("results", {})

if "writer" in r:
    st.markdown("## Final Report")
    st.markdown(f'<div class="result">{r["writer"]}</div>', unsafe_allow_html=True)

if "critic" in r:
    st.markdown("## Critic Feedback")
    st.markdown(f'<div class="result">{r["critic"]}</div>', unsafe_allow_html=True)