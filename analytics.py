"""
Analytics Module for Chatbot Performance Tracking
Provides insights into conversations, intents, and user satisfaction
"""

from database import Database, get_db_connection
from datetime import datetime, timedelta
import json

class Analytics:
    """Analytics and reporting for chatbot performance"""
    
    @staticmethod
    def get_overview():
        """Get overall chatbot statistics"""
        stats = Database.get_conversation_stats()
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get feedback stats
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_feedback,
                    SUM(CASE WHEN rating > 0 THEN 1 ELSE 0 END) as positive,
                    SUM(CASE WHEN rating < 0 THEN 1 ELSE 0 END) as negative
                FROM feedback
            ''')
            feedback = dict(cursor.fetchone())
            
            # Calculate satisfaction rate
            if feedback['total_feedback'] > 0:
                satisfaction_rate = (feedback['positive'] / feedback['total_feedback']) * 100
            else:
                satisfaction_rate = 0
            
            # Get active users
            cursor.execute('SELECT COUNT(DISTINCT user_id) as active_users FROM conversations')
            active_users = cursor.fetchone()['active_users']
        
        return {
            **stats,
            'feedback': feedback,
            'satisfaction_rate': round(satisfaction_rate, 2),
            'active_users': active_users
        }
    
    @staticmethod
    def get_intent_performance():
        """Get performance metrics per intent"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    m.intent,
                    COUNT(*) as total_messages,
                    AVG(m.confidence) as avg_confidence,
                    COUNT(f.id) as feedback_count,
                    SUM(CASE WHEN f.rating > 0 THEN 1 ELSE 0 END) as positive_feedback
                FROM messages m
                LEFT JOIN feedback f ON f.message_id = m.id
                WHERE m.intent IS NOT NULL AND m.sender = 'user'
                GROUP BY m.intent
                ORDER BY total_messages DESC
            ''')
            
            results = []
            for row in cursor.fetchall():
                row_dict = dict(row)
                if row_dict['feedback_count'] > 0:
                    row_dict['satisfaction'] = round((row_dict['positive_feedback'] / row_dict['feedback_count']) * 100, 2)
                else:
                    row_dict['satisfaction'] = None
                row_dict['avg_confidence'] = round(row_dict['avg_confidence'], 3) if row_dict['avg_confidence'] else 0
                results.append(row_dict)
            
            return results
    
    @staticmethod
    def get_recent_conversations(limit=10):
        """Get recent conversation summaries"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    c.id,
                    c.session_id,
                    c.started_at,
                    c.ended_at,
                    u.username,
                    COUNT(m.id) as message_count
                FROM conversations c
                LEFT JOIN users u ON u.id = c.user_id
                LEFT JOIN messages m ON m.conversation_id = c.id
                GROUP BY c.id
                ORDER BY c.started_at DESC
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_common_queries(limit=20):
        """Get most common user queries"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    message,
                    intent,
                    COUNT(*) as frequency,
                    AVG(confidence) as avg_confidence
                FROM messages
                WHERE sender = 'user' AND intent IS NOT NULL
                GROUP BY message, intent
                ORDER BY frequency DESC
                LIMIT ?
            ''', (limit,))
            
            results = []
            for row in cursor.fetchall():
                row_dict = dict(row)
                row_dict['avg_confidence'] = round(row_dict['avg_confidence'], 3)
                results.append(row_dict)
            
            return results
    
    @staticmethod
    def get_time_based_stats(days=7):
        """Get statistics for the last N days"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            cursor.execute('''
                SELECT 
                    DATE(started_at) as date,
                    COUNT(*) as conversations
                FROM conversations
                WHERE started_at >= ?
                GROUP BY DATE(started_at)
                ORDER BY date
            ''', (cutoff_date,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def generate_report():
        """Generate comprehensive analytics report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'overview': Analytics.get_overview(),
            'intent_performance': Analytics.get_intent_performance(),
            'common_queries': Analytics.get_common_queries(10),
            'recent_conversations': Analytics.get_recent_conversations(5)
        }
        
        return report
    
    @staticmethod
    def print_report():
        """Print formatted analytics report"""
        report = Analytics.generate_report()
        
        print("=" * 60)
        print("CHATBOT ANALYTICS REPORT")
        print("=" * 60)
        print(f"\nGenerated: {report['generated_at']}")
        
        print("\n--- OVERVIEW ---")
        overview = report['overview']
        print(f"Total Conversations: {overview['total_conversations']}")
        print(f"Total Messages: {overview['total_messages']}")
        print(f"Active Users: {overview['active_users']}")
        print(f"Avg Messages/Conversation: {overview['avg_messages_per_conversation']}")
        print(f"Satisfaction Rate: {overview['satisfaction_rate']}%")
        
        print("\n--- TOP INTENTS ---")
        for intent in report['intent_performance'][:5]:
            print(f"{intent['intent']}: {intent['total_messages']} messages "
                  f"(confidence: {intent['avg_confidence']})")
        
        print("\n--- COMMON QUERIES ---")
        for query in report['common_queries'][:5]:
            print(f"'{query['message'][:50]}...' ({query['frequency']}x)")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    Analytics.print_report()
