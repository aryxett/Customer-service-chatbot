"""
Demo script to test the Customer Service Chatbot
This script runs automated tests with various customer queries
"""

from chatbot import CustomerServiceChatbot
import sys

def test_chatbot():
    """Run automated tests on the chatbot"""
    print("=" * 60)
    print("Customer Service Chatbot - Automated Testing")
    print("=" * 60)
    
    # Initialize chatbot
    print("\nInitializing chatbot...")
    bot = CustomerServiceChatbot()
    
    # Test queries
    test_queries = [
        ("Hello!", "greeting"),
        ("Hi there", "greeting"),
        ("What products do you sell?", "product_info"),
        ("How much does it cost?", "pricing"),
        ("What are your shipping options?", "shipping"),
        ("How do I return a product?", "returns"),
        ("I want to file a complaint", "complaints"),
        ("I need help", "help"),
        ("What payment methods do you accept?", "payment"),
        ("I forgot my password", "account"),
        ("What are your business hours?", "hours"),
        ("Thank you!", "thanks"),
        ("Goodbye", "goodbye"),
    ]
    
    print("\n" + "=" * 60)
    print("Running Tests")
    print("=" * 60 + "\n")
    
    correct = 0
    total = len(test_queries)
    
    for query, expected_intent in test_queries:
        # Get prediction
        predicted_intent, confidence = bot.predict_intent(query)
        response = bot.chat(query)
        
        # Check if correct
        is_correct = predicted_intent == expected_intent
        if is_correct:
            correct += 1
        
        # Print result
        status = "[OK]" if is_correct else "[FAIL]"
        print(f"{status} Query: \"{query}\"")
        print(f"     Expected: {expected_intent} | Predicted: {predicted_intent} | Confidence: {confidence:.2f}")
        print(f"     Response: {response}")
        print()
    
    # Print summary
    accuracy = (correct / total) * 100
    print("=" * 60)
    print(f"Test Results: {correct}/{total} correct ({accuracy:.1f}% accuracy)")
    print("=" * 60)

if __name__ == "__main__":
    test_chatbot()
