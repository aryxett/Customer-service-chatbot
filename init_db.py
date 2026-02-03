"""
Database Initialization Script
Creates tables and populates sample data
"""

from database import Database
import random

def init_database():
    """Initialize database with tables and sample data"""
    print("=" * 60)
    print("Database Initialization")
    print("=" * 60)
    
    # Create tables
    print("\n1. Creating database tables...")
    Database.create_tables()
    print("   [OK] Tables created")
    
    # Create sample users
    print("\n2. Creating sample users...")
    sample_users = [
        ('john_doe', 'john@example.com'),
        ('jane_smith', 'jane@example.com'),
        ('guest', None)
    ]
    
    for username, email in sample_users:
        try:
            Database.create_user(username, email)
        except:
            pass  # User might already exist
    print(f"   [OK] Created {len(sample_users)} users")
    
    # Create sample products
    print("\n3. Creating sample products...")
    sample_products = [
        ('Laptop Pro 15"', 'Electronics', 1299.99, 15, 'High-performance laptop with 16GB RAM'),
        ('Wireless Mouse', 'Electronics', 29.99, 50, 'Ergonomic wireless mouse'),
        ('USB-C Cable', 'Accessories', 12.99, 100, 'Fast charging USB-C cable'),
        ('Bluetooth Headphones', 'Electronics', 89.99, 30, 'Noise-cancelling headphones'),
        ('Phone Case', 'Accessories', 19.99, 75, 'Protective phone case'),
        ('Portable Charger', 'Electronics', 39.99, 40, '10000mAh power bank'),
        ('Laptop Bag', 'Accessories', 49.99, 25, 'Padded laptop backpack'),
        ('Webcam HD', 'Electronics', 69.99, 20, '1080p webcam with microphone'),
        ('Keyboard Mechanical', 'Electronics', 129.99, 18, 'RGB mechanical keyboard'),
        ('Monitor 24"', 'Electronics', 199.99, 12, 'Full HD IPS monitor'),
    ]
    
    from database import get_db_connection
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Check if products already exist
        cursor.execute('SELECT COUNT(*) as count FROM products')
        if cursor.fetchone()['count'] == 0:
            cursor.executemany(
                'INSERT INTO products (name, category, price, stock, description) VALUES (?, ?, ?, ?, ?)',
                sample_products
            )
    print(f"   [OK] Created {len(sample_products)} products")
    
    # Create sample orders
    print("\n4. Creating sample orders...")
    sample_orders = [
        (1, 'ORD-2024-001', 'Delivered', 1329.98),
        (1, 'ORD-2024-002', 'Shipped', 89.99),
        (2, 'ORD-2024-003', 'Processing', 249.97),
        (2, 'ORD-2024-004', 'Delivered', 69.99),
    ]
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Check if orders already exist
        cursor.execute('SELECT COUNT(*) as count FROM orders')
        if cursor.fetchone()['count'] == 0:
            cursor.executemany(
                'INSERT INTO orders (user_id, order_number, status, total) VALUES (?, ?, ?, ?)',
                sample_orders
            )
    print(f"   [OK] Created {len(sample_orders)} orders")
    
    print("\n" + "=" * 60)
    print("Database initialized successfully!")
    print("=" * 60)
    print("\nSample Data:")
    print(f"  - Users: {len(sample_users)}")
    print(f"  - Products: {len(sample_products)}")
    print(f"  - Orders: {len(sample_orders)}")
    print("\nDatabase ready for use!")

if __name__ == "__main__":
    init_database()
