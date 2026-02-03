"""
Customer Service Chatbot - Main Application
Interactive chatbot for handling customer service queries
"""

import json
import pickle
import os
import random
from nlp_utils import clean_text, download_nltk_data

class CustomerServiceChatbot:
    """Main chatbot class"""
    
    def __init__(self, model_dir='model', intents_file='intents.json'):
        """Initialize the chatbot"""
        self.model_dir = model_dir
        self.intents_file = intents_file
        self.vectorizer = None
        self.classifier = None
        self.tags = None
        self.intents_data = None
        self.confidence_threshold = 0.5
        
        # Load model and intents
        self.load_model()
        self.load_intents()
    
    def load_model(self):
        """Load trained model and vectorizer"""
        try:
            # Load vectorizer
            with open(os.path.join(self.model_dir, 'vectorizer.pkl'), 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            # Load classifier
            with open(os.path.join(self.model_dir, 'classifier.pkl'), 'rb') as f:
                self.classifier = pickle.load(f)
            
            # Load tags
            with open(os.path.join(self.model_dir, 'tags.pkl'), 'rb') as f:
                self.tags = pickle.load(f)
            
            print("[OK] Model loaded successfully!")
        except FileNotFoundError:
            print("Error: Model files not found. Please run train_model.py first.")
            exit(1)
    
    def load_intents(self):
        """Load intents data"""
        try:
            with open(self.intents_file, 'r', encoding='utf-8') as f:
                self.intents_data = json.load(f)
            print("[OK] Intents loaded successfully!")
        except FileNotFoundError:
            print(f"Error: {self.intents_file} not found.")
            exit(1)
    
    def predict_intent(self, user_input):
        """
        Predict the intent of user input
        
        Returns:
            intent (str): Predicted intent tag
            confidence (float): Confidence score
        """
        # Clean the input
        cleaned_input = clean_text(user_input)
        
        # Vectorize
        input_vector = self.vectorizer.transform([cleaned_input])
        
        # Predict
        intent = self.classifier.predict(input_vector)[0]
        
        # Get probability/confidence
        probabilities = self.classifier.predict_proba(input_vector)[0]
        confidence = max(probabilities)
        
        return intent, confidence
    
    def get_response(self, intent):
        """Get a random response for the predicted intent"""
        for intent_data in self.intents_data['intents']:
            if intent_data['tag'] == intent:
                return random.choice(intent_data['responses'])
        
        return "I'm not sure I understand. Could you rephrase that?"
    
    def get_fallback_response(self):
        """Return a fallback response when confidence is low"""
        fallback_responses = [
            "I'm not quite sure I understand. Could you please rephrase your question?",
            "I didn't quite catch that. Can you try asking in a different way?",
            "I'm still learning! Could you provide more details or ask differently?",
            "I'm not certain about that. Would you like to speak with a human representative?",
            "I want to make sure I help you correctly. Could you clarify your question?"
        ]
        return random.choice(fallback_responses)
    
    def chat(self, user_input):
        """
        Process user input and return response
        
        Args:
            user_input (str): User's message
        
        Returns:
            response (str): Bot's response
        """
        # Predict intent
        intent, confidence = self.predict_intent(user_input)
        
        # Check confidence threshold
        if confidence < self.confidence_threshold:
            return self.get_fallback_response()
        
        # Get response
        response = self.get_response(intent)
        
        return response
    
    def run(self):
        """Run the chatbot in interactive mode"""
        print("\n" + "=" * 60)
        print("Customer Service Chatbot")
        print("=" * 60)
        print("\nHello! I'm your customer service assistant.")
        print("I can help you with:")
        print("  • Product information")
        print("  • Pricing and payments")
        print("  • Shipping and delivery")
        print("  • Returns and refunds")
        print("  • Account issues")
        print("  • And more!")
        print("\nType 'quit', 'exit', or 'bye' to end the conversation.")
        print("=" * 60 + "\n")
        
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\nBot: Goodbye! Have a great day! Feel free to come back if you need help.\n")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Get response
            response = self.chat(user_input)
            
            # Print response
            print(f"Bot: {response}\n")

def main():
    """Main function to run the chatbot"""
    # Download NLTK data if needed
    download_nltk_data()
    
    # Initialize and run chatbot
    bot = CustomerServiceChatbot()
    bot.run()

if __name__ == "__main__":
    main()
