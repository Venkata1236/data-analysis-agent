# streamlit_app.py
# Data Analysis Agent — Streamlit Web UI

import os
import streamlit as st
from dotenv import load_dotenv
from core.data_loader import load_csv_from_bytes, get_dataframe_info, get_filename
from core.agent import create_agent, run_analysis

# ── Load API key ──────────────────────────────────────────────
try:
    api_key = st.secrets.get("OPENAI_API_KEY", "")
except:
    api_key = os.environ.get("OPENAI_API_KEY", "")

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Data Analysis Agent",
    page_icon="📊",
    layout="centered"
)

# ── Header ────────────────────────────────────────────────────
st.title("📊 Data Analysis Agent")
st.caption("Upload a CSV — ask questions in plain English — powered by custom LangChain tools")
st.divider()

# ── Session state ─────────────────────────────────────────────
if "agent" not in st.session_state:
    st.session_state.agent = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "df_loaded" not in st.session_state:
    st.session_state.df_loaded = False

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    max_iterations = st.slider("Max tool calls", min_value=3, max_value=10, value=8)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

    st.divider()
    st.subheader("🛠️ Custom Tools")
    st.info("📋 **get_dataset_info**\nUnderstand data structure")
    st.info("📈 **calculate_statistics**\nMean, sum, min, max, std")
    st.info("🔍 **filter_data**\nFilter rows by condition")
    st.info("📊 **group_and_aggregate**\nGroup by + sum/mean/count")
    st.info("🏆 **find_top_n**\nTop or bottom N rows")
    st.info("🔗 **calculate_correlation**\nCorrelation between columns")

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


# ── Step 1: Upload CSV ────────────────────────────────────────
st.subheader("📂 Step 1 — Upload CSV")

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"],
    help="Upload any CSV file — sales data, survey results, financial data, etc."
)

# Use sample data button
col1, col2 = st.columns(2)
with col1:
    use_sample = st.button("📊 Use Sample Sales Data", use_container_width=True)

if use_sample:
    try:
        with open("sample_data/sales_data.csv", "rb") as f:
            file_bytes = f.read()
        load_csv_from_bytes(file_bytes, "sales_data.csv")
        st.session_state.df_loaded = True
        st.session_state.agent = None
        st.session_state.chat_history = []
        st.success("✅ Sample sales data loaded!")
    except Exception as e:
        st.error(f"❌ Error loading sample data: {e}")

if uploaded_file:
    try:
        file_bytes = uploaded_file.read()
        load_csv_from_bytes(file_bytes, uploaded_file.name)
        st.session_state.df_loaded = True
        st.session_state.agent = None
        st.session_state.chat_history = []
        st.success(f"✅ {uploaded_file.name} loaded successfully!")
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")

# Show dataset info if loaded
if st.session_state.df_loaded:
    with st.expander("📋 Dataset Overview"):
        st.text(get_dataframe_info())

    st.divider()

    # ── Step 2: Initialize Agent ──────────────────────────────
    st.subheader("⚡ Step 2 — Initialize Agent")

    if st.button("🚀 Initialize Agent", type="primary", use_container_width=True):
        if not api_key:
            st.error("❌ API key not found. Check your .env file.")
        else:
            with st.spinner("Loading 6 custom tools and agent..."):
                st.session_state.agent = create_agent(
                    api_key=api_key,
                    temperature=temperature,
                    max_iterations=max_iterations
                )
                st.session_state.chat_history = []
            st.success("✅ Agent ready with 6 custom tools!")

    st.divider()

    # ── Step 3: Ask Questions ─────────────────────────────────
    if st.session_state.agent:
        st.subheader(f"💬 Step 3 — Ask Questions about {get_filename()}")

        # Example questions
        st.caption("💡 Try these questions:")
        example_questions = [
            "What are the total sales by category?",
            "Who is the top salesperson by total sales?",
            "Show me top 5 products by total sales",
            "What is the average order value?",
            "What is the correlation between quantity and total sales?",
            "Filter orders where total_sales > 2000"
        ]

        cols = st.columns(2)
        for i, q in enumerate(example_questions):
            with cols[i % 2]:
                if st.button(q, use_container_width=True, key=f"q{i}"):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    with st.spinner("🤔 Analyzing..."):
                        result = run_analysis(st.session_state.agent, q)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": result["answer"],
                            "steps": result["steps"]
                        })
                    st.rerun()

        st.divider()

        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if msg["role"] == "assistant":
                    steps = msg.get("steps", [])
                    if steps:
                        with st.expander(f"🔧 Tools used — {len(steps)} calls"):
                            for idx, step in enumerate(steps, 1):
                                action, observation = step
                                st.markdown(f"**Step {idx} — `{action.tool}`**")
                                st.markdown(f"Input: `{str(action.tool_input)[:200]}`")
                                st.markdown(f"Result: {str(observation)[:400]}")
                                if idx < len(steps):
                                    st.divider()

        # Chat input
        question = st.chat_input("Ask anything about your data...")

        if question:
            with st.chat_message("user"):
                st.write(question)
            st.session_state.chat_history.append({"role": "user", "content": question})

            with st.chat_message("assistant"):
                with st.spinner("🤔 Analyzing your data..."):
                    try:
                        result = run_analysis(st.session_state.agent, question)
                        answer = result["answer"]
                        steps = result["steps"]

                        st.write(answer)

                        if steps:
                            with st.expander(f"🔧 Tools used — {len(steps)} calls"):
                                for idx, step in enumerate(steps, 1):
                                    action, observation = step
                                    st.markdown(f"**Step {idx} — `{action.tool}`**")
                                    st.markdown(f"Input: `{str(action.tool_input)[:200]}`")
                                    st.markdown(f"Result: {str(observation)[:400]}")
                                    if idx < len(steps):
                                        st.divider()

                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": answer,
                            "steps": steps
                        })

                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    else:
        st.info("👆 Click **Initialize Agent** to start asking questions.")

else:
    st.info("👆 Upload a CSV file or use the sample data to get started.")