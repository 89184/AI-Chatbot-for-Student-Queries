# AI Chatbot for Student Queries

## Project Overview

An AI-powered college inquiry chatbot that provides quick and accurate responses to frequently asked questions about courses, admissions, fee structure, and facilities.

### Key Features

- **NLP-powered**: Uses TensorFlow and NLTK for intent classification
- **85%+ Accuracy**: Trained on 1,000+ Q&A pairs
- **<1 Second Response**: Fast inference for real-time chat
- **200+ Concurrent Users**: Scalable for high traffic
- **DeepSeek-style UI**: Modern dark theme with sidebar
- **Cloud Deployable**: Works on Render, Streamlit Cloud, or any cloud platform

---

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Core programming language |
| TensorFlow | 2.15.0+ | Model training and inference |
| NLTK | 3.8.1+ | Natural language processing |
| Flask | 2.3.3+ | API server |
| Gunicorn | 21.2.0+ | Production WSGI server |
| HTML/CSS/JS | - | Chat interface |
| Docker | - | Containerization |

---

##  Project Structure
'''text
AI-Chatbot-for-Student-Queries/
│
├── backend/
│ ├── app.py # Flask API server
│ ├── train.py # Model training script
│ ├── model.keras # Trained Keras model
│ ├── words.pkl # Vocabulary
│ ├── classes.pkl # Intent classes
│ ├── requirements.txt # Dependencies
│ ├── templates/
│ │ └── index.html # Chat UI
│ └── static/
│ ├── style.css # Styling
│ ├── script.js # Frontend logic
│ └── sidebar.js # Sidebar functionality
│
├── data/
│ └── intents.json # Q&A dataset
│
├── frontend/ # Original frontend files
│ ├── index.html
│ ├── style.css
│ └── script.js
│
├── tests/
│ └── test_chatbot.py # Unit tests
│
├── .env # Environment variables
├── .gitignore # Git ignore file
├── requirements.txt # Python dependencies
├── LICENSE # MIT License
└── README.md # This file '''



---

##  Installation Guide

### Prerequisites

- Python 3.11+ (Recommended)
- pip
- Git (optional)

### Step 1: Clone Repository

git clone https://github.com/yourusername/ai-chatbot.git
cd ai-chatbot


### Step 2: Create Virtual Environment

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate          # Linux/Mac
# OR
venv\Scripts\activate              # Windows

### Step 3: Install Dependencies

pip install -r backend/requirements.txt

### Step 4: Download NLTK Data

python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('omw-1.4')"

### Step 5: Train the Model

python backend/train.py

### Step 6: Run the Application

python backend/app.py

### Step 7: Access the Chatbot
Open your browser and go to: http://localhost:5000

Training Results
Metric	Value
Training Accuracy	85%+
Q&A Pairs	1,000+
Intents	10+
Vocabulary Size	82+ words
Response Time	<1 second
 Testing
bash
# Run unit tests
python -m pytest tests/

# Test specific file
python -m pytest tests/test_chatbot.py -v

# Run tests directly
python tests/test_chatbot.py
 Docker Deployment
bash
# Build Docker image
docker build -f docker/Dockerfile -t ai-chatbot .

# Run container
docker run -p 5000:5000 ai-chatbot
 Deploy to Render (Free)
Push code to GitHub

Go to render.com

Create new Web Service

Connect repository

Use these settings:

Build Command: pip install -r backend/requirements.txt

Start Command: python backend/app.py

Instance Type: Free

Click "Create"

