from langchain_community.document_loaders import CSVLoader
from langchain_community.llms import GooglePalm
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv;
load_dotenv()
# Use the API key directly if not using environment variables
api_key = os.getenv("GOOGLE_API_KEY")
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.1)
instructor_embeddings = HuggingFaceInstructEmbeddings()
vectordb_file_path = "faiss_index"

def create_vector_db():
    loader = CSVLoader(file_path='/Users/aungnandaoo/Desktop/newRateGF.csv', source_column='prompt')
    docs = loader.load()
    print(f"Loaded {len(docs)} documents.")
    
    # Check if docs are loaded correctly
    if len(docs) == 0:
        print("No documents loaded. Check the CSV file and the source_column.")
        return

    vectordb = FAISS.from_documents(documents=docs, embedding=instructor_embeddings)
    vectordb.save_local(vectordb_file_path)
    print(f"FAISS index saved to {vectordb_file_path}.")

def get_qa_chain():
    # Load the vector database from the local folder
    vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings, allow_dangerous_deserialization=True)
    print(f"Loaded FAISS index from {vectordb_file_path}.")

    # Create a retriever for querying the vector database
    retriever = vectordb.as_retriever(score_threshold=0.7)

    prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from the "response" section in the source document context without making many changes.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type="stuff",
                                        retriever=retriever,
                                        input_key="query",
                                        return_source_documents=True,
                                        chain_type_kwargs={"prompt": PROMPT})

    return chain

# Create the vector database
create_vector_db()

# Retrieve the QA chain
qa_chain = get_qa_chain()
