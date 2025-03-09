# Import necessary libraries
import numpy as np
import pickle
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import os

# Initialize Flask app
app = Flask(__name__)

# Load trained model (Assuming we have a saved model)
model_path = "model.pkl"
if os.path.exists(model_path):
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)
else:
    # Train a basic sentiment model if not found
    sample_data = ["I love this!", "This is bad", "Amazing product", "Worst experience"]
    sample_labels = [1, 0, 1, 0]
    
    model = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('classifier', MultinomialNB())
    ])
    
    model.fit(sample_data, sample_labels)
    with open(model_path, "wb") as model_file:
        pickle.dump(model, model_file)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        text = data.get("text", "")
        prediction = model.predict([text])[0]
        return jsonify({"sentiment": "positive" if prediction == 1 else "negative"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def home():
    return "Sentiment Analysis API is running!"

if __name__ == '__main__':
    app.run(debug=True)
