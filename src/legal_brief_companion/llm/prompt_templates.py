# from langchain.prompts import PromptTemplate
# import re
# import textwrap

# def get_prompt_template(query_type: str) -> PromptTemplate:
#     templates = {
#         "default": "Please provide information about: {query}",
#         "summary": "Summarize the following context:\n\n{context}",
#         "question": textwrap.dedent("""
#             Use the following context to answer the question.

#             Context:
#             {context}

#             Question:
#             {question}

#             Answer:
#         """).strip(),
#         "explanation": "Explain the following concept:\n\n{concept}",
#     }

#     template_str = templates.get(query_type, templates["default"])
#     input_vars = re.findall(r"{(.*?)}", template_str)


#     return PromptTemplate(template=template_str, input_variables=input_vars)
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
