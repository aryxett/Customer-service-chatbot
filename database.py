"""
Database module for Customer Service Chatbot
Handles all database operations using SQLite
"""

import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager

DATABASE_PATH = 'chatbot.db'

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

class Database:
    """Database operations handler"""
    
    @staticmethod
    def create_tables():
        """Create all database tables"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT,
                    preferences TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_id TEXT UNIQUE NOT NULL,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ended_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    sender TEXT NOT NULL,
                    message TEXT NOT NULL,
                    intent TEXT,
                    confidence REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            ''')
            
            # Feedback table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER NOT NULL,
                    rating INTEGER,
                    comment TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (message_id) REFERENCES messages(id)
                )
            ''')
            
            # Products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    price REAL,
                    stock INTEGER,
                    description TEXT
                )
            ''')
            
            # Orders table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    order_number TEXT UNIQUE NOT NULL,
                    status TEXT,
                    total REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id)')
    
    # User operations
    @staticmethod
    def create_user(username, email=None, preferences=None):
        """Create a new user"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            prefs_json = json.dumps(preferences) if preferences else None
            cursor.execute(
                'INSERT INTO users (username, email, preferences) VALUES (?, ?, ?)',
                (username, email, prefs_json)
            )
            return cursor.lastrowid
    
    @staticmethod
    def get_user(username):
        """Get user by username"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    @staticmethod
    def get_or_create_user(username, email=None):
        """Get existing user or create new one"""
        user = Database.get_user(username)
        if not user:
            user_id = Database.create_user(username, email)
            user = Database.get_user(username)
        return user
    
    # Conversation operations
    @staticmethod
    def create_conversation(session_id, user_id=None):
        """Create a new conversation"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO conversations (session_id, user_id) VALUES (?, ?)',
                (session_id, user_id)
            )
            return cursor.lastrowid
    
    @staticmethod
    def get_conversation(session_id):
        """Get conversation by session ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM conversations WHERE session_id = ?', (session_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    @staticmethod
    def end_conversation(session_id):
        """Mark conversation as ended"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE conversations SET ended_at = ? WHERE session_id = ?',
                (datetime.now(), session_id)
            )
    
    # Message operations
    @staticmethod
    def add_message(conversation_id, sender, message, intent=None, confidence=None):
        """Add a message to conversation"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (conversation_id, sender, message, intent, confidence) VALUES (?, ?, ?, ?, ?)',
                (conversation_id, sender, message, intent, confidence)
            )
            return cursor.lastrowid
    
    @staticmethod
    def get_conversation_messages(conversation_id, limit=50):
        """Get messages for a conversation"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp DESC LIMIT ?',
                (conversation_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    # Feedback operations
    @staticmethod
    def add_feedback(message_id, rating, comment=None):
        """Add feedback for a message"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO feedback (message_id, rating, comment) VALUES (?, ?, ?)',
                (message_id, rating, comment)
            )
            return cursor.lastrowid
    
    # Product operations
    @staticmethod
    def get_product(product_id):
        """Get product by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    @staticmethod
    def search_products(query):
        """Search products by name or category"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM products WHERE name LIKE ? OR category LIKE ? LIMIT 10',
                (f'%{query}%', f'%{query}%')
            )
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_all_products():
        """Get all products"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products')
            return [dict(row) for row in cursor.fetchall()]
    
    # Order operations
    @staticmethod
    def get_order(order_number):
        """Get order by order number"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM orders WHERE order_number = ?', (order_number,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    @staticmethod
    def get_user_orders(user_id):
        """Get all orders for a user"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    # Analytics
    @staticmethod
    def get_conversation_stats():
        """Get conversation statistics"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Total conversations
            cursor.execute('SELECT COUNT(*) as total FROM conversations')
            total_conversations = cursor.fetchone()['total']
            
            # Total messages
            cursor.execute('SELECT COUNT(*) as total FROM messages')
            total_messages = cursor.fetchone()['total']
            
            # Average messages per conversation
            avg_messages = total_messages / total_conversations if total_conversations > 0 else 0
            
            # Intent distribution
            cursor.execute('''
                SELECT intent, COUNT(*) as count 
                FROM messages 
                WHERE intent IS NOT NULL 
                GROUP BY intent 
                ORDER BY count DESC
            ''')
            intent_distribution = [dict(row) for row in cursor.fetchall()]
            
            return {
                'total_conversations': total_conversations,
                'total_messages': total_messages,
                'avg_messages_per_conversation': round(avg_messages, 2),
                'intent_distribution': intent_distribution
            }

if __name__ == "__main__":
    # Test database creation
    print("Creating database tables...")
    Database.create_tables()
    print("Database tables created successfully!")
