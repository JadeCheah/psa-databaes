# 🩺 PathAI — Personalized Skills Analysis Platform

## 🌟 Project Overview

**PathAI** is a prototype web app designed to help employees visualize their professional strengths, detect skill gaps, and receive tailored recommendations for upskilling, leadership growth, and team collaboration.

The goal is to move beyond static performance reports — enabling **data-driven, personalized career development**.

---

## 🎯 Intention

Many organizations struggle to offer personalized growth advice due to fragmented data and one-size-fits-all frameworks.
PathAI addresses this by:

* Combining structured employee skill data with a recommendation engine.
* Giving employees actionable, individualized insights.
* Promoting mentorship and leadership growth through intelligent team matching.

---

## 👥 Target Users

* **Employees** seeking to grow in their careers.
* **HR / L&D teams** tracking workforce development trends.
* **Leaders or mentors** identifying suitable mentees or collaborators.

---

## ⚙️ Core Features

### 🧠 Leadership & Skill Analysis

Each employee profile is analyzed to extract:

* Leadership readiness score
* Strengths and gaps in key skill clusters

### 📚 Training Recommendations

Suggests courses or learning areas to close skill gaps.
Recommendations are based on missing competencies compared to successful peer profiles.

### 🤝 Collaboration Matching

Identifies potential mentors or teammates with complementary skills, enabling:

* Cross-functional collaboration
* Peer-to-peer learning

### 💬 Interactive Chat (Current Version)

The Chat tab provides a **deterministic Q&A interface**, summarizing insights from the recommender system.
No external APIs are used — all recommendations come from local computations.

---

## 🧩 Tech Stack

| Layer              | Technology                       |
| ------------------ | -------------------------------- |
| Frontend           | Streamlit                        |
| Backend            | Python (modular services)        |
| Recommender Engine | Custom similarity-based logic    |
| Data               | CSV/embedding cache using Pandas |

---

## 🗂️ Code Structure

```
app/
├── streamlit_app.py          # Main entry point
├── views/
│   └── chat.py               # Chat tab UI (deterministic fallback)
├── recommenders/             # Core recommendation modules
│   ├── recommendation_engine.py
│   └── test_recommenders.py
├── services/
│   └── llm_client.py         # (Removed) placeholder for LLM integration
└── data/                     # Employee profiles and embedding cache
```

---

## 🧮 Recommenders & Analytics Module

The `/recommenders` module forms the analytical core of the platform. It powers all insights displayed on the webpage — including skill gaps, team matches, and leadership scoring.

### 🧩 `recommend_training(employee_profile)`

This function identifies an employee’s **missing or weak skills** by comparing their skill vector to an ideal benchmark or reference profile.
It then generates **personalized training recommendations** to help close these gaps.

**Logic Summary:**

* Uses similarity scoring between the employee’s known skills and target competencies.
* Prioritizes skill areas where the user’s proficiency is lowest.
* Returns a structured list of “recommended upskilling areas.”

**Example Output:**

```json
{
  "Employee": "Alicia",
  "Missing Skills": ["Data Visualization", "Cloud Security"],
  "Suggested Courses": ["Advanced Tableau", "AWS Foundations"]
}
```

---

### 🤝 `recommend_team_collabs(employee_profile, all_profiles)`

Finds suitable **collaboration or mentorship matches** based on complementarity of skills.

**Logic Summary:**

* Calculates cosine similarity between employee embeddings.
* Matches users whose strengths align with another’s weaknesses.
* Returns a ranked list of ideal mentors, mentees, or team collaborators.

**Feature Integration:**
This logic powers the **“Recommended Collaborators”** section on the site, helping users discover colleagues to learn from or support.

---

### 🧠 `recommend_leadership(employee_profile)`

Assesses **leadership potential** using weighted competency data such as:

* Communication
* Initiative
* Adaptability
* Decision-making

**Logic Summary:**

* Aggregates key behavioral and performance metrics.
* Normalizes to a 0–1 scale to produce a **Leadership Score**.
* Categorizes employees as “High,” “Moderate,” or “Developing” potential.

**Example Output:**

```json
{
  "Employee": "Ravi",
  "Leadership Score": 0.82,
  "Potential Level": "High"
}
```

---

### 🧪 `test_recommenders.py`

A small validation script that:

* Loads mock employee data.
* Runs all three recommendation functions.
* Prints structured sample outputs to confirm the logic works correctly.

Used for quick sanity checks before full app deployment.

---

## 💻 Web Application Features

The web interface, built using **Streamlit**, is designed for ease of exploration and interactivity.

### **Dashboard View**

Displays personalized analytics:

* Leadership readiness
* Skill strengths and gaps
* Suggested training programs

### **Team Collaboration View**

Allows users to visualize and filter potential mentors or teammates, based on recommender results.

### **Chat Tab**

Provides a simple Q&A-like interface that summarizes results from the recommender engine.
While currently deterministic (non-AI), the design allows easy integration of future LLM-based interaction.

### **Data Insights**

Shows aggregate organizational trends — e.g., common skill gaps or top leadership competencies across all profiles.

---

## 🚀 Setup & Run Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/psa-database.git
cd psa-database
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App

```bash
streamlit run app/streamlit_app.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).

---

## 🚧 Future Improvements

### ✨ LLM Integration

Originally, the project included a prototype `llm_client.py` using **Azure OpenAI** to generate richer, conversational responses.
This was disabled due to credential and quota restrictions.

With more time and resources, future versions could:

* Integrate an **LLM-powered assistant** (e.g., GPT-4o-mini).
* Generate **personalized summaries and natural responses** to user questions.
* Combine multiple recommender outputs into an AI-driven conversational layer.

---

## ✅ Current Outcome

PathAI successfully demonstrates how structured employee data can drive:

* **Leadership insight generation**
* **Targeted upskilling recommendations**
* **Mentorship and collaboration suggestions**

This provides a scalable foundation for an AI-enhanced professional development system.

