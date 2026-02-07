import streamlit as st
import requests
import json
import datetime
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Study Planner",
    layout="centered"
)

st.title("📚 AI Study Planner")

# ---------------- CONSTANTS ----------------
HISTORY_FILE = "study_plan_history.json"
PDF_FILE = "ai_study_plan.pdf"

# ---------------- FUNCTIONS ----------------
def save_plan(plan, subjects, days_left, weak_topics):
    entry = {
        "timestamp": str(datetime.datetime.now()),
        "subjects": subjects,
        "days_left": days_left,
        "weak_topics": weak_topics,
        "plan": plan
    }

    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    history.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def generate_pdf(plan):
    doc = SimpleDocTemplate(PDF_FILE)
    styles = getSampleStyleSheet()
    story = []

    for line in plan.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def delete_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

# ---------------- USER INPUT ----------------
subjects = st.text_input("Enter subjects (comma separated)")
days_left = st.number_input("Days left for exam", min_value=1, step=1)
weak_topics = st.text_input("Weak topics (comma separated)")

# ---------------- GENERATE PLAN ----------------
if st.button("Generate Study Plan"):

    if subjects and weak_topics:
        prompt = f"""
You are an AI study planner.

Create a concise daily study plan based on:
Subjects: {subjects}
Days left: {days_left}
Weak topics: {weak_topics}

Rules:
- Max 5 hours per day
- Prioritize weak topics
- Include revision
- Day-wise plan
"""

        payload = {
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=300
            )

            if response.status_code == 200:
                data = response.json()

                if "response" in data:
                    st.session_state["plan"] = data["response"]
                    save_plan(
                        st.session_state["plan"],
                        subjects,
                        days_left,
                        weak_topics
                    )
                else:
                    st.error("No response generated")
            else:
                st.error("Ollama server error")

        except requests.exceptions.RequestException:
            st.error("Cannot connect to Ollama server")
    else:
        st.warning("Please fill all fields")

# ---------------- DISPLAY PLAN + DOWNLOADS ----------------
if "plan" in st.session_state:
    plan = st.session_state["plan"]

    st.subheader("📅 AI Generated Study Plan")
    st.text(plan)

    st.download_button(
        "⬇️ Download as TXT",
        plan,
        "ai_study_plan.txt",
        "text/plain"
    )

    generate_pdf(plan)
    with open(PDF_FILE, "rb") as f:
        st.download_button(
            "📄 Download as PDF",
            f,
            "ai_study_plan.pdf",
            "application/pdf"
        )

# ---------------- HISTORY ----------------
st.divider()
st.subheader("📜 Study Plan History")

history = load_history()

if history:
    for i, entry in enumerate(reversed(history), 1):
        with st.expander(f"Plan {i} | {entry['timestamp']}"):
            st.write("**Subjects:**", entry["subjects"])
            st.write("**Days Left:**", entry["days_left"])
            st.write("**Weak Topics:**", entry["weak_topics"])
            st.text(entry["plan"])

    if st.button("🗑️ Delete All History"):
        delete_history()
        st.success("History deleted successfully")
        st.experimental_rerun()
else:
    st.info("No study plan history found")
