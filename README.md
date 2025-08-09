⚡ Real-Time Fraud Detection System
📌 Overview
The Real-Time Fraud Detection System continuously simulates transactions, detects suspicious activity using both rule-based logic and optional machine learning, and visualizes insights through an interactive Streamlit dashboard.
It is ideal for demonstrating fraud analytics pipelines and anomaly detection workflows.

✨ Features
Live Transaction Simulation – Synthetic banking/payment transactions (Faker + Geocoding).

Rule-Based Detection – High amount, frequency, IP/location mismatch, blacklist checks.

Optional ML Integration – Anomaly detection via Isolation Forest.

Optional AI Explanations – Fraud reason explanations using OpenAI GPT.

Real-Time Web Dashboard (Streamlit):

📜 Recent transactions

🚨 Flagged alerts with reasons & explanations

📊 Analytics: bar, pie, and time-series charts

🌍 Geo Map of transactions (Lat/Lon from geocoding)

SQLite Storage – Stores transactions and alerts locally.

🏗 Tech Stack
Backend & Pipeline: Python 3.10+, SQLAlchemy, SQLite

Frontend: Streamlit, Altair, PyDeck

ML Model: Scikit-learn (Isolation Forest)

Data Simulation: Faker, Geopy (Nominatim API for lat/lon)

Optional AI: OpenAI GPT-4

📂 Project Structure
text
fraud_detection_system/
│
├── api/
│   └── data_pipeline.py           # Main real-time ingestion and detection loop
│
├── dashboard/
│   └── app.py                     # Interactive Streamlit dashboard
│
├── models/
│   ├── db_models.py               # ORM models for DB tables
│   └── isolation_forest_model.py  # ML model training & prediction
│
├── utils/
│   ├── data_generator.py          # Transaction simulation + geocoding
│   ├── fraud_rules.py             # Rule-based fraud detection logic
│   └── genai_explain.py           # (Optional) AI-based alert explanations
│
├── data/
│   └── fraud_detector.db          # SQLite database file
│
├── requirements.txt
└── README.md


⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/fraud_detection_system.git
cd fraud_detection_system

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ (Optional) Configure OpenAI API
If you want AI explanations for alerts:

In utils/genai_explain.py, set:

python
openai.api_key = "YOUR_OPENAI_API_KEY"

▶️ Running Locally
Step 1: Initialize Database
python -m models.db_models
Creates fraud_detector.db with tables for transactions and alerts.

Step 2: Start the Data Pipeline
Run in Terminal 1:

python -m api.data_pipeline
Continuously simulates transactions, detects risk, stores data.

Step 3: Launch the Dashboard
Run in Terminal 2:

streamlit run dashboard/app.py
Local: http://localhost:8501

Network: http://<your-local-ip>:8501

📊 Dashboard Overview
Tabs in the UI:

Recent Transactions – Refreshes automatically.

Flagged Alerts – Expandable sections showing risk score, reasons, and explanations.

Analytics – Visual insights:

Transactions per country (bar chart)

Alert reasons (pie chart)

Alerts over time (line chart)

Geo Map – Locations of last 200 transactions (requires lat/lon from geocoding).

🧮 Risk Scoring Logic
Rule	Score	Description
Amount > 3000	+30	High amount
≥5 txns by same user (recent)	+40	High frequency
IP/location mismatch	+20	Geographic mismatch
Blacklisted user/IP	+50	Known bad actor
Final risk_score = sum of triggered rule scores.

ML anomaly detection can be added to adjust/influence the score.

🤖 Machine Learning Mode (Optional)
Uses Isolation Forest for unsupervised anomaly detection.

Feature vector example: [amount, transaction velocity, hour_of_day].

Helps detect subtle anomalies rules may miss.

Train example (run in models/isolation_forest_model.py):

python -m models.isolation_forest_model
🌍 Geocoding Notes
geopy.Nominatim adds lat/lon for map plotting.

Subject to free API rate limits (~1 request/sec).

For failsafe, you can add a local lookup table for common countries.

🔄 Reset Database
If you change the schema:

rm data/fraud_detector.db          # or del data\fraud_detector.db (on Windows)
python -m models.db_models

🛠 Possible Enhancements
Switch SQLite → PostgreSQL for scalability.

Add authentication to dashboard.

Containerize (Docker) and orchestrate with Kubernetes.

Integrate live payments API for real data streams.
