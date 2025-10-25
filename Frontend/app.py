import streamlit as st
import requests

# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="Slack AI Agent",
    page_icon="💬",
    layout="wide",
)

# --- Custom CSS for White/Purple Theme ---
st.markdown("""
    <style>
        /* Main background */
        [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #F4F3FF;
        }

        /* Title + Headings */
        h1,
        [data-testid="stMarkdownContainer"] h1 {
            color: #0f172a !important;
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            letter-spacing: -0.5px;
            line-height: 1.2;
            opacity: 1 !important;
            text-shadow: 0 2px 18px rgba(15, 23, 42, 0.08);
        }

        h2, h3, h4, h5, h6,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {
            color: #111827 !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            opacity: 1 !important;
        }

        /* General text */
        body,
        p,
        label,
        span,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] label {
            color: #1f2937 !important;
            font-family: 'Inter', sans-serif;
            opacity: 1 !important;
        }

        /* Field labels */
        [data-testid="stWidgetLabel"] > div {
            color: #1f2937 !important;
            font-weight: 600;
            opacity: 1 !important;
        }

        /* Markdown blocks (summary + misc copy) */
        div[data-testid="stMarkdown"],
        div[data-testid="stMarkdown"] * {
            color: #0f172a !important;
            opacity: 1 !important;
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
        }

        div[data-testid="stMarkdown"] a {
            color: #6C63FF !important;
            text-decoration: underline;
            font-weight: 600;
        }

        /* Buttons */
        div.stButton > button {
            background-color: #6C63FF;
            color: white;
            border: none;
            padding: 0.6em 1.2em;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #5a52e0;
            transform: scale(1.02);
        }

        /* Text Inputs */
        input, textarea {
            border-radius: 8px !important;
        }

        /* Info/Success/Error boxes */
        .stAlert {
            border-radius: 8px;
            background-color: #F4F3FF !important;
            color: #2B2B2B !important;
        }

        /* Footer */
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("💬 Slack AI Summarizer")
st.write("Generate daily summaries from your team’s Slack conversations — powered by LangChain + FastAPI.")

# --- Inputs ---
col1, col2 = st.columns([2, 1])
with col1:
    channel = st.text_input("🔗 Slack Channel ID", placeholder="e.g. C1234567890")
    post_to_slack = st.checkbox("Send summary back to Slack", value=False)
with col2:
    st.write("")  # spacing
    summarize_btn = st.button("Generate Summary")

# --- Fetch and Display Summary ---
if summarize_btn:
    st.info("Fetching messages and generating AI summary... please wait.")
    try:
        response = requests.post(
            "http://127.0.0.1:8000/summarize",
            json={
                "channel_id": channel.strip(),
                "post_to_slack": post_to_slack,
            },
            timeout=20
        )
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Summary generated successfully!")
            st.markdown("---")
            st.subheader("📋 Team Summary")
            st.markdown(data["summary"])
        else:
            st.error("❌ Failed to fetch summary. Check your backend connection.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# --- Footer ---
st.markdown(
    "<p style='text-align:center;color:#888;'>Built with ❤️ using FastAPI, LangChain, and Streamlit.</p>",
    unsafe_allow_html=True
)
