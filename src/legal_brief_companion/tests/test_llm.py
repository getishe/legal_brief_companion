import pytest

from legal_brief_companion.llm.prompt_templates import get_prompt_template


@pytest.mark.parametrize(
    "query_type",
    ["question", "summary", "argument", "citation"],
)
def test_supported_prompt_types(query_type):
    prompt = get_prompt_template(query_type)
    assert "{context}" in prompt.template
    assert "{query}" in prompt.template


def test_unknown_prompt_type_is_rejected():
    with pytest.raises(ValueError, match="Unsupported query type"):
        get_prompt_template("student speech rights")
