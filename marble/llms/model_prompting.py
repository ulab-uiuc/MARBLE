import litellm
from beartype import beartype
from beartype.typing import Any, Dict, List, Optional
from litellm.types.utils import Message
from litellm.utils import trim_messages

from .error_handler import api_calling_error_exponential_backoff


@beartype
@api_calling_error_exponential_backoff(retries=5, base_wait_time=10)


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
    """

    if 'fireworks_ai' not in llm_model:
        completion = litellm.completion(
            model=llm_model,
            # api_key = "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",
            messages=trim_messages(messages, model=llm_model, max_tokens=int(16384 * 0.6)),
            max_tokens=max_token_num,
            n=return_num,
            top_p=top_p,
            temperature=temperature,
            stream=stream,
            tools=tools,
            tool_choice=tool_choice
        )
        message_0: Message = completion.choices[0].message
        assert message_0 is not None
        assert isinstance(message_0, Message)
        return [message_0]
    else:
        llm_model = llm_model.split('/', 1)[-1]
        completion = litellm.completion(
            model='openai/'+llm_model,
            api_base='https://api.fireworks.ai/inference/v1',
            api_key='fw_3ZghkaiZXewcBtUoU9pjoD3K',
            # fw_3ZghkaiZXewcBtUoU9pjoD3K
            # api_key = "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",
            messages=trim_messages(messages, model=llm_model, max_tokens=int(16384 * 0.6)),
            max_tokens=max_token_num,
            n=return_num,
            top_p=top_p,
            temperature=temperature,
            stream=stream,
            tools=tools,
            tool_choice=tool_choice
        )
        message_0: Message = completion.choices[0].message
        assert message_0 is not None
        assert isinstance(message_0, Message)
        return [message_0]
