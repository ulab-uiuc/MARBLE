import litellm

import os
from openai import OpenAI
from beartype import beartype
from beartype.typing import Any, Dict, List, Optional
from litellm.types.utils import Message

from .error_handler import api_calling_error_exponential_backoff

@beartype
@api_calling_error_exponential_backoff(retries=5, base_wait_time=1)
# def model_prompting(
#     llm_model: str,
#     messages: List[Dict[str, str]],
#     return_num: Optional[int] = 1,
#     max_token_num: Optional[int] = 512,
#     temperature: Optional[float] = 0.0,
#     top_p: Optional[float] = None,
#     stream: Optional[bool] = None,
#     mode: Optional[str] = None,
#     tools: Optional[List[Dict[str, Any]]] = None,
#     tool_choice: Optional[str] = None,
# ) -> List[Message]:
#     completion = litellm.completion(
#         model=llm_model,
#         messages=messages,
#         max_tokens=max_token_num,
#         n=return_num,
#         top_p=top_p,
#         temperature=temperature,
#         stream=stream,
#         tools=tools,
#         tool_choice=tool_choice
#     )
#     message_0: Message = completion.choices[0].message
#     assert message_0 is not None
#     assert isinstance(message_0, Message)
#     return [message_0]

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
    client = OpenAI(
        api_key="none",
        base_url="http://127.0.0.1:80/v1"
    )
    try:
        params = {
            "model": llm_model,
            "messages": messages,
            "max_tokens": max_token_num,
            "n": return_num,
            "temperature": temperature,
        }
        
        if top_p is not None:
            params["top_p"] = top_p
        if stream is not None:
            params["stream"] = stream
        if tools is not None:
            params["tools"] = tools
            if tool_choice is not None:
                params["tool_choice"] = tool_choice
        
        # 打印请求参数
        # print(f"发送请求：")
        # print(f"- 参数：{params}")
        
        completion = client.chat.completions.create(**params)
        
        # 打印响应内容
        # print(f"收到响应：")
        # print(f"- 完整响应：{completion}")
        
        message_0 = completion.choices[0].message
   
        tool_calls = None
        if message_0.tool_calls:
            tool_calls = []
            for tool_call in message_0.tool_calls:
                tool_calls.append({
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                })
        
        # 将 OpenAI 的消息转换为 litellm 的消息格式
        litellm_message = Message(
            content=message_0.content,
            role=message_0.role,
            tool_calls=tool_calls
        )
        
        return [litellm_message]
        
    except Exception as e:
        print(f"模型调用失败，详细信息：")
        print(f"- 模型：{llm_model}")
        print(f"- 消息：{messages}")
        print(f"- 错误：{str(e)}")
        if hasattr(e, 'response'):
            print(f"- 响应：{e.response.text if hasattr(e.response, 'text') else e.response}")
            print(f"- 响应状态码：{e.response.status_code if hasattr(e.response, 'status_code') else 'unknown'}")
            print(f"- 响应头：{e.response.headers if hasattr(e.response, 'headers') else 'unknown'}")
        raise e