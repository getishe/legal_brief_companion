from legal_brief_companion.llm.chain import build_chain

query = "Summarize the ruling in Tinker v. Des Moines"
chain, docs = build_chain(query_type="student speech rights")

output = chain.invoke({"query": query})
response = output["result"]

print("\n🧠 Chain Response:\n", response)

print("\n📄 Source Pages:")
for doc in output["source_documents"]:
    page = doc.metadata.get("page_label", doc.metadata.get("page"))
    print(f"- {doc.metadata['source']}, page {page}")
# poetry run python src/legal_brief_companion/tests/test_chain.py
