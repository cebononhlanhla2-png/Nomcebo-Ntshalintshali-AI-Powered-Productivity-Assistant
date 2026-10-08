# Nomcebo-Ntshalintshali-AI-Powered-Productivity-Assistant
AI-Powered Productivity Assistant
# WorkPulse AI — Workplace Productivity Assistant

WorkPulse AI is an enterprise-grade AI productivity suite built to automate high-volume workplace administrative tasks, including contextual communication, meeting summarization, and task scheduling.

---

## 🚀 Live Links & Project Assets
- **Live Deployed Portfolio Application**: [https://workpulse-ai.vercel.app](https://workpulse-ai.vercel.app)
- **GitHub Repository**: [https://github.com/your-username/workpulse-ai](https://github.com/your-username/workpulse-ai)
- **PowerPoint Presentation Deck**: Included in `/docs/WorkPulse_AI_Presentation.pptx`

---

## 💡 Key Features & AI Capabilities

### 1. Smart Email Generator
- **Context-Based Drafting**: Generates focused drafts based on short situational prompts.
- **Tone Customization**: Real-time adjustment across *Formal*, *Informal*, and *Persuasive* options.
- **Audience Targeting**: Contextually adjusts vocabulary and level of detail for *Clients*, *Managers*, or *Internal Teams*.

### 2. Meeting Notes Summarizer
- **Executive Summaries**: Distills dense transcripts into concise 3-sentence briefings.
- **Key Decision Extraction**: Pulls definitive alignment points out of general discussion.
- **Action Item Parsing**: Formats responsibilities, assignees, and deadlines into structured objects.

### 3. AI Task Planner & Scheduler
- **Eisenhower Matrix Classification**: Automatically bins tasks into *Urgent/Important* quadrants.
- **Time-Blocking Optimization**: Allocates items into structured hourly workday slots.
- **Productivity Recommendations**: Generates tailored efficiency and focus advice.

---

## 🛡️ Responsible AI & Governance Framework

WorkPulse AI enforces ethical and safe AI practices through system design:

1. **Human-in-the-Loop (HITL) Workflow**: All outputs (emails, summaries, schedules) are presented as editable drafts requiring final human approval before dispatch.
2. **Stateless Processing & Data Privacy**: User data and transcripts are processed transiently via standard API requests and are never persisted to external databases.
3. **Structured Schema Constraints**: Outputs for summaries and planning are validated against explicit JSON schemas to minimize hallucinated fields.
4. **Safety Filter Enforcements**: Default API safety settings are enabled to block harmful, biased, or toxic content generation.

---

## 🏗️ Technical Architecture & Stack

- **Frontend**: React (Vite), Tailwind CSS, Lucide Icons
- **AI Core**: Google Gemini API (`gemini-1.5-flash`)
- **Deployment Platform**: Vercel Serverless Hosting

---

## ⚙️ Local Setup & Installation

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/your-username/workpulse-ai.git](https://github.com/your-username/workpulse-ai.git)
   cd workpulse-ai
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Configure Environment Variables**:
   Create a `.env.local` file in the root directory:
   ```env
   VITE_GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Launch Local Server**:
   ```bash
   npm run dev
   ```
