import openai
import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# Function to load and index documents
def load_and_index_documents(folder_path="."):
    print("Loading documents...")
    loader = DirectoryLoader(folder_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    print("Splitting and embedding documents...")
    embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
    vectorstore = Chroma.from_documents(documents, embeddings)

    print("Documents successfully indexed.")
    return vectorstore

# Function to create the AI agent
def create_agent(vectorstore):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    # Use ChatOpenAI for the correct v1/chat/completions endpoint
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai.api_key)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain

# Main script
if __name__ == "__main__":
    try:
        # Load and index documents
        folder_path = "."  # Folder containing your documents
        vectorstore = load_and_index_documents(folder_path)
        agent = create_agent(vectorstore)

        print("\nAI Agent: Hello! I can answer questions based on your documents. Ask me anything!")
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("AI Agent: Goodbye!")
                break
            try:
                # Use the invoke method for querying
                response = agent.invoke({"query": user_input})
                print(f"AI Agent: {response['result']}")
            except Exception as e:
                print(f"AI Agent: Sorry, I couldn't process your request. Error: {e}")
    except Exception as e:
        print(f"Error during setup: {e}")