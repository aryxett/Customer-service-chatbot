"""
Learning Engine for Continuous Improvement
Collects feedback and generates training data from conversations
"""

from database import Database, get_db_connection
import json
from datetime import datetime, timedelta

class LearningEngine:
    """Handles learning and model improvement"""
    
    @staticmethod
    def collect_misclassified_intents(confidence_threshold=0.5):
        """Find messages with low confidence scores"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.*, f.rating 
                FROM messages m
                LEFT JOIN feedback f ON f.message_id = m.id
                WHERE m.sender = 'user' 
                AND m.confidence < ?
                ORDER BY m.timestamp DESC
                LIMIT 100
            ''', (confidence_threshold,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_negative_feedback_messages():
        """Get messages with negative feedback"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.*, f.rating, f.comment
                FROM messages m
                JOIN feedback f ON f.message_id = m.id
                WHERE f.rating < 0
                ORDER BY f.timestamp DESC
            ''')
            
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def generate_training_data():
        """Generate new training data from conversations"""
        training_data = []
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get messages with high confidence and positive feedback
            cursor.execute('''
                SELECT m.message, m.intent, m.confidence, f.rating
                FROM messages m
                LEFT JOIN feedback f ON f.message_id = m.id
                WHERE m.sender = 'user' 
                AND m.intent IS NOT NULL
                AND m.confidence > 0.7
                AND (f.rating IS NULL OR f.rating > 0)
                GROUP BY m.message, m.intent
            ''')
            
            for row in cursor.fetchall():
                training_data.append({
                    'pattern': row['message'],
                    'intent': row['intent'],
                    'confidence': row['confidence']
                })
        
        return training_data
    
    @staticmethod
    def export_training_data(filename='learned_intents.json'):
        """Export learned patterns to JSON file"""
        training_data = LearningEngine.generate_training_data()
        
        # Group by intent
        intents_dict = {}
        for item in training_data:
            intent = item['intent']
            if intent not in intents_dict:
                intents_dict[intent] = []
            intents_dict[intent].append(item['pattern'])
        
        # Format for intents.json
        export_data = []
        for intent, patterns in intents_dict.items():
            export_data.append({
                'tag': intent,
                'patterns': list(set(patterns)),  # Remove duplicates
                'learned': True
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({'learned_intents': export_data}, f, indent=2, ensure_ascii=False)
        
        return len(export_data)
    
    @staticmethod
    def get_improvement_suggestions():
        """Get suggestions for model improvement"""
        suggestions = []
        
        # Check for low confidence messages
        low_conf = LearningEngine.collect_misclassified_intents()
        if len(low_conf) > 10:
            suggestions.append({
                'type': 'low_confidence',
                'count': len(low_conf),
                'suggestion': f'Found {len(low_conf)} messages with low confidence. Consider adding more training patterns.'
            })
        
        # Check for negative feedback
        negative = LearningEngine.get_negative_feedback_messages()
        if len(negative) > 5:
            suggestions.append({
                'type': 'negative_feedback',
                'count': len(negative),
                'suggestion': f'Found {len(negative)} messages with negative feedback. Review and improve responses.'
            })
        
        # Check intent distribution
        stats = Database.get_conversation_stats()
        if stats['intent_distribution']:
            top_intent = stats['intent_distribution'][0]
            if top_intent['count'] > stats['total_messages'] * 0.5:
                suggestions.append({
                    'type': 'intent_imbalance',
                    'intent': top_intent['intent'],
                    'suggestion': f'Intent "{top_intent["intent"]}" dominates ({top_intent["count"]} messages). Consider diversifying training data.'
                })
        
        return suggestions

if __name__ == "__main__":
    print("Learning Engine Test")
    print("=" * 60)
    
    # Get improvement suggestions
    suggestions = LearningEngine.get_improvement_suggestions()
    print(f"\nImprovement Suggestions: {len(suggestions)}")
    for s in suggestions:
        print(f"  - {s['suggestion']}")
    
    # Export training data
    count = LearningEngine.export_training_data()
    print(f"\nExported {count} learned intent patterns to 'learned_intents.json'")
