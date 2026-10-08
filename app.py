
"""
AI Productivity Assistant — Powered by Gemini 3.5 Flash
========================================================
A command-line productivity suite that automates common workplace tasks:

  1. Smart Email Generator
  2. Meeting Notes Summarizer
  3. AI Task Planner / Scheduler
  4. AI Research Assistant
  5. AI Chatbot Interface

Built with the official google-genai SDK and Gemini 3.5 Flash.
"""

import os
import sys
import textwrap
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.table import Table
from rich.rule import Rule

# ------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------
load_dotenv()

console = Console()

MODEL_NAME = "gemini-3.5-flash"
API_KEY_ENV_VAR = "GEMINI_API_KEY"

DISCLAIMER = (
    "⚠️  Responsible AI Notice: AI-generated content may contain errors or biases. "
    "Always review, validate, and edit outputs before professional use."
)


# ------------------------------------------------------------------
# Client helpers
# ------------------------------------------------------------------
def get_api_key() -> str:
    """Retrieve the Gemini API key from environment variables."""
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        console.print(Panel.fit(
            f"[bold red]API key not found.[/bold red]\n\n"
            f"Set the [cyan]{API_KEY_ENV_VAR}[/cyan] environment variable or create a "
            f"[cyan].env[/cyan] file with:\n\n"
            f"[green]{API_KEY_ENV_VAR}=your_api_key_here[/green]",
            title="Configuration Error",
            border_style="red",
        ))
        sys.exit(1)
    return api_key


def build_client() -> genai.Client:
    """Create and return a Google GenAI client."""
    return genai.Client(api_key=get_api_key())


def generate(
    client: genai.Client,
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.7,
) -> str:
    """
    Send a prompt to Gemini 3.5 Flash and return the text response.

    Includes basic error handling so a single failed call does not crash
    the whole application.
    """
    try:
        config = genai.types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=system_instruction,
        ) if system_instruction else genai.types.GenerateContentConfig(
            temperature=temperature,
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=config,
        )
        return response.text.strip()

    except Exception as exc:
        return f"[ERROR] {exc}"


