"""
Helpers for pulling JSON out of raw LLM responses.

LLMs rarely return bare JSON: the payload is usually wrapped in a markdown
code fence, preceded by some prose, or decorated with ``//`` comments. Every
component that asks a model for structured output should go through
:func:`extract_json` instead of calling ``json.loads`` on the raw text.
"""

import json
import re
from typing import Any, Optional

_FENCE_PATTERN = re.compile(r"```(?:json|JSON)?\s*(.*?)```", re.DOTALL)
_LINE_COMMENT_PATTERN = re.compile(r"(?m)(?<![:\"'\\/])//[^\n]*$")
_TRAILING_COMMA_PATTERN = re.compile(r",\s*([}\]])")


def _balanced_span(text: str, open_char: str, close_char: str) -> Optional[str]:
    """Return the first balanced ``open_char``...``close_char`` span in ``text``."""
    start = text.find(open_char)
    while start != -1:
        depth = 0
        in_string = False
        escaped = False
        for index in range(start, len(text)):
            char = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == open_char:
                depth += 1
            elif char == close_char:
                depth -= 1
                if depth == 0:
                    return text[start : index + 1]
        start = text.find(open_char, start + 1)
    return None


def _try_loads(candidate: str) -> Any:
    """Parse ``candidate`` leniently, raising ``ValueError`` on failure."""
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass
    # Models are often told "true // set to false when done" and echo it back.
    cleaned = _LINE_COMMENT_PATTERN.sub("", candidate)
    cleaned = _TRAILING_COMMA_PATTERN.sub(r"\1", cleaned)
    return json.loads(cleaned)


def extract_json(text: Optional[str], expect: type = dict) -> Any:
    """
    Extract the first JSON value of type ``expect`` from an LLM response.

    Args:
        text (Optional[str]): Raw model output.
        expect (type): ``dict`` (default) or ``list``.

    Returns:
        Any: The parsed JSON value.

    Raises:
        ValueError: If no JSON value of the expected type can be recovered.
    """
    if not text or not text.strip():
        raise ValueError("Empty response: no JSON to parse.")

    open_char, close_char = ("{", "}") if expect is dict else ("[", "]")

    candidates = [text.strip()]
    candidates.extend(match.strip() for match in _FENCE_PATTERN.findall(text))
    for source in list(candidates):
        span = _balanced_span(source, open_char, close_char)
        if span:
            candidates.append(span)
    # Last resort: everything between the first opener and the last closer.
    start, end = text.find(open_char), text.rfind(close_char)
    if start != -1 and end > start:
        candidates.append(text[start : end + 1])

    for candidate in candidates:
        try:
            value = _try_loads(candidate)
        except ValueError:
            continue
        if isinstance(value, expect):
            return value

    raise ValueError(
        f"JSON parsing failed: no valid JSON {expect.__name__} found in response."
    )
