import pytest

from legal_brief_companion.llm.prompt_templates import get_prompt_template


def test_prompts_reject_unknown_type_before_chain_creation():
    with pytest.raises(ValueError):
        get_prompt_template("unsupported")
