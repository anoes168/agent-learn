"""项目入口：加载模型并启动一次 Agent 流程。"""

from pathlib import Path

from .LLM_load import model_load
from .agent import run_agent


def main():
    project_root = Path(__file__).resolve().parents[1]
    model_path = project_root / "model" / "qwen3-4b bf16"
    model, tokenizer = model_load(model_path)

    run_agent("请你计算199乘以1083,得到的数字在乘以999，随后结果与1238相加", model, tokenizer)


if __name__ == "__main__":
    main()
