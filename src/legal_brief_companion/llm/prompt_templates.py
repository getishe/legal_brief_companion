
from langchain_core.prompts import PromptTemplate


def get_prompt_template(query_type: str) -> PromptTemplate:
    templates = {
        "question": """
Answer the legal research question using only the supplied context.

Requirements:
- Answer directly and concisely; include only details needed to answer the question.
- Explain the answer clearly and distinguish facts from legal conclusions.
- Cite the supporting source and page number for each material claim.
- Treat the supplied document as the only authority. If it does not support an answer, say that clearly instead of filling gaps from general knowledge.
- Separate direct statements in the document from your inferences.
- Do not invent authorities or page numbers.
- End with "Not legal advice."

Context:
{context}

Question:
{question}
""".strip(),
        "summary": """
Summarize the supplied legal material for a legal research briefing.

Requirements:
- Keep the summary focused; avoid repeating the same point.
- Include the issue, rule, holding, reasoning, and practical significance.
- Label the source and page for each major point.
- Separate verified points from any inference.
- Do not add authorities that are absent from the context.
- If an element is not addressed by the document, label it as missing rather than assuming it.
- End with "Not legal advice."

Context:
{context}

Briefing request:
{question}
""".strip(),
        "argument": """
Draft a legally responsible analysis of the issue using only the supplied context.

Requirements:
- Keep the analysis focused and avoid repeating points.
- Present the strongest argument supported by the sources.
- Address a likely counterargument.
- Cite the source and page for every significant proposition.
- Clearly identify gaps or uncertainty.
- Do not use facts or legal rules outside the supplied document.
- Do not invent authorities or represent the analysis as legal advice.
- End with "Not legal advice."

Context:
{context}

Issue:
{question}
""".strip(),
        "citation": """
Answer the question and provide a precise source trail.

Context:
{context}

Question:
{question}

Format:
1. Answer
2. Supporting authorities
3. Limitations or missing context

Keep each section concise.
Use only authorities in the context. Cite source and page number for each claim.
End with "Not legal advice."
""".strip(),
    }

    normalized = query_type.strip().lower()
    if normalized not in templates:
        supported = ", ".join(sorted(templates))
        raise ValueError(
            f"Unsupported query type '{query_type}'. Supported types: {supported}"
        )

    return PromptTemplate(
        input_variables=["context", "question"],
        template=templates[normalized],
    )