def show_output(title: str, text: str) -> None:
    """Pretty-print AI output with a panel and disclaimer."""
    console.print()
    console.print(Panel(
        Markdown(text),
        title=f"[bold cyan]{title}[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print(f"[dim]{DISCLAIMER}[/dim]")
    console.print()


# ==================================================================
# TOOL 1 — Smart Email Generator
# ==================================================================
def tool_email_generator(client: genai.Client) -> None:
    console.print(Rule("[bold cyan]📧 Smart Email Generator[/bold cyan]"))

    recipient = Prompt.ask("  Recipient type", choices=["client", "manager", "team", "colleague"], default="client")
    tone = Prompt.ask("  Tone", choices=["formal", "informal", "persuasive", "friendly", "apologetic"], default="formal")
    subject = Prompt.ask("  Subject / purpose of the email")
    key_points = Prompt.ask("  Key points to include (separate with ';')")

    prompt = f"""You are a professional business communication assistant.

Write a complete, ready-to-send email with the following specifications:

- Recipient type: {recipient}
- Tone: {tone}
- Subject/purpose: {subject}
- Key points to include: {key_points}

Requirements:
1. Include a clear subject line.
2. Use an appropriate greeting and sign-off for the recipient type.
3. Keep the body concise (3–5 short paragraphs maximum).
4. Ensure the tone matches the "{tone}" specification.
5. End with a clear call to action or next step.
6. Output only the email — no commentary or explanations."""

    with console.status("[bold green]Drafting email…[/bold green]"):
        result = generate(client, prompt, temperature=0.7)

    show_output("Generated Email", result)


# ==================================================================
# TOOL 2 — Meeting Notes Summarizer
# ==================================================================
def tool_meeting_summarizer(client: genai.Client) -> None:
    console.print(Rule("[bold cyan]📝 Meeting Notes Summarizer[/bold cyan]"))
    console.print("[dim]Paste your raw meeting notes below. Type END on a new line when finished.[/dim]\n")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().upper() == "END":
            break
        lines.append(line)

    raw_notes = "\n".join(lines).strip()
    if not raw_notes:
        console.print("[yellow]No notes provided. Returning to menu.[/yellow]")
        return

    prompt = f"""You are an expert meeting-notes analyst.

Analyse the following raw meeting notes and produce a structured summary.

RAW NOTES:
\"\"\"
{raw_notes}
\"\"\"

Output the summary in this exact structure using Markdown:

## 📌 Meeting Summary
A 2–3 sentence overview of what the meeting was about.

## 🔑 Key Points
- Bullet list of the most important discussion points (max 8).

## ✅ Decisions Made
- Bullet list of decisions agreed upon. If none, write "None recorded."

## 🎯 Action Items
| Action | Owner | Deadline |
|--------|-------|----------|
| ...    | ...   | ...      |

## ⏰ Deadlines & Responsibilities
- Highlight any critical deadlines and who is responsible.

Be concise. Do not invent information that is not in the notes."""

    with console.status("[bold green]Summarising meeting notes…[/bold green]"):
        result = generate(client, prompt, temperature=0.4)

    show_output("Meeting Summary", result)


# ==================================================================
# TOOL 3 — AI Task Planner / Scheduler
# ==================================================================
def tool_task_planner(client: genai.Client) -> None:
    console.print(Rule("[bold cyan]📅 AI Task Planner / Scheduler[/bold cyan]"))

    horizon = Prompt.ask("  Plan for (day/week)", choices=["day", "week"], default="day")
    tasks = Prompt.ask("  List your tasks (separate with ';')")
    hours = Prompt.ask("  Available working hours per day", default="8")
    priorities = Prompt.ask("  Any fixed priorities or constraints?", default="None")

    prompt = f"""You are a productivity coach and scheduling expert.

Create a structured {horizon} plan based on the following:

- Tasks: {tasks}
- Available hours per day: {hours}
- Fixed priorities / constraints: {priorities}

Use the Eisenhower Matrix (Urgency × Importance) to prioritise.

Output in this exact Markdown structure:

## 🧭 Priority Matrix
| Priority | Task | Why |
|----------|------|-----|
| 🔴 Do First | ... | ... |
| 🟡 Schedule | ... | ... |
| 🟢 Delegate / Batch | ... | ... |

## 🗓️ {horizon.title()} Schedule
A time-blocked schedule with realistic time estimates for each task.

## 💡 Time-Optimisation Tips
- 3–5 practical suggestions to reduce context-switching and protect focus time.

## ⚠️ Risks & Watch-outs
- Any bottlenecks or overload risks the user should be aware of.

Be realistic about how much can be done in the available hours."""

    with console.status("[bold green]Building your plan…[/bold green]"):
        result = generate(client, prompt, temperature=0.5)

    show_output(f"{horizon.title()} Plan", result)


# ==================================================================
# TOOL 4 — AI Research Assistant
# ==================================================================
def tool_research_assistant(client: genai.Client) -> None:
    console.print(Rule("[bold cyan]🔎 AI Research Assistant[/bold cyan]"))

    topic = Prompt.ask("  Topic, article title, or text to research")

    prompt = f"""You are a senior research analyst.

Analyse the following topic or text:

\"\"\"
{topic}
\"\"\"

Produce a structured research brief in this exact Markdown format:

## 📖 Overview
A clear 2–3 sentence summary for a busy professional.

## 🔑 Key Insights
- 4–6 bullet points capturing the most important findings.

## 📊 Implications
- What this means for a business or professional context.

## ✅ Recommendations
- 3–5 actionable recommendations based on the analysis.

## ⚠️ Limitations & Caveats
- Note any uncertainties, missing information, or potential biases.

Keep the language simple and jargon-free. If the topic is too broad, focus on the most practical angle."""

    with console.status("[bold green]Researching…[/bold green]"):
        result = generate(client, prompt, temperature=0.5)

    show_output("Research Brief", result)


# ==================================================================
# TOOL 5 — AI Chatbot Interface
# ==================================================================
def tool_chatbot(client: genai.Client) -> None:
    console.print(Rule("[bold cyan]💬 AI Workplace Assistant[/bold cyan]"))
    console.print("[dim]Type /exit to return to the main menu. Type /clear to reset the conversation.[/dim]\n")

    system_instruction = (
        "You are a helpful, professional workplace AI assistant. "
        "You help with drafting, planning, researching, and general productivity tasks. "
        "Be concise, structured, and practical. Always remind the user to validate "
        "important information before acting on it."
    )

    history = []

    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Returning to menu…[/dim]")
            break

        if user_input.strip().lower() == "/exit":
            break
        if user_input.strip().lower() == "/clear":
            history.clear()
            console.print("[yellow]Conversation cleared.[/yellow]\n")
            continue
        if not user_input.strip():
            continue

        history.append({"role": "user", "parts": [user_input]})

        with console.status("[bold green]Thinking…[/bold green]"):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=history,
                    config=genai.types.GenerateContentConfig(
                        temperature=0.7,
                        system_instruction=system_instruction,
                    ),
                )
                reply = response.text.strip()
            except Exception as exc:
                reply = f"[ERROR] {exc}"
                history.pop()
                console.print(f"[red]{reply}[/red]\n")
                continue

        history.append({"role": "model", "parts": [reply]})
        console.print(Panel(Markdown(reply), border_style="cyan", title="Assistant"))
        console.print(f"[dim]{DISCLAIMER}[/dim]\n")


# ==================================================================
# Main Menu
# ==================================================================
def show_menu() -> str:
    table = Table(title="AI Productivity Assistant", show_header=False, border_style="cyan")
    table.add_column("Option", style="bold cyan", width=6)
    table.add_column("Tool")

    table.add_row("1", "📧  Smart Email Generator")
    table.add_row("2", "📝  Meeting Notes Summarizer")
    table.add_row("3", "📅  AI Task Planner / Scheduler")
    table.add_row("4", "🔎  AI Research Assistant")
    table.add_row("5", "💬  AI Workplace Chatbot")
    table.add_row("0", "🚪  Exit")

    console.print()
    console.print(table)
    return Prompt.ask("Select a tool", choices=["1", "2", "3", "4", "5", "0"], default="5")


def main() -> None:
    console.print(Panel.fit(
        "[bold cyan]AI Productivity Assistant[/bold cyan]\n"
        f"[dim]Powered by Gemini 3.5 Flash  ·  {datetime.now():%d %b %Y}[/dim]\n\n"
        "[italic]Automate emails, meetings, planning, research, and more.[/italic]",
        border_style="cyan",
    ))

    client = build_client()

    actions = {
        "1": tool_email_generator,
        "2": tool_meeting_summarizer,
        "3": tool_task_planner,
        "4": tool_research_assistant,
        "5": tool_chatbot,
    }

    while True:
        choice = show_menu()
        if choice == "0":
            console.print("\n[bold cyan]Goodbye! 👋[/bold cyan]\n")
            break
        action = actions.get(choice)
        if action:
            action(client)
            console.print(Rule(style="dim"))


if __name__ == "__main__":
    main()
