"""
Customer Service Chatbot – Final Version with Confirmation & Undo
"""

import os
import pickle
import random
import re
from nlp_utils import download_nltk_data


class EnhancedChatbot:
    def __init__(self, model_dir="model"):
        self.model_dir = model_dir

        # NLP model
        self.vectorizer = None
        self.classifier = None

        # Conversation state
        self.help_shown = False
        self.waiting_for_order_id = False
        self.waiting_for_refund_reason = False

        self.last_order_id = None
        self.last_order_status = None

        self.awaiting_cancel_confirmation = False
        self.cancelled_order_backup = None  # for undo

        self.load_model()

    # ---------------- LOAD MODEL ---------------- #

    def load_model(self):
        with open(os.path.join(self.model_dir, "vectorizer.pkl"), "rb") as f:
            self.vectorizer = pickle.load(f)
        with open(os.path.join(self.model_dir, "classifier.pkl"), "rb") as f:
            self.classifier = pickle.load(f)

    # ---------------- HELPERS ---------------- #

    def extract_order_id(self, text):
        match = re.search(r"(ORD|ORDER)[-_]?\d+", text.upper())
        return match.group(0) if match else None

    def fake_order(self, order_id):
        status = random.choice(["Out for delivery", "In transit", "Delivered"])
        return {
            "status": status,
            "expected": "Tomorrow" if status != "Delivered" else "Delivered",
            "location": "City warehouse" if status != "Delivered" else "Customer address"
        }

    # ---------------- CHAT ---------------- #

    def chat(self, user_input):
        text = user_input.lower().strip()

        # ----- CONFIRM CANCELLATION -----
        if self.awaiting_cancel_confirmation:
            if text in ["yes", "y"]:
                self.awaiting_cancel_confirmation = False

                # Delivered orders cannot be cancelled
                if self.last_order_status == "Delivered":
                    return (
                        f"❌ Order **{self.last_order_id}** has already been delivered and cannot be cancelled."
                    )

                # Backup for undo
                self.cancelled_order_backup = self.last_order_id
                cancelled = self.last_order_id
                self.last_order_id = None
                self.last_order_status = None

                return (
                    f"❌ Order **{cancelled}** has been cancelled successfully.\n\n"
                    "If this was a mistake, type **undo**."
                )

            if text in ["no", "n"]:
                self.awaiting_cancel_confirmation = False
                return "👍 Cancellation aborted. Your order is still active."

            return "Please reply with **Yes** or **No**."

        # ----- UNDO CANCELLATION -----
        if "undo" in text and self.cancelled_order_backup:
            restored = self.cancelled_order_backup
            self.last_order_id = restored
            self.last_order_status = "In transit"
            self.cancelled_order_backup = None

            return (
                f"✅ Cancellation undone.\n"
                f"Order **{restored}** is active again and currently in transit."
            )

        # ----- WAITING FOR ORDER ID -----
        if self.waiting_for_order_id:
            order_id = self.extract_order_id(text)
            if not order_id:
                return "Please share a valid **order ID** (example: ORD12345)."

            self.waiting_for_order_id = False
            details = self.fake_order(order_id)

            self.last_order_id = order_id
            self.last_order_status = details["status"]

            return (
                f"📦 Order **{order_id}** details:\n"
                f"• Status: {details['status']}\n"
                f"• Expected delivery: {details['expected']}\n"
                f"• Current location: {details['location']}\n\n"
                "Can I help you with anything else?"
            )

        # ----- REFUND FLOW -----
        if self.waiting_for_refund_reason:
            self.waiting_for_refund_reason = False
            return (
                "✅ Refund request submitted.\n"
                "Your refund will be processed within 5–7 business days.\n\n"
                "Anything else I can help you with?"
            )

        # ----- CANCEL ORDER -----
        if "cancel" in text:
            if not self.last_order_id:
                self.waiting_for_order_id = True
                return "Sure 👍 Please share your **order ID** to cancel the order."

            self.awaiting_cancel_confirmation = True
            return (
                f"⚠️ Are you sure you want to cancel order **{self.last_order_id}**?\n"
                "Reply **Yes** or **No**."
            )

        # ----- ORDER / DELIVERY SHORTCUT -----
        if "order" in text or "delivery" in text or "where is" in text:
            self.waiting_for_order_id = True
            return (
                "I can help with your order 😊\n"
                "Please share your **order ID** so I can check its status."
            )

        # ----- REFUND -----
        if "refund" in text or "money back" in text:
            self.waiting_for_refund_reason = True
            return "I can help with a refund 👍 What is the reason?"

        # ----- GREETING -----
        if "hi" in text or "hello" in text:
            if not self.help_shown:
                self.help_shown = True
                return (
                    "Hello! 👋 How can I help you today?\n"
                    "• Track an order\n"
                    "• Delivery issues\n"
                    "• Refunds\n"
                    "• Cancel an order"
                )
            return "Hi again 😊 What would you like help with?"

        # ----- HUMAN AGENT -----
        if "human" in text or "agent" in text:
            return "👤 Connecting you to a human support agent. Please wait..."

        # ----- FALLBACK -----
        return (
            "I’m here to help 🙂\n"
            "You can ask about your **order**, **delivery**, **refund**, or **cancellation**."
        )


# ---------------- TEST MODE ---------------- #
if __name__ == "__main__":
    download_nltk_data()
    bot = EnhancedChatbot()

    while True:
        msg = input("You: ")
        print("Bot:", bot.chat(msg))

