"""
Train the Customer Service Chatbot Model
This script loads intents, preprocesses data, and trains a classification model
"""

import json
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from nlp_utils import clean_text, download_nltk_data


def load_intents(filepath='intents.json'):
    """Load intents from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def prepare_training_data(intents_data):
    """
    Prepare training data from intents
    """
    X = []  # Patterns
    y = []  # Tags

    for intent in intents_data['intents']:
        tag = intent['tag']
        for pattern in intent['patterns']:
            cleaned_pattern = clean_text(pattern)
            X.append(cleaned_pattern)
            y.append(tag)

    tags = list(set(y))
    return X, y, tags


def train_model(X, y):
    """
    Train the chatbot model using TF-IDF and Naive Bayes
    """

    # ✅ FIX: REMOVE stratify=y (CRITICAL for small datasets)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),
        min_df=1
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    classifier = MultinomialNB(alpha=0.1)
    classifier.fit(X_train_tfidf, y_train)

    y_pred = classifier.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)

    print("\nModel Training Complete!")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return vectorizer, classifier, accuracy


def save_model(vectorizer, classifier, tags, model_dir='model'):
    """Save trained model and vectorizer"""
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    with open(os.path.join(model_dir, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)

    with open(os.path.join(model_dir, 'classifier.pkl'), 'wb') as f:
        pickle.dump(classifier, f)

    with open(os.path.join(model_dir, 'tags.pkl'), 'wb') as f:
        pickle.dump(tags, f)

    print(f"\nModel saved to '{model_dir}/' directory")


def main():
    """Main training pipeline"""
    print("=" * 60)
    print("Customer Service Chatbot - Model Training")
    print("=" * 60)

    print("\n1. Downloading NLTK data...")
    download_nltk_data()
    print("   [OK] NLTK data ready")

    print("\n2. Loading intents...")
    intents_data = load_intents()
    print(f"   [OK] Loaded {len(intents_data['intents'])} intent categories")

    print("\n3. Preparing training data...")
    X, y, tags = prepare_training_data(intents_data)
    print(f"   [OK] Prepared {len(X)} training samples")
    print(f"   [OK] Intent categories: {', '.join(tags)}")

    print("\n4. Training model...")
    vectorizer, classifier, accuracy = train_model(X, y)
    print(f"   [OK] Model trained with {accuracy * 100:.2f}% accuracy")

    print("\n5. Saving model...")
    save_model(vectorizer, classifier, tags)
    print("   [OK] Model saved successfully")

    print("\n" + "=" * 60)
    print("Training Complete! You can now run app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
