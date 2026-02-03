"""
API Handler for Dynamic Data Integration
Provides mock APIs for products, orders, inventory, and user data
"""

from database import Database
import random

class APIHandler:
    """Handles API calls for dynamic data"""
    
    @staticmethod
    def get_product_info(product_name=None, product_id=None):
        """Get product information"""
        if product_id:
            product = Database.get_product(product_id)
            if product:
                return {
                    'success': True,
                    'product': product
                }
            return {'success': False, 'error': 'Product not found'}
        
        if product_name:
            products = Database.search_products(product_name)
            if products:
                return {
                    'success': True,
                    'products': products,
                    'count': len(products)
                }
            return {'success': False, 'error': 'No products found'}
        
        # Return all products
        products = Database.get_all_products()
        return {
            'success': True,
            'products': products[:10],  # Limit to 10
            'count': len(products)
        }
    
    @staticmethod
    def get_product_price(product_name):
        """Get product price"""
        products = Database.search_products(product_name)
        if products:
            product = products[0]
            return {
                'success': True,
                'product_name': product['name'],
                'price': product['price'],
                'currency': 'USD'
            }
        return {'success': False, 'error': 'Product not found'}
    
    @staticmethod
    def check_inventory(product_name):
        """Check product inventory"""
        products = Database.search_products(product_name)
        if products:
            product = products[0]
            stock = product['stock']
            status = 'In Stock' if stock > 10 else 'Low Stock' if stock > 0 else 'Out of Stock'
            
            return {
                'success': True,
                'product_name': product['name'],
                'stock': stock,
                'status': status
            }
        return {'success': False, 'error': 'Product not found'}
    
    @staticmethod
    def get_order_status(order_number):
        """Get order status"""
        order = Database.get_order(order_number)
        if order:
            # Calculate estimated delivery (mock)
            status_info = {
                'Processing': 'Your order is being prepared. Expected ship date: 1-2 business days.',
                'Shipped': 'Your order has been shipped. Expected delivery: 3-5 business days.',
                'Delivered': 'Your order has been delivered.',
                'Cancelled': 'Your order has been cancelled.'
            }
            
            return {
                'success': True,
                'order_number': order['order_number'],
                'status': order['status'],
                'total': order['total'],
                'info': status_info.get(order['status'], 'Status unknown')
            }
        return {'success': False, 'error': 'Order not found'}
    
    @staticmethod
    def get_user_orders(user_id):
        """Get user's orders"""
        orders = Database.get_user_orders(user_id)
        return {
            'success': True,
            'orders': orders,
            'count': len(orders)
        }
    
    @staticmethod
    def get_shipping_info(order_number=None):
        """Get shipping information"""
        if order_number:
            order = Database.get_order(order_number)
            if order:
                # Mock tracking info
                tracking_number = f"TRK{random.randint(100000, 999999)}"
                return {
                    'success': True,
                    'order_number': order_number,
                    'tracking_number': tracking_number,
                    'carrier': 'FastShip Express',
                    'status': order['status']
                }
            return {'success': False, 'error': 'Order not found'}
        
        # General shipping info
        return {
            'success': True,
            'options': [
                {'name': 'Standard', 'duration': '5-7 business days', 'cost': 'Free'},
                {'name': 'Express', 'duration': '2-3 business days', 'cost': '$9.99'},
                {'name': 'Next Day', 'duration': '1 business day', 'cost': '$19.99'}
            ]
        }
    
    @staticmethod
    def get_return_policy():
        """Get return policy information"""
        return {
            'success': True,
            'policy': {
                'return_window': '30 days',
                'condition': 'Unused and in original packaging',
                'refund_time': '5-7 business days',
                'shipping': 'Free return shipping label provided'
            }
        }
    
    @staticmethod
    def initiate_return(order_number, reason=None):
        """Initiate a return (mock)"""
        order = Database.get_order(order_number)
        if order:
            return_id = f"RET-{random.randint(1000, 9999)}"
            return {
                'success': True,
                'return_id': return_id,
                'order_number': order_number,
                'message': 'Return initiated successfully. You will receive a return label via email.',
                'next_steps': [
                    'Check your email for the return label',
                    'Pack the item in original packaging',
                    'Attach the label and drop off at any shipping location'
                ]
            }
        return {'success': False, 'error': 'Order not found'}
    
    @staticmethod
    def get_user_profile(user_id):
        """Get user profile"""
        user = Database.get_user_by_id(user_id) if hasattr(Database, 'get_user_by_id') else None
        if user:
            return {
                'success': True,
                'user': user
            }
        return {'success': False, 'error': 'User not found'}
    
    @staticmethod
    def format_product_response(products):
        """Format product list for chatbot response"""
        if not products:
            return "I couldn't find any products matching your query."
        
        if len(products) == 1:
            p = products[0]
            return f"I found {p['name']} - ${p['price']}. {p['description']}. We have {p['stock']} in stock."
        
        response = f"I found {len(products)} products:\n"
        for p in products[:5]:  # Limit to 5
            response += f"• {p['name']} - ${p['price']}\n"
        
        if len(products) > 5:
            response += f"...and {len(products) - 5} more."
        
        return response

# Convenience functions for chatbot integration
def get_dynamic_response(intent, entities, user_context=None):
    """Get dynamic response based on intent and entities"""
    
    # Order tracking
    if intent == 'shipping' and 'order_number' in entities:
        result = APIHandler.get_order_status(entities['order_number'])
        if result['success']:
            return f"Your order {result['order_number']} is currently {result['status']}. {result['info']}"
    
    # Product search
    if intent == 'product_info' and user_context:
        # Extract product name from last message (simplified)
        result = APIHandler.get_product_info()
        if result['success'] and result.get('products'):
            return APIHandler.format_product_response(result['products'][:3])
    
    # Pricing
    if intent == 'pricing' and user_context:
        products = Database.get_all_products()
        if products:
            return f"Our products range from ${min(p['price'] for p in products):.2f} to ${max(p['price'] for p in products):.2f}. What specific product are you interested in?"
    
    return None  # No dynamic response available

if __name__ == "__main__":
    # Test API handler
    print("Testing API Handler...")
    
    # Test product info
    result = APIHandler.get_product_info(product_name="laptop")
    print(f"\nProduct search: {result}")
    
    # Test order status
    result = APIHandler.get_order_status("ORD-2024-001")
    print(f"\nOrder status: {result}")
    
    # Test shipping info
    result = APIHandler.get_shipping_info()
    print(f"\nShipping info: {result}")
    
    print("\nAPI Handler test complete!")
