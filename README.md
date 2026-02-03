# Customer Service Chatbot - Enhanced Edition

A comprehensive NLP-based customer service chatbot with advanced dynamic features including conversation context, database integration, web interface, API connections, learning capability, and personalization.

## 🌟 Features

### Core NLP Features
- **Intent Classification**: TF-IDF + Naive Bayes for understanding user queries
- **Natural Language Processing**: Tokenization, lemmatization, stopword removal
- **12 Intent Categories**: Greetings, products, pricing, shipping, returns, complaints, and more
- **Confidence-Based Responses**: Smart fallback for uncertain predictions

### 🚀 Dynamic Features
- **Conversation Context**: Multi-turn dialogue with memory and entity extraction
- **Database Integration**: SQLite for storing conversations, users, feedback, products, orders
- **Web Interface**: Modern Flask-based chat UI with real-time messaging
- **API Integration**: Mock APIs for products, orders, inventory, and shipping
- **Learning Engine**: Collects feedback and generates training data from conversations
- **Analytics Dashboard**: Track performance, satisfaction, and intent distribution
- **Personalization**: User profiles and context-aware responses

## 📁 Project Structure

```
Customer service chatbot/
├── app.py                  # Flask web application
├── chatbot.py              # Original CLI chatbot
├── chatbot_enhanced.py     # Enhanced chatbot with context
├── chatbot_cli.py          # Enhanced CLI with colors
├── train_model.py          # Model training script
├── nlp_utils.py            # NLP preprocessing
├── database.py             # Database operations
├── init_db.py              # Database initialization
├── context_manager.py      # Conversation context tracking
├── api_handler.py          # Mock API integrations
├── learning_engine.py      # Learning and improvement
├── analytics.py            # Performance analytics
├── intents.json            # Training data
├── requirements.txt        # Dependencies
├── model/                  # Trained models
│   ├── vectorizer.pkl
│   ├── classifier.pkl
│   └── tags.pkl
├── templates/              # Web interface HTML
│   └── index.html
├── static/                 # CSS and JavaScript
│   ├── css/style.css
│   └── js/chat.js
└── chatbot.db             # SQLite database
```

## 🛠️ Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize database**:
   ```bash
   python init_db.py
   ```

3. **Train the model** (if not already trained):
   ```bash
   python train_model.py
   ```

## 🎯 Usage

### Option 1: Web Interface (Recommended)

Start the Flask web server:
```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

Features:
- Modern, responsive chat UI
- Real-time messaging
- Conversation history
- User sessions
- Typing indicators

### Option 2: Enhanced CLI

Run the enhanced command-line interface:
```bash
python chatbot_cli.py
```

Features:
- Colored output
- Session management
- Conversation history (`history` command)
- Session statistics (`stats` command)
- Help menu (`help` command)

### Option 3: Original CLI

Run the original chatbot:
```bash
python chatbot.py
```

## 📊 Analytics & Learning

### View Analytics

```python
from analytics import Analytics

# Print comprehensive report
Analytics.print_report()

# Get specific metrics
overview = Analytics.get_overview()
intent_performance = Analytics.get_intent_performance()
```

### Learning Engine

```python
from learning_engine import LearningEngine

# Get improvement suggestions
suggestions = LearningEngine.get_improvement_suggestions()

# Export learned patterns
LearningEngine.export_training_data('learned_intents.json')
```

## 🔌 API Integration

The chatbot includes mock APIs for:

- **Products**: Search, pricing, inventory
- **Orders**: Tracking, status updates
- **Shipping**: Delivery estimates, tracking numbers
- **Returns**: Policy info, return initiation

Example usage:
```python
from api_handler import APIHandler

# Track an order
result = APIHandler.get_order_status("ORD-2024-001")

# Search products
products = APIHandler.get_product_info(product_name="laptop")

# Get shipping info
shipping = APIHandler.get_shipping_info()
```

## 💾 Database Schema

- **users**: User profiles and preferences
- **conversations**: Chat sessions
- **messages**: All messages with intent/confidence
- **feedback**: User ratings and comments
- **products**: Product catalog (10 sample products)
- **orders**: Order tracking (4 sample orders)

## 🎨 Web Interface

The web interface features:
- **Premium Design**: Gradient backgrounds, glassmorphism effects
- **Responsive Layout**: Works on desktop and mobile
- **Smooth Animations**: Fade-ins, typing indicators
- **User-Friendly**: Clean message bubbles, auto-scroll

## 📈 Example Conversations

### Order Tracking
```
User: Track my order ORD-2024-001
Bot: Your order ORD-2024-001 is currently Delivered. Your order has been delivered.
```

### Product Inquiry
```
User: What products do you have?
Bot: We offer a wide range of products including electronics, clothing, home goods, and more.
```

### Context-Aware Follow-up
```
User: How much does it cost?
Bot: Our products range from $12.99 to $1299.99. What specific product are you interested in?
```

## 🔧 Configuration

### Adjust Confidence Threshold

In `chatbot_enhanced.py`:
```python
self.confidence_threshold = 0.5  # Default: 0.5
```

### Add New Intents

Edit `intents.json`:
```json
{
  "tag": "new_intent",
  "patterns": ["example pattern 1", "example pattern 2"],
  "responses": ["response 1", "response 2"]
}
```

Then retrain:
```bash
python train_model.py
```

## 🚀 Advanced Features

### Conversation Context

The chatbot remembers:
- Previous messages in the session
- Extracted entities (order numbers, emails, phone numbers)
- Last intent for follow-up questions
- User preferences and history

### Entity Extraction

Automatically extracts:
- Order numbers (ORD-YYYY-NNN format)
- Email addresses
- Phone numbers

### Learning from Feedback

- Collects user ratings (positive/negative)
- Identifies low-confidence predictions
- Generates new training data from successful conversations
- Provides improvement suggestions

## 📊 Performance Metrics

Current performance:
- **Test Accuracy**: 92.3% on automated tests
- **Training Samples**: 113 patterns across 12 intents
- **Model**: TF-IDF + Multinomial Naive Bayes
- **Response Time**: < 100ms average

## 🔮 Future Enhancements

- Real-time model retraining
- Multi-language support
- Voice interface integration
- Advanced NLP models (BERT, GPT)
- Integration with real e-commerce APIs
- Sentiment analysis
- Proactive suggestions

## 🐛 Troubleshooting

**Model not found error**:
```bash
python train_model.py
```

**Database error**:
```bash
python init_db.py
```

**NLTK data missing**:
```bash
python nlp_utils.py
```

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Built as an advanced learning project for understanding NLP, chatbot design, web development, and full-stack application architecture.

---

**Ready to chat?** Start with `python app.py` and visit http://localhost:5000! 🚀
