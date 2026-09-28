# 🏋️ FitBuddy – AI Fitness Plan Generator

FitBuddy is an AI-powered web application that generates personalized 7-day fitness plans based on a user's age, weight, fitness goal, and workout intensity.

It uses **Google Gemini AI** to generate workout plans and nutrition/recovery guidance. Users can also provide feedback to update their workout plans.

## ✨ Features

- 🤖 AI-generated personalized workout plans
- 📅 7-day fitness plans
- 🥗 Nutrition & recovery guidance
- 🔄 Feedback-based plan updates
- 👤 User profile management
- 📊 Admin dashboard
- 🗄️ SQLite database
- 🌐 FastAPI web application

## 🛠️ Technologies Used

- **Python**
- **FastAPI**
- **Google Gemini AI**
- **Google GenAI SDK**
- **HTML, CSS & JavaScript**
- **Jinja2**
- **SQLite & SQLAlchemy**
- **Uvicorn**

## 📁 Project Structure

```text
FitBuddy-AI/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── gemini_client.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   ├── updated_plan.py
│   ├── routes.py
│   └── main.py
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── all_users.html
│   └── error.html
├── static/
│   ├── style.css
│   └── script.js
├── tests/
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md  '''text

##🚀 How to Run
-1. Clone the repository
git clone https://github.com/YOUR-USERNAME/FitBuddy-AI.git
cd FitBuddy-AI
-2. Create virtual environment
python -m venv venv
venv\Scripts\activate
-3. Install dependencies
python -m pip install -r requirements.txt
-4. Configure Gemini API

##Create a .env file and add your Gemini API key:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_WORKOUT_MODEL=gemini-3.5-flash-lite
GEMINI_NUTRITION_MODEL=gemini-3.5-flash-lite
DATABASE_URL=sqlite:///./fitbuddy.db
ALLOW_DEMO_FALLBACK=true

-Do not upload your .env file or API key to GitHub.

##5. Run the application
python -m uvicorn app.main:app --reload

-Open:

http://127.0.0.1:8000
##🤖 AI Workflow
-User Details
     ↓
-FastAPI Backend
     ↓
-Gemini AI
     ↓
-Personalized 7-Day Plan
     ↓
-Nutrition & Recovery Guidance
     ↓
-SQLite Database
     ↓
-Result Page

-Users can also submit feedback to generate an updated workout plan.

##🎯 Project Objective

-The main objective of FitBuddy is to demonstrate how Generative AI, Python, FastAPI, databases and web technologies can be combined to create a practical AI-powered fitness application.

##🔮 Future Scope
-Secure user authentication
-Cloud deployment
-Fitness progress tracking
-Wearable device integration
-Multilingual support
-PDF export of fitness plans
-Advanced workout history and analytics
##👩‍💻 Project Type

_Generative AI Academic Project

-**Project**: FitBuddy – AI Fitness Plan Generator
-**AI**: Google Gemini
-**Backend**: FastAPI + Python
-**Database**: SQLite
