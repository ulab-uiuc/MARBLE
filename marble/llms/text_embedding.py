import litellm
from beartype import beartype
from beartype.typing import List

from .error_handler import api_calling_error_exponential_backoff


@beartype
@api_calling_error_exponential_backoff(retries=5, base_wait_time=1)


def text_embedding(
    model: str,
    input: str,
) -> List[float]:
    """
    Select model via router in LiteLLM with support for function calling.
    """
    # litellm.set_verbose=True
    embedding = litellm.embedding(
        model=model,
        input=[input],
    )
    embedding_0 = embedding.data[0]["embedding"]
    assert embedding_0 is not None
    assert isinstance(embedding_0, list)
    return embedding_0
