"""
NLP Utilities for Customer Service Chatbot
Contains text preprocessing and NLP helper functions
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import re

# Download required NLTK data
def download_nltk_data():
    """Download necessary NLTK datasets"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)
    
    try:
        nltk.data.find('corpora/omw-1.4')
    except LookupError:
        nltk.download('omw-1.4', quiet=True)

# Download NLTK data on import
download_nltk_data()

# Initialize lemmatizer and stopwords after download
from nltk.corpus import stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    """
    Preprocess text for NLP processing
    
    Args:
        text (str): Input text to preprocess
    
    Returns:
        str: Preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def tokenize_and_lemmatize(text):
    """
    Tokenize and lemmatize text
    
    Args:
        text (str): Input text
    
    Returns:
        list: List of lemmatized tokens
    """
    # Tokenize
    tokens = word_tokenize(text)
    
    # Lemmatize and remove stopwords
    lemmatized_tokens = [
        lemmatizer.lemmatize(token) 
        for token in tokens 
        if token not in stop_words and len(token) > 1
    ]
    
    return lemmatized_tokens

def clean_text(text):
    """
    Complete text cleaning pipeline
    
    Args:
        text (str): Input text
    
    Returns:
        str: Cleaned text ready for vectorization
    """
    # Preprocess
    text = preprocess_text(text)
    
    # Tokenize and lemmatize
    tokens = tokenize_and_lemmatize(text)
    
    # Join tokens back into string
    return ' '.join(tokens)

if __name__ == "__main__":
    # Download NLTK data when module is run directly
    print("Downloading NLTK data...")
    download_nltk_data()
    print("NLTK data downloaded successfully!")
    
    # Test the functions
    test_text = "Hello! I need help with returning my product. Can you assist me?"
    print(f"\nOriginal: {test_text}")
    print(f"Cleaned: {clean_text(test_text)}")
