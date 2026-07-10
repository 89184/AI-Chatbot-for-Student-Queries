import json
import pickle
import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Create Flask app
app = Flask(__name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
CORS(app)

# Try loading tensorflow
try:
    # Import with error handling for newer versions
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    print(f" TensorFlow loaded successfully (version: {tf.__version__})")
    
    # Suppress warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
except ImportError:
    print(" TensorFlow not found. Please install: pip install tensorflow")
    sys.exit(1)

print("=" * 60)
print(" AI CHATBOT - STARTING SERVER")
print("=" * 60)

# Load model and data
try:
    lemmatizer = WordNetLemmatizer()
    
    # Check if model files exist
    model_path = os.path.join(BASE_DIR, 'model.keras')
    if not os.path.exists(model_path):
        model_path = os.path.join(BASE_DIR, 'model.h5')
    
    if not os.path.exists(model_path):
        logger.error(f" Model not found at: {model_path}")
        logger.info(" Please run: python backend/train.py")
        sys.exit(1)
    
    # Load model with custom objects to handle version differences
    try:
        model = load_model(model_path, compile=False)
    except:
        # Try loading with custom_objects
        model = load_model(model_path, custom_objects={}, compile=False)
    
    words = pickle.load(open(os.path.join(BASE_DIR, 'words.pkl'), 'rb'))
    classes = pickle.load(open(os.path.join(BASE_DIR, 'classes.pkl'), 'rb'))
    
    with open(os.path.join(PROJECT_ROOT, 'data', 'intents.json'), 'r') as f:
        intents = json.load(f)
    
    logger.info(" Model loaded successfully!")
    logger.info(f" Vocabulary: {len(words)} words")
    logger.info(f" Classes: {len(classes)} intents")
except Exception as e:
    logger.error(f" Error loading model: {e}")
    logger.info(" Please run: python backend/train.py to retrain the model")
    sys.exit(1)

# NLTK functions
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]

def get_response(intents_list, intents_json):
    if not intents_list:
        return "Sorry, I don't understand. Please rephrase your question."
    
    tag = intents_list[0]['intent']
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "Sorry, I don't understand."

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'response': 'Please enter a message.', 'confidence': '0'})
    
    try:
        ints = predict_class(message)
        response = get_response(ints, intents)
        confidence = ints[0]['probability'] if ints else '0'
        return jsonify({'response': response, 'confidence': confidence})
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'response': 'Sorry, something went wrong.', 'confidence': '0'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'model_loaded': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🚀 Server running at:")
    print(f"   http://localhost:{port}")
    print(f"   http://127.0.0.1:{port}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
