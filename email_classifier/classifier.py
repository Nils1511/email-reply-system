from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class EmailClassifier:
    def __init__(self):
        self.llm = OpenAI(temperature=0)
        self.classify_prompt = PromptTemplate(
            input_variables=["email_content"],
            template="Classify the following email into one of these categories: Inquiry, Review, Assistance Request, or Other. Email content: {email_content}"
        )
        self.classify_chain = LLMChain(llm=self.llm, prompt=self.classify_prompt)

    def classify(self, email_content):
        return self.classify_chain.run(email_content)