"""
Context Manager for Conversation Tracking
Handles conversation state, history, and context-aware responses
"""

from datetime import datetime
from database import Database
import re

class ConversationContext:
    """Manages conversation context and state"""
    
    def __init__(self, session_id, user_id=None):
        self.session_id = session_id
        self.user_id = user_id
        self.conversation_id = None
        self.history = []
        self.entities = {}
        self.last_intent = None
        self.context_data = {}
        
        # Initialize or retrieve conversation
        self._init_conversation()
    
    def _init_conversation(self):
        """Initialize or retrieve existing conversation"""
        conv = Database.get_conversation(self.session_id)
        if conv:
            self.conversation_id = conv['id']
            # Load recent history
            messages = Database.get_conversation_messages(self.conversation_id, limit=10)
            self.history = list(reversed(messages))  # Oldest first
        else:
            self.conversation_id = Database.create_conversation(self.session_id, self.user_id)
    
    def add_message(self, sender, message, intent=None, confidence=None):
        """Add a message to the conversation"""
        message_id = Database.add_message(
            self.conversation_id, 
            sender, 
            message, 
            intent, 
            confidence
        )
        
        # Update history
        self.history.append({
            'id': message_id,
            'sender': sender,
            'message': message,
            'intent': intent,
            'confidence': confidence,
            'timestamp': datetime.now()
        })
        
        # Update last intent if from user
        if sender == 'user' and intent:
            self.last_intent = intent
        
        # Extract entities
        if sender == 'user':
            self._extract_entities(message)
        
        return message_id
    
    def _extract_entities(self, message):
        """Extract entities from message (order numbers, product names, etc.)"""
        # Extract order numbers (format: ORD-YYYY-NNN)
        order_pattern = r'ORD-\d{4}-\d{3}'
        orders = re.findall(order_pattern, message.upper())
        if orders:
            self.entities['order_number'] = orders[0]
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        if emails:
            self.entities['email'] = emails[0]
        
        # Extract phone numbers (simple pattern)
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, message)
        if phones:
            self.entities['phone'] = phones[0]
    
    def get_history(self, limit=5):
        """Get recent conversation history"""
        return self.history[-limit:] if self.history else []
    
    def get_context_for_intent(self, current_intent):
        """Get relevant context for intent prediction"""
        context = {
            'last_intent': self.last_intent,
            'entities': self.entities,
            'message_count': len(self.history),
            'has_order': 'order_number' in self.entities
        }
        
        # Check for follow-up patterns
        if self.last_intent and current_intent:
            context['is_followup'] = self._is_followup(self.last_intent, current_intent)
        
        return context
    
    def _is_followup(self, last_intent, current_intent):
        """Determine if current intent is a follow-up to last intent"""
        followup_patterns = {
            'product_info': ['pricing', 'shipping', 'returns'],
            'pricing': ['payment', 'shipping'],
            'shipping': ['returns', 'complaints'],
            'returns': ['shipping', 'complaints'],
            'complaints': ['help'],
        }
        
        return current_intent in followup_patterns.get(last_intent, [])
    
    def set_context_data(self, key, value):
        """Store arbitrary context data"""
        self.context_data[key] = value
    
    def get_context_data(self, key, default=None):
        """Retrieve context data"""
        return self.context_data.get(key, default)
    
    def clear_entities(self):
        """Clear extracted entities"""
        self.entities = {}
    
    def end_conversation(self):
        """Mark conversation as ended"""
        Database.end_conversation(self.session_id)
    
    def get_summary(self):
        """Get conversation summary"""
        return {
            'session_id': self.session_id,
            'message_count': len(self.history),
            'last_intent': self.last_intent,
            'entities': self.entities,
            'duration': self._calculate_duration()
        }
    
    def _calculate_duration(self):
        """Calculate conversation duration"""
        if len(self.history) < 2:
            return 0
        
        first = self.history[0]['timestamp']
        last = self.history[-1]['timestamp']
        
        if isinstance(first, str):
            first = datetime.fromisoformat(first)
        if isinstance(last, str):
            last = datetime.fromisoformat(last)
        
        duration = (last - first).total_seconds()
        return round(duration, 2)

class ContextManager:
    """Manages multiple conversation contexts"""
    
    def __init__(self):
        self.contexts = {}
    
    def get_context(self, session_id, user_id=None):
        """Get or create context for session"""
        if session_id not in self.contexts:
            self.contexts[session_id] = ConversationContext(session_id, user_id)
        return self.contexts[session_id]
    
    def remove_context(self, session_id):
        """Remove context (cleanup)"""
        if session_id in self.contexts:
            self.contexts[session_id].end_conversation()
            del self.contexts[session_id]
    
    def get_active_sessions(self):
        """Get list of active session IDs"""
        return list(self.contexts.keys())

if __name__ == "__main__":
    # Test context manager
    print("Testing Context Manager...")
    
    ctx = ConversationContext("test-session-123", user_id=1)
    
    # Add some messages
    ctx.add_message("user", "Hello, I need help with order ORD-2024-001", "help", 0.85)
    ctx.add_message("bot", "I'd be happy to help with your order!", None, None)
    ctx.add_message("user", "What's the status?", "help", 0.75)
    
    print(f"Entities extracted: {ctx.entities}")
    print(f"Message count: {len(ctx.history)}")
    print(f"Summary: {ctx.get_summary()}")
    print("\nContext Manager test complete!")
