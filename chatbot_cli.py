"""
Enhanced CLI for Customer Service Chatbot
Features: colored output, context awareness, session management
"""

from chatbot_enhanced import EnhancedChatbot
from context_manager import ConversationContext
from database import Database
from colorama import init, Fore, Style
import uuid
from datetime import datetime

# Initialize colorama for Windows
init(autoreset=True)

class EnhancedCLI:
    """Enhanced command-line interface with colors and context"""
    
    def __init__(self):
        self.chatbot = EnhancedChatbot()
        self.context = None
        self.username = None
        self.session_id = None
        
    def print_header(self):
        """Print colorful header"""
        print(Fore.CYAN + Style.BRIGHT + "=" * 60)
        print(Fore.MAGENTA + Style.BRIGHT + "Customer Service Chatbot - Enhanced CLI")
        print(Fore.CYAN + Style.BRIGHT + "=" * 60)
        print()
    
    def get_username(self):
        """Get username from user"""
        print(Fore.YELLOW + "Welcome! Please enter your name (or press Enter for 'guest'):")
        username = input(Fore.WHITE + "> ").strip()
        return username if username else "guest"
    
    def start_session(self):
        """Start a new chat session"""
        self.username = self.get_username()
        
        # Get or create user
        user = Database.get_or_create_user(self.username)
        user_id = user['id']
        
        # Create session
        self.session_id = f"cli_{uuid.uuid4().hex[:8]}"
        self.context = ConversationContext(self.session_id, user_id)
        
        print()
        print(Fore.GREEN + f"Hello, {self.username}! Your session has started.")
        print(Fore.CYAN + "Type 'quit', 'exit', or 'bye' to end the conversation.")
        print(Fore.CYAN + "Type 'help' for available commands.")
        print(Fore.CYAN + "=" * 60)
        print()
    
    def print_bot_message(self, message):
        """Print bot message in color"""
        print(Fore.BLUE + Style.BRIGHT + "Bot: " + Fore.WHITE + message)
        print()
    
    def print_user_message(self, message):
        """Print user message in color"""
        print(Fore.GREEN + Style.BRIGHT + "You: " + Fore.WHITE + message)
    
    def print_info(self, message):
        """Print info message"""
        print(Fore.YELLOW + "[INFO] " + message)
        print()
    
    def show_help(self):
        """Show available commands"""
        help_text = """
Available Commands:
  help     - Show this help message
  history  - Show conversation history
  stats    - Show session statistics
  clear    - Clear screen
  quit     - Exit the chatbot
        """
        print(Fore.CYAN + help_text)
    
    def show_history(self):
        """Show conversation history"""
        history = self.context.get_history(limit=10)
        
        if not history:
            self.print_info("No conversation history yet.")
            return
        
        print(Fore.CYAN + "\n--- Conversation History ---")
        for msg in history:
            sender = msg['sender'].capitalize()
            text = msg['message']
            color = Fore.GREEN if sender == 'User' else Fore.BLUE
            print(color + f"{sender}: {text}")
        print()
    
    def show_stats(self):
        """Show session statistics"""
        summary = self.context.get_summary()
        
        print(Fore.CYAN + "\n--- Session Statistics ---")
        print(Fore.WHITE + f"Session ID: {summary['session_id']}")
        print(Fore.WHITE + f"Messages: {summary['message_count']}")
        print(Fore.WHITE + f"Duration: {summary['duration']} seconds")
        print(Fore.WHITE + f"Last Intent: {summary['last_intent']}")
        if summary['entities']:
            print(Fore.WHITE + f"Entities: {summary['entities']}")
        print()
    
    def run(self):
        """Run the enhanced CLI"""
        self.print_header()
        self.start_session()
        
        # Initial greeting
        self.print_bot_message(
            "Hello! I'm your customer service assistant. "
            "I can help you with products, orders, shipping, returns, and more. "
            "How can I assist you today?"
        )
        
        while True:
            try:
                # Get user input
                user_input = input(Fore.GREEN + Style.BRIGHT + "You: " + Fore.WHITE).strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    self.context.end_conversation()
                    print()
                    self.print_bot_message(
                        f"Goodbye, {self.username}! Thank you for chatting with me. "
                        "Have a great day!"
                    )
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                if user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                
                if user_input.lower() == 'clear':
                    import os
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.print_header()
                    continue
                
                # Get bot response
                response_data = self.chatbot.chat_with_context(user_input, self.context)
                
                # Add messages to context
                self.context.add_message(
                    'user', 
                    user_input, 
                    response_data['intent'], 
                    response_data['confidence']
                )
                self.context.add_message('bot', response_data['response'])
                
                # Print response
                print()
                self.print_bot_message(response_data['response'])
                
                # Show intent and confidence (debug info)
                if response_data['confidence'] < 0.7:
                    print(Fore.YELLOW + Style.DIM + 
                          f"[Confidence: {response_data['confidence']:.2f}]")
                    print()
                
            except KeyboardInterrupt:
                print("\n")
                self.print_info("Interrupted. Type 'quit' to exit properly.")
            except Exception as e:
                print(Fore.RED + f"\nError: {e}")
                print()

def main():
    """Main function"""
    cli = EnhancedCLI()
    cli.run()

if __name__ == "__main__":
    main()
