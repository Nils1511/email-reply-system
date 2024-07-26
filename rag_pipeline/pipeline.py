from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

class RAGPipeline:
    def __init__(self, faq_file):
        with open(faq_file, 'r') as file:
            faq_text = file.read()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(faq_text)

        embeddings = OpenAIEmbeddings()
        self.docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))])

        self.qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=self.docsearch.as_retriever())

    def query(self, question):
        return self.qa.run(question)