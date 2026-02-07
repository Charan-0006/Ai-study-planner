# 📚 AI Study Planner

AI Study Planner is a Streamlit-based web application that generates personalized, day-wise study plans using an AI model. Users can create structured study schedules based on subjects, available preparation time, and weak topics, with options to download and manage plans.

---

## 🚀 Features

- AI-generated daily study plans
- Prioritizes weak topics
- Day-wise structured output
- Download study plans as:
  - PDF
  - TXT
- Save generated plans locally
- View previously generated plans
- Delete saved plan history
- Simple and clean UI

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Requests
- Ollama (Local LLM)
- ReportLab
- JSON (local storage)

---

## 📂 Project Structure

ai-study-planner/
│
├── app.py
├── README.md
├── requirements.txt
├── study_plan_history.json


pip install -r requirements.txt
Run the Application
ollama serve
streamlit run app.py
Open in browser:

http://localhost:8501
📄 requirements.txt
streamlit
requests
reportlab
⚠️ Notes
Uses a locally running Ollama server at http://localhost:11434

Not configured for cloud deployment without backend changes

Study plans are stored locally in JSON format

PDF files are generated dynamically for download

🔮 Future Enhancements
Cloud-based AI integration

User authentication

Database-backed storage

Progress tracking

UI improvements