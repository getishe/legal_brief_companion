from langchain.prompts import PromptTemplate
import re
import textwrap

def get_prompt_template(query_type: str) -> PromptTemplate:
    templates = {
        "default": "Please provide information about: {query}",
        "summary": "Summarize the following content:\n\n{content}",
        "question": textwrap.dedent("""
            Use the following context to answer the question.

            Context:
            {context}

            Question:
            {question}

            Answer:
        """).strip(),
        "explanation": "Explain the following concept:\n\n{concept}",
    }

    template_str = templates.get(query_type, templates["default"])
    input_vars = re.findall(r"{(.*?)}", template_str)

    return PromptTemplate(template=template_str, input_variables=input_vars)
