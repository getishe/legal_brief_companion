def get_prompt_template(query_type: str) -> str:
    templates = {
        "default": "Please provide information about: {query}",
        "summary": "Summarize the following content: {content}",
        "question": "Answer the question based on the provided context: {context}",
        "explanation": "Explain the following concept: {concept}",
    }
    return templates.get(query_type, templates["default"])