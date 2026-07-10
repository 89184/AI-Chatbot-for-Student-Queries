import json
import pickle
import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import os
import sys

print("=" * 60)
print(" AI CHATBOT - MODEL TRAINING")
print("=" * 60)

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)
try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4', quiet=True)

# TensorFlow
try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout
    from tensorflow.keras.optimizers import SGD
    print(" Using TensorFlow")
except ImportError:
    print(" TensorFlow not found")
    sys.exit(1)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents
print("\n Loading intents...")
with open('data/intents.json', 'r') as f:
    intents = json.load(f)

# Prepare training data
words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and sort
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

print(f" Found {len(words)} unique words")
print(f" Found {len(classes)} intent classes")

# Create directories
os.makedirs('backend', exist_ok=True)

# Save words and classes
pickle.dump(words, open('backend/words.pkl', 'wb'))
pickle.dump(classes, open('backend/classes.pkl', 'wb'))
print(" Saved vocabulary and classes")

# Create training data
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(w.lower()) for w in word_patterns]
    
    for w in words:
        bag.append(1) if w in word_patterns else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

print(f" Training data: {len(train_x)} samples")

# Build model
print("\n Building neural network model...")
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train model
print("\n Training model...")
history = model.fit(
    np.array(train_x), 
    np.array(train_y), 
    epochs=200, 
    batch_size=5, 
    verbose=1
)

# Save model in .keras format (compatible across versions)
model.save('backend/model.keras')
print("\n Model trained and saved successfully!")
print(f" Training Accuracy: {history.history['accuracy'][-1]*100:.2f}%")

print("\n" + "=" * 60)
print(" TRAINING COMPLETE!")
print("=" * 60)