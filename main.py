from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
from email_classifier.classifier import EmailClassifier
from rag_pipeline.pipeline import RAGPipeline
from email_response_generator.generator import EmailResponseGenerator

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Initialize components
email_classifier = EmailClassifier()
rag_pipeline = RAGPipeline("equipment_faq.txt")

def process_email(email_content):
    db = SessionLocal()
    try:
        # Classify email
        email_category = email_classifier.classify(email_content)

        # Generate response
        response_generator = EmailResponseGenerator(db, rag_pipeline)
        response = response_generator.generate_response(email_category, email_content)

        return response
    finally:
        db.close()

if __name__ == "__main__":
    # Example usage
    sample_email = "Hello, I'm interested in renting a camera for my upcoming film project. Do you have any available?"
    response = process_email(sample_email)
    print(response)