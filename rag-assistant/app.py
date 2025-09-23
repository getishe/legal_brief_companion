from dotenv import load_dotenv
from logchain_Groq import ChatGroq


# Load environment variables from .env file
load_dotenv()

# Initialize the ChatGroq
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.0,
    max_retries=2,
    )

result = llm.chat("What is the capital of France?")
print(result)
print("-----")
print(result.completion)











# from ingestion.document_loader import DocumentLoader
# from ingestion.text_splitter import TextSplitter
# from retrieval.vector_store import VectorStore
# from retrieval.retriever import Retriever
# from llm.chain import LLMChain
# from interface.cli import run_cli

# def main():
#     # Initialize components
#     document_loader = DocumentLoader()
#     text_splitter = TextSplitter()
#     vector_store = VectorStore()
#     retriever = Retriever(vector_store)
#     llm_chain = LLMChain()

#     # Load and process documents
#     documents = document_loader.load_documents()
#     chunks = text_splitter.split_documents(documents)
#     vector_store.store_embeddings(chunks)

#     # Start the command-line interface
#     run_cli(retriever, llm_chain)

# if __name__ == "__main__":
#     main()