"""
AI Productivity Assistant — Streamlit Edition
=============================================
A web-based productivity suite powered by Gemini 3.5 Flash.

Tools:
  1. Smart Email Generator
  2. Meeting Notes Summarizer
  3. AI Task Planner / Scheduler
  4. AI Research Assistant
  5. AI Workplace Chatbot

Deploy-ready for Streamlit Cloud.
"""

import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
load_dotenv()

MODEL_NAME = "gemini-3.5-flash"
DISCLAIMER = (
    "⚠️ **Responsible AI Notice:** AI-generated content may contain errors or biases. "
    "Always review, validate, and edit outputs before professional use."
)

st.set_page_config(
    page_title="AI Productivity Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ------------------------------------------------------------------
# API Key handling — works on BOTH Streamlit Cloud AND locally
# ------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_client(api_key: str) -> genai.Client:
    """Create and cache the GenAI client."""
    return genai.Client(api_key=api_key)


def resolve_api_key() -> str | None:
    """
    Priority order:
      1. Streamlit secrets (st.secrets) — used on Streamlit Cloud
      2. Environment variable — used locally via .env
    """
    # 1. Streamlit Cloud secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except (FileNotFoundError, KeyError):
        pass

    # 2. Local .env
    return os.getenv("GEMINI_API_KEY")


# ------------------------------------------------------------------
# Gemini call helper (for single-shot prompts)
# ------------------------------------------------------------------
def call_gemini(prompt: str, system_instruction: str | None = None,
                temperature: float = 0.7) -> str:
    """Send a single prompt to Gemini and return text. Handles errors gracefully."""
    client = get_client(st.session_state["api_key"])
    try:
        config = types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=system_instruction,
        )
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=config,
        )
        return response.text.strip()
    except Exception as exc:
        return f"❌ **Error:** {exc}"


# ------------------------------------------------------------------
# Sidebar — navigation
# ------------------------------------------------------------------
def render_sidebar() -> str:
    with st.sidebar:
        st.title("🤖 AI Productivity")
        st.caption("Powered by **Gemini 3.5 Flash**")
        st.caption(f"📅 {datetime.now():%d %b %Y}")
        st.divider()

        tool = st.radio(
            "Choose a tool",
            [
                "📧 Smart Email Generator",
                "📝 Meeting Notes Summarizer",
                "📅 AI Task Planner",
                "🔎 AI Research Assistant",
                "💬 AI Workplace Chatbot",
            ],
            label_visibility="collapsed",
        )

        st.divider()
        st.caption("⚠️ Always validate AI output before professional use.")
        return tool


# ------------------------------------------------------------------
# Tool 1 — Smart Email Generator
# ------------------------------------------------------------------
def page_email():
    st.header("📧 Smart Email Generator")
    st.caption("Generate context-aware professional emails with tone and audience control.")

    with st.form("email_form"):
        col1, col2 = st.columns(2)
        with col1:
            recipient = st.selectbox("Recipient", ["client", "manager", "team", "colleague"])
        with col2:
            tone = st.selectbox("Tone", ["formal", "informal", "persuasive", "friendly", "apologetic"])

        subject = st.text_input("Subject / Purpose", placeholder="e.g. Follow-up on project proposal")
        key_points = st.text_area(
            "Key points to include",
            placeholder="One point per line, or separated by semicolons",
            height=120,
        )

        submitted = st.form_submit_button("✨ Generate Email", use_container_width=True)

    if submitted:
        if not subject.strip():
            st.warning("Please enter a subject.")
            return

        prompt = f"""You are a professional business communication assistant.

Write a complete, ready-to-send email:
- Recipient type: {recipient}
- Tone: {tone}
- Subject/purpose: {subject}
- Key points: {key_points or "None specified"}

Requirements:
1. Include a clear subject line.
2. Appropriate greeting and sign-off for the recipient.
3. Concise body (3–5 short paragraphs).
4. Tone must match "{tone}".
5. End with a clear call to action.
6. Output ONLY the email — no commentary."""

        with st.spinner("Drafting your email…"):
            result = call_gemini(prompt, temperature=0.7)

        st.markdown("### 📨 Generated Email")
        st.markdown(result)
        st.info(DISCLAIMER)
        st.download_button("⬇️ Download email", result, file_name="email.txt")


# ------------------------------------------------------------------
# Tool 2 — Meeting Notes Summarizer
# ------------------------------------------------------------------
def page_summarizer():
    st.header("📝 Meeting Notes Summarizer")
    st.caption("Turn messy meeting notes into structured summaries with action items.")

    notes = st.text_area(
        "Paste your raw meeting notes here",
        height=250,
        placeholder="Paste notes…",
    )

    if st.button("✨ Summarise Notes", use_container_width=True):
        if not notes.strip():
            st.warning("Please paste some notes first.")
            return

        prompt = f"""You are an expert meeting-notes analyst.

Analyse the following raw meeting notes:

\"\"\"
{notes}
\"\"\"

Output in this EXACT Markdown structure:

## 📌 Meeting Summary
A 2–3 sentence overview.

## 🔑 Key Points
- Bullet list (max 8).

## ✅ Decisions Made
- Bullet list. If none, write "None recorded."

## 🎯 Action Items
| Action | Owner | Deadline |
|--------|-------|----------|
| ...    | ...   | ...      |

## ⏰ Deadlines & Responsibilities
- Highlight critical deadlines and owners.

Do NOT invent information that isn't in the notes."""

        with st.spinner("Summarising…"):
            result = call_gemini(prompt, temperature=0.4)

        st.markdown("### 📋 Summary")
        st.markdown(result)
        st.info(DISCLAIMER)
        st.download_button("⬇️ Download summary", result, file_name="meeting_summary.md")


# ------------------------------------------------------------------
# Tool 3 — AI Task Planner
# ------------------------------------------------------------------
def page_planner():
    st.header("📅 AI Task Planner / Scheduler")
    st.caption("Build Eisenhower-prioritised day or week plans.")

    col1, col2 = st.columns(2)
    with col1:
        horizon = st.selectbox("Plan for", ["day", "week"])
        hours = st.number_input("Working hours per day", 1, 16, 8)
    with col2:
        priorities = st.text_input("Fixed priorities / constraints", value="None")

    tasks = st.text_area(
        "Your tasks (one per line, or separated with semicolons)",
        height=150,
    )

    if st.button("✨ Build Plan", use_container_width=True):
        if not tasks.strip():
            st.warning("Please list at least one task.")
            return

        prompt = f"""You are a productivity coach and scheduling expert.

Create a structured {horizon} plan:
- Tasks: {tasks}
- Available hours per day: {hours}
- Constraints: {priorities}

Use the Eisenhower Matrix. Output in this EXACT Markdown structure:

## 🧭 Priority Matrix
| Priority | Task | Why |
|----------|------|-----|
| 🔴 Do First | ... | ... |
| 🟡 Schedule | ... | ... |
| 🟢 Delegate / Batch | ... | ... |

## 🗓️ {horizon.title()} Schedule
Time-blocked schedule with realistic estimates.

## 💡 Time-Optimisation Tips
- 3–5 practical suggestions.

## ⚠️ Risks & Watch-outs
- Bottlenecks or overload risks.

Be realistic about what fits in the hours available."""

        with st.spinner("Building your plan…"):
            result = call_gemini(prompt, temperature=0.5)

        st.markdown(f"### 🗓️ Your {horizon.title()} Plan")
        st.markdown(result)
        st.info(DISCLAIMER)
        st.download_button("⬇️ Download plan", result, file_name="plan.md")


# ------------------------------------------------------------------
# Tool 4 — AI Research Assistant
# ------------------------------------------------------------------
def page_research():
    st.header("🔎 AI Research Assistant")
    st.caption("Turn a topic or article into a structured research brief.")

    topic = st.text_area(
        "Topic, article title, or text to research",
        height=200,
        placeholder="e.g. 'Impact of generative AI on customer service in banking'",
    )

    if st.button("✨ Research", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic or text.")
            return

        prompt = f"""You are a senior research analyst.

Analyse this topic/text:

\"\"\"
{topic}
\"\"\"

Output in this EXACT Markdown structure:

## 📖 Overview
2–3 sentence summary for a busy professional.

## 🔑 Key Insights
- 4–6 bullet points of important findings.

## 📊 Implications
- Business / professional implications.

## ✅ Recommendations
- 3–5 actionable recommendations.

## ⚠️ Limitations & Caveats
- Uncertainties, missing info, or potential bias.

Keep language simple and jargon-free."""

        with st.spinner("Researching…"):
            result = call_gemini(prompt, temperature=0.5)

        st.markdown("### 📄 Research Brief")
        st.markdown(result)
        st.info(DISCLAIMER)
        st.download_button("⬇️ Download brief", result, file_name="research_brief.md")


# ------------------------------------------------------------------
# Tool 5 — AI Chatbot  (CORRECTED — uses types.Content & types.Part)
# ------------------------------------------------------------------
def page_chatbot():
    st.header("💬 AI Workplace Assistant")
    st.caption("Have an interactive conversation with Gemini.")

    system_instruction = (
        "You are a helpful, professional workplace AI assistant. "
        "You help with drafting, planning, researching, and productivity tasks. "
        "Be concise, structured, and practical. Remind the user to validate "
        "important information before acting on it."
    )

    # Initialise chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Clear button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # Render past messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask me anything…")
    if user_input:
        # Show user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # ------------------------------------------------------------------
        # Build contents in the format the SDK expects:
        # a list of types.Content(role=..., parts=[types.Part.from_text(...)])
        # ------------------------------------------------------------------
        contents = []
        for m in st.session_state.chat_history:
            role = "user" if m["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=m["content"])],
                )
            )

        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    client = get_client(st.session_state["api_key"])
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            temperature=0.7,
                            system_instruction=system_instruction,
                        ),
                    )
                    reply = response.text.strip()
                except Exception as exc:
                    reply = f"❌ **Error:** {exc}"

            st.markdown(reply)
            st.session_state.chat_history.append(
                {"role": "assistant", "content": reply}
            )


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    # Resolve API key once per session
    if "api_key" not in st.session_state:
        key = resolve_api_key()
        if not key:
            st.error(
                "### ❌ GEMINI_API_KEY not configured\n\n"
                "**On Streamlit Cloud:** go to your app → **Settings → Secrets** "
                "and add:\n\n"
                "```toml\nGEMINI_API_KEY = \"AIzaSy...\"\n```\n\n"
                "**Locally:** create a `.env` file with "
                "`GEMINI_API_KEY=AIzaSy...`"
            )
            st.stop()
        st.session_state["api_key"] = key

    tool = render_sidebar()

    if tool.startswith("📧"):
        page_email()
    elif tool.startswith("📝"):
        page_summarizer()
    elif tool.startswith("📅"):
        page_planner()
    elif tool.startswith("🔎"):
        page_research()
    elif tool.startswith("💬"):
        page_chatbot()


if __name__ == "__main__":
    main()
