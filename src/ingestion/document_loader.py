import os

class DocumentLoader:
    def __init__(self, source_directory):
        self.source_directory = source_directory

    def load_documents(self):
        documents = []
        for filename in os.listdir(self.source_directory):
            if filename.endswith('.txt'):
                with open(os.path.join(self.source_directory, filename), 'r', encoding='utf-8') as file:
                    documents.append(file.read())
        return documents