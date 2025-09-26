from langchain.text_splitter import RecursiveCharacterTextSplitter

# Function to split documents into smaller chunks
def split_documents(documents, chunks_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunks_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    split_docs = text_splitter.split_documents(documents)
    return split_docs