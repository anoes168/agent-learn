
import json

from .LLM_load import predict
from .tools import TOOL_FUNCTION


def run_agent(message, model, tokenizer):
    max_round = 5
    start_tag = "<tool_call>"
    end_tag = "</tool_call>"

    for round_index in range(max_round):
        print(f"\n 第{round_index + 1}轮")
        answer = predict(message, model, tokenizer)

        message.append({
            "role":"assistant",
            "content":answer,
        })

        if start_tag not in answer:
            print("模型回答:", answer)
            break

        if end_tag not in answer:
            print("工具请求不完整，停止执行。")
            break
        print("模型请求工具:", answer)

        tool_json = answer.split(start_tag,1)[1].split(end_tag,1)[0]
        tool_call = json.loads(tool_json)

        tool_name = tool_call["name"]
        arguments = tool_call["arguments"]
        if "a" not in arguments:
            message.append({
                "role": "tool",
                "content": "执行失败：缺少必需参数 a，请检查工具参数。"
            })
            continue
        if "b" not in arguments:
            message.append({
                "role": "tool",
                "content": "执行失败：缺少必需参数 b，请检查工具参数。",
            })
            continue

        if tool_name in TOOL_FUNCTION:
            function = TOOL_FUNCTION[tool_name]
            result = function(**arguments)
            print("工具结果：",result)
        else:
            print("未知工具：",tool_name)
            break

        message.append({
            "role":"tool",
            "content":str(result),
        })
    else:
        print("已到达最大调用论述，任务尚未得到解决")
