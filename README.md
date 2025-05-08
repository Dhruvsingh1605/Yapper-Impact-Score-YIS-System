Yapper Impact Score (YIS)
The Yapper Impact Score (YIS) system is a prototype designed to evaluate social media influencers' impact on specific campaigns. It simulates tweets for mock users, measures each tweet's engagement and semantic relevance to a campaign brief, and combines these metrics into a single score per user. The project integrates MLOps tools like DVC and MLflow for data and experiment reproducibility and exposes the scoring logic via a FastAPI REST endpoint for integration or dashboarding.

📁 Project Structure
arduino
Copy
Edit

├── data/
│   ├── raw/
│   │   ├── generate_mock_tweets.py
│   │   ├── mock_tweets.json
│   │   └── campaign_brief.txt
│   └── processed/
│       └── yis_report.csv
├── app/
│   ├── models/
│   │   └── config.py
│   ├── services/
│   │   ├── embedder.py
│   │   └── scorer.py
│   ├── pipeline/
│   │   └── embed_and_score.py
│   ├── routers/
│   │   └── score.py
│   └── main.py
├── dvc.yaml
├── requirements.txt
└── README.md
⚙️ Features
Data Simulation: Generates synthetic tweet data using Faker, random timestamps, and engagement metrics.

Embedding: Utilizes Sentence-Transformers to encode tweet texts and campaign briefs into embedding vectors.

Relevance Computation: Calculates cosine similarity between tweet vectors and the campaign brief vector to determine relevance scores.

Engagement Scoring: Computes engagement scores based on retweets, replies, and likes using configurable weights.

Final Scoring: Combines engagement and relevance scores to produce a final YIS per user.

MLOps Integration: Employs DVC for data versioning and MLflow for experiment tracking.

API Endpoint: Exposes scoring logic via a FastAPI REST endpoint.

🛠️ Installation
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/yourusername/yapper-impact-score.git
cd yapper-impact-score
Create a Virtual Environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Install DVC:

bash
Copy
Edit
pip install dvc
🚀 Usage
1. Data Simulation
Generate synthetic tweet data:
EHeidi.dev
+2
YouTube
+2
DEV Community
+2

bash
Copy
Edit
dvc repro simulate
2. Run the Pipeline
Execute the embedding and scoring pipeline:

bash
Copy
Edit
dvc repro embed_and_score
3. Start the API Server
Launch the FastAPI server:

bash
Copy
Edit
uvicorn app.main:app --reload
Access the API documentation at: http://localhost:8000/docs

📈 MLflow Tracking
To monitor experiments and metrics:

bash
Copy
Edit
mlflow ui
Then, navigate to http://localhost:5000 in your browser.

🧪 API Endpoint
POST /score/

Request Body:

json
Copy
Edit
[
  {
    "text": "Sample tweet text",
    "retweet_count": 10,
    "reply_count": 5,
    "favorite_count": 20
  },
  ...
]
Response:

json
Copy
Edit
{
  "yis": 85.5,
  "details": {
    "tweet_count": 10,
    "total_engagement": 150,
    "average_relevance": 0.85
  }
}
📂 Configuration
The app/models/config.py file manages configuration settings:

Embedding Model Name: Specifies the Sentence-Transformers model to use.

Engagement Weights: Defines weights for retweets, replies, and likes.

🔧 Modules Overview
generate_mock_tweets.py: Generates synthetic tweets with random engagement metrics.

embedder.py:

embed_texts: Embeds a list of texts into vectors.

compute_relevance: Calculates cosine similarity between tweet vectors and the campaign brief vector.

scorer.py:

engagement_score: Calculates engagement score based on retweets, replies, and likes.

final_tweet_score: Combines engagement and relevance scores.

aggregate_user_scores: Aggregates tweet scores to compute the final YIS.

embed_and_score.py: Orchestrates the data loading, embedding, scoring, and result generation processes.

score.py: Defines the FastAPI endpoint for computing YIS.

main.py: Initializes and runs the FastAPI application.

📌 Future Enhancements
Live Twitter Integration: Fetch real tweets using Twitter API.

Multi-User Support: Group tweets per user handle and compute individual YIS.

Advanced Scoring: Incorporate GPT-based scoring mechanisms.

Dashboard Visualization: Develop a Streamlit or Flask dashboard to visualize YIS trends.

📄 License
This project is licensed under the MIT License.