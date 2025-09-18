from langchain.document_loaders import PyPDFLoader

# Load your legal document
loader = PyPDFLoader("sheridan_quashawn_v_state_criminal.pdf")
documents = loader.load()
