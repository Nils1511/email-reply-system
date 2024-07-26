from sqlalchemy.orm import Session
from database.models import Equipment
from rag_pipeline.pipeline import RAGPipeline

class EmailResponseGenerator:
    def __init__(self, db: Session, rag_pipeline: RAGPipeline):
        self.db = db
        self.rag_pipeline = rag_pipeline

    def handle_inquiry(self, item_name):
        equipment = self.db.query(Equipment).filter(Equipment.name == item_name).first()
        if equipment:
            if equipment.availability:
                return f"The {item_name} is available for rent at ${equipment.price} per day."
            else:
                alternatives = self.db.query(Equipment).filter(
                    Equipment.category == equipment.category,
                    Equipment.availability == True
                ).limit(3).all()
                alt_str = ", ".join([alt.name for alt in alternatives])
                return f"Unfortunately, the {item_name} is not available. You might consider these alternatives: {alt_str}"
        else:
            return f"We don't have {item_name} in our inventory. Please check our website for a full list of available equipment."

    def handle_review(self, review_content):
        # This is a simplified version. In a real-world scenario, you'd use a more sophisticated sentiment analysis.
        if "great" in review_content.lower() or "excellent" in review_content.lower():
            return "Thank you for your positive feedback! We'd be grateful if you could share your experience on our social media pages."
        else:
            return "We're sorry to hear about your experience. A customer service representative will call you shortly to address your concerns. As a token of our appreciation, we're sending you a gift voucher for your next rental."

    def handle_assistance(self, query):
        result = self.rag_pipeline.query(query)
        if result:
            return f"Here's a possible solution to your issue: {result}"
        else:
            return "We couldn't find an immediate solution to your issue. A customer service representative will contact you shortly to assist you further."

    def generate_response(self, email_category, email_content):
        if email_category == "Inquiry":
            # Extract item name from email content (this would require more sophisticated NLP in a real-world scenario)
            item_name = email_content.split()[-1]  # Simplified: assumes the last word is the item name
            return self.handle_inquiry(item_name)
        elif email_category == "Review":
            return self.handle_review(email_content)
        elif email_category == "Assistance Request":
            return self.handle_assistance(email_content)
        else:
            return "Your email has been forwarded to our customer service team for further assistance."