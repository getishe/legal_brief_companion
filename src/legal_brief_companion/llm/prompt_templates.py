
from langchain_core.prompts import PromptTemplate

def get_prompt_template(query_type: str) -> PromptTemplate:
   if query_type == "citation":
    return PromptTemplate(
        input_variables=["context", "query"],
        template="""
Use the following legal context to answer the question. Cite specific page numbers and rulings.

Context:
{context}

Question:
{query}
""".strip()
    )

    # Add other query types as needed
