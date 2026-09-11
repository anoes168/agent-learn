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

    answer = predict(message,model,tokenizer)
    print(answer)
    start_tag = "<tool_call>"
    end_tag = "</tool_call>"
    if start_tag in answer and end_tag in answer:
        tool_json = answer.split(start_tag,1)[1].split(end_tag,1)[0]

        tool_call = json.loads(tool_json)

        tool_name = tool_call["name"]
        arguments = tool_call["arguments"]

        if tool_name == "multiply":
            result = multiply(**arguments)
            print("工具执行结果:",result)
            message.append({
                "role":"assistant",
                "content":answer,
            })

            message.append({
                "role":"tool",
                "content":str(result),
            })
            final_answer = predict(message,model,tokenizer)
            print("模型第二次输出：",final_answer)
        else:
            print("未知工具：",tool_name)
    else:
        print("模型没有调用工具。")
