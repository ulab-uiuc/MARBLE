import pytest

from marble.utils.json_utils import extract_json


def test_plain_json() -> None:
    assert extract_json('{"a": 1}') == {"a": 1}


def test_fenced_json_with_prose() -> None:
    text = 'Here is the plan:\n```json\n{"tasks": {"agent1": "x"}, "continue": true}\n```\nGood luck!'
    assert extract_json(text) == {"tasks": {"agent1": "x"}, "continue": True}


def test_json_with_comment_and_trailing_comma() -> None:
    text = '{\n  "continue": true // Set to false if the task is completed\n,}'
    assert extract_json(text) == {"continue": True}


def test_urls_inside_strings_survive_comment_stripping() -> None:
    text = '{"url": "https://example.com/a", "continue": true // done\n}'
    assert extract_json(text)["url"] == "https://example.com/a"


def test_json_array() -> None:
    text = '```json\n[{"milestone": "m", "agents": ["agent1"]}]\n```'
    assert extract_json(text, expect=list) == [{"milestone": "m", "agents": ["agent1"]}]


@pytest.mark.parametrize("bad", ["", None, "no json here", "{broken"])
def test_invalid_input_raises_value_error(bad) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(ValueError):
        extract_json(bad)
