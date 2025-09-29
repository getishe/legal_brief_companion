from langchain.prompts import PromptTemplate

def get_prompt_template(query_type: str) -> PromptTemplate:
    templates = {
        "default": "Please provide information about: {query}",
        "summary": "Summarize the following content: {content}",
        "question": "Answer the question based on the provided context: {context}",
        "explanation": "Explain the following concept: {concept}",
    }
    
    template_str = templates.get(query_type, templates["default"])
    input_var = [var.strip("{}") for var in template_str.split() if var.startswith("{") and var.endswith("}")]
    return PromptTemplate(template=template_str, input_variables=input_var)
    # return templates.get(query_type, templates["default"])