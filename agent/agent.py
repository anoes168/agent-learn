"""执行一次工具调用，并将结果交回模型。"""

import json

from .LLM_load import predict
from .tools import multiply


def run_agent(text, model, tokenizer):
    message = [
        {
            "role":"system",
            "content":(
                "你是一个工具助手，遇到整数的乘法问题，请调用multiply工具 "
                "收到工具结果后，根据结果回答用户，不要反复调用工具"
            )
        },
        {
            "role":"user",
            "content":text
        }
    ]
    max_round = 5
    start_tag = "<tool_call>"
    end_tag = "</tool_call>"

    for round_index in range(max_round):
        print(f"\n 第{round_index + 1}轮")
        answer = predict(message, model, tokenizer)
        print("模型输出:",answer)

        message.append({
            "role":"assistant",
            "content":answer,
        })

        if start_tag not in answer:
            print("最终回答：", answer)
            break

        if end_tag not in answer:
            print("工具请求不完整，停止执行。")
            break

        tool_json = answer.split(start_tag,1)[1].split(end_tag,1)[0]
        tool_call = json.loads(tool_json)

        tool_name = tool_call["name"]
        arguments = tool_call["arguments"]

        if tool_name == "multiply":
            result = multiply(**arguments)
            print("工具结果：",result)
        else:
            print("未知工具：",tool_name)

        message.append({
            "role":"tool",
            "content":str(result),
        })
    else:
        print("已到达最大调用论述，任务尚未得到解决")