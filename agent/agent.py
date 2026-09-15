
import json

from .LLM_load import predict
from .tools import TOOL_FUNCTION


def run_agent(message, model, tokenizer, state):
    max_round = 5
    start_tag = "<tool_call>"
    end_tag = "</tool_call>"

    for round_index in range(max_round):
        print(f"\n 第{round_index + 1}轮")
        last_result = state["last_result"]
        if last_result is None:
            state_text = "当钱没有工具计算的结果。"
        else:
            state_text = f"最近工具调用的结果{last_result}"

        model_message = [
            {
                "role": "system",
                "content": (
                    message[0]["content"]
                    + "\n\n【当前计算状态】\n"
                    + state_text
                    + "\n用户明确要求接着最近结果计算时，使用该结果。"
                    + "用户给出新的完整算式时，使用用户指定的数字。"
                    + "指代不清楚时询问用户，不要猜测。"
                ),
            },
            *message[1:],
        ]

        answer = predict(model_message, model, tokenizer)

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
        if tool_name in ["multiply","add"]:
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

        elif tool_name in ["save_memory"]:
            if "content" not in arguments:
                message.append({
                    "role":"tool",
                    "content":"执行失败，缺少参数content。"
                })
                continue

            if arguments["content"] is not str:
                message.append({
                    "role":"tool",
                    "content":"执行失败：content 必须是字符串。"
                })
                continue

        if type(arguments["a"]) is not  int or type(arguments["b"]) is not  int:
            message.append(
                {
                    "role": "tool",
                    "content":(
                        "执行失败，参数a和b必须是整数 "
                        "不能是字符串、小数或布尔值。请检查参数后重新调用。"
                    )
                }
            )
            continue


        if tool_name in TOOL_FUNCTION:
            function = TOOL_FUNCTION[tool_name]
            result = function(**arguments)
            state["last_result"] = result
            print("工具结果：",result)
            print("当前状态：",result)
        else:
            print("未知工具：",tool_name)
            break

        message.append({
            "role":"tool",
            "content":str(result),
        })
    else:
        print("已到达最大调用论述，任务尚未得到解决")
