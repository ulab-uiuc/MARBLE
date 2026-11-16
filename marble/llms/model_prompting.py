import os

import litellm
from beartype import beartype
from beartype.typing import Any, Dict, List, Optional
from litellm.types.utils import Message

from marble.llms.error_handler import api_calling_error_exponential_backoff

# Silently drop request parameters a provider does not support (e.g. ``top_p``
# or ``temperature`` on reasoning models) instead of failing the whole run.
litellm.drop_params = True


def _resolve_max_tokens(max_token_num: Optional[int]) -> Optional[int]:
    """
    Apply the optional ``MARBLE_MIN_MAX_TOKENS`` floor to a completion budget.

    Reasoning models (Gemini 2.5+/3.x, GPT-5, o-series, ...) spend part of the
    completion budget on hidden reasoning tokens, so the small per-call budgets
    used throughout MARBLE (256-512 tokens) can come back empty or truncated.
    Setting ``MARBLE_MIN_MAX_TOKENS=4096`` raises every budget to at least that
    value without touching the benchmark code.
    """
    floor = os.environ.get("MARBLE_MIN_MAX_TOKENS")
    if not floor or max_token_num is None:
        return max_token_num
    try:
        return max(max_token_num, int(floor))
    except ValueError:
        return max_token_num


@beartype
@api_calling_error_exponential_backoff(retries=5, base_wait_time=1)
def model_prompting(
    llm_model: str,
    messages: List[Dict[str, str]],
    return_num: Optional[int] = 1,
    max_token_num: Optional[int] = 512,
    temperature: Optional[float] = 0.0,
    top_p: Optional[float] = None,
    stream: Optional[bool] = None,
    mode: Optional[str] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: Optional[str] = None,
) -> List[Message]:
    """
    Select model via router in LiteLLM with support for function calling.

    Any LiteLLM model string works, e.g. ``gpt-4o-mini``,
    ``openrouter/google/gemini-2.5-flash``, ``gemini/gemini-2.5-flash`` or
    ``together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo``.

    Raises:
        Exception: The provider error, once all retries are exhausted.
    """
    # litellm.set_verbose=True
    if "together_ai/TA" in llm_model:
        base_url = "https://api.ohmygpt.com/v1"
    else:
        base_url = None
    completion = litellm.completion(
        model=llm_model,
        messages=messages,
        max_tokens=_resolve_max_tokens(max_token_num),
        n=return_num,
        top_p=top_p,
        temperature=temperature,
        stream=stream,
        tools=tools,
        tool_choice=tool_choice if tools else None,
        base_url=base_url,
    )
    message_0: Message = completion.choices[0].message
    assert message_0 is not None
    assert isinstance(message_0, Message)
    return [message_0]
