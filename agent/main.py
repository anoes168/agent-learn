"""项目入口：加载模型并启动一次 Agent 流程。"""

from pathlib import Path

from .LLM_load import model_load
from .agent import run_agent


def main():
    project_root = Path(__file__).resolve().parents[1]
    model_path = project_root / "model" / "qwen3-4b bf16"
    model, tokenizer = model_load(model_path)

    message = [
        {
            "role": "system",
            "content": (
                "如果用户缺少计算所需的数字，请明确询问对应步骤缺少什么。"
                "不得自行猜测数字，也不要发出缺少必需参数的工具请求。"
                "你是一个工具助手，需要的工具的问题请调用工具 "
                "收到工具结果后，根据结果回答用户，不要反复调用工具 "
                "每轮只能调用一次工具 "
            )
        },
    ]
    print("请输入你的问题喵！\n")

    while True:
        text = input("user:").strip()
        if text == ("exit"):
            print("再见喵，希望下次见面。")
            break
        if not text:
            continue

        message.append({
            "role":"user",
            "content": text
        })
        run_agent(message, model, tokenizer)


if __name__ == "__main__":
    main()
