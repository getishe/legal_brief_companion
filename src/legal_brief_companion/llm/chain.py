# from langchain.chains import retrieval_qa
# from langchain_groq import ChatGroq
# from src.llm.prompt_templates import get_prompt_template
# from src.retrieval.retriever import get_retriever

# def build_chain(query_type: str, chain_type: str= "stuff"):
#     retriever = get_retriever()
#     prompt_template = get_prompt_template(query_type)
#     llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     temperature=0.0,
#     max_retries=2,
#     # other params...
# )
#     chain = retrieval_qa.RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type=chain_type,
#         retriever=retriever,
#         return_source_documents=True,
#         chain_type_kwargs={"prompt": prompt_template}
#     )
    
#     print(f"🔗 Chain built with model: {llm.model}, prompt type: {query_type}")
      
#     return chain
# poetry run python src/interface/cli.py ingest
# poetry run python src/interface/cli.py query "What is the precedent in Tinker v. Des Moines?" --query-type question

from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from legal_brief_companion.config.settings import settings
from legal_brief_companion.llm.prompt_templates import get_prompt_template
from legal_brief_companion.retrieval.retriever import get_retriever


def build_chain(
    query_type: str,
    chain_type: str = "stuff",
    filters: dict = None,
    max_chunks: int = 4,
    max_tokens: int = 500,
    retriever=None,
):
    if retriever is None:
        retriever = get_retriever(filters, max_chunks)
    prompt_template = get_prompt_template(query_type)
    document_prompt = PromptTemplate(
        input_variables=["page", "source"],
        template="Source: {source}\nPage: {page}\n\n{page_content}",
    )

    # Dynamically select model from settings
    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.0,
        max_retries=2,
        groq_api_key=settings.GROQ_API_KEY,
        max_tokens=max_tokens,
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt_template,
            "document_prompt": document_prompt,
        },
    )
    return chain


def summarize_documents(
    documents,
    request: str = "Summarize this document.",
    progress_callback=None,
    batch_chars: int = 30000,
    max_tokens: int = 2048,
):
    """Summarize every document chunk through map/reduce passes with page labels."""
    if not documents:
        raise ValueError("There is no document content to summarize.")

    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.0,
        max_retries=2,
        groq_api_key=settings.GROQ_API_KEY,
        max_tokens=900,
    )
    final_llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.0,
        max_retries=2,
        groq_api_key=settings.GROQ_API_KEY,
        max_tokens=max_tokens,
    )

    batches = []
    batch = []
    batch_size = 0
    for doc in documents:
        source = doc.metadata.get("source", "Uploaded document")
        page = doc.metadata.get("page", "N/A")
        segment = f"Source: {source}; page {page}\n{doc.page_content.strip()}"
        if batch and batch_size + len(segment) > batch_chars:
            batches.append("\n\n".join(batch))
            batch = []
            batch_size = 0
        batch.append(segment)
        batch_size += len(segment)
    if batch:
        batches.append("\n\n".join(batch))

    partial_summaries = []
    for index, content in enumerate(batches, 1):
        prompt = f"""Summarize this portion of an uploaded document for a user who wants to understand the document.

Use only the text below. Preserve important facts and cite the source and page printed with them. Do not force legal brief categories such as issue, rule, or holding unless the text actually contains them. Mark uncertainty or missing information instead of guessing.

Document portion:
{content}
"""
        response = llm.invoke(prompt)
        partial_summaries.append(str(response.content).strip())
        if progress_callback:
            progress_callback(
                0.1 + 0.65 * index / len(batches),
                f"Summarized section {index} of {len(batches)}...",
            )

    # Reduce large collections of partial summaries in bounded batches until
    # they fit in one final synthesis request.
    while sum(len(item) for item in partial_summaries) > batch_chars:
        reduced = []
        group = []
        group_size = 0
        for item in partial_summaries:
            if group and group_size + len(item) > batch_chars:
                response = llm.invoke(
                    "Combine these summaries, removing repetition while preserving "
                    "important points and every source/page citation:\n\n"
                    + "\n\n".join(group)
                )
                reduced.append(str(response.content).strip())
                group = []
                group_size = 0
            group.append(item)
            group_size += len(item)
        if group:
            response = llm.invoke(
                "Combine these summaries, removing repetition while preserving "
                "important points and every source/page citation:\n\n"
                + "\n\n".join(group)
            )
            reduced.append(str(response.content).strip())
        if len(reduced) >= len(partial_summaries):
            raise ValueError("The document summary could not be reduced safely.")
        partial_summaries = reduced

    if progress_callback:
        progress_callback(0.82, "Writing the complete document summary...")
    summary_context = "\n\n".join(partial_summaries)
    final_prompt = f"""Write a clear, useful summary of the entire uploaded document using the section summaries below.

The document may be a workbook, opinion, brief, or another type of legal material. Describe what it actually contains; do not assume it is a judicial opinion or force an issue/rule/holding table. Keep the summary focused and avoid repetition. Cite source pages for material points, identify gaps, and do not add facts or legal rules that are not supported by the summaries. End with "Not legal advice."

User request: {request}

Section summaries covering the document:
{summary_context}
"""
    result = str(final_llm.invoke(final_prompt).content).strip()
    if progress_callback:
        progress_callback(1.0, "Complete document summary ready.")
    return result

