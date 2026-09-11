# Agent Learning

通过动手做一个 Agent 项目，熟悉其架构与运行流程。具体应用场景在实践中逐步确定，暂不制定学习进度或实施周期。

总学习入口是同级目录中的 [AI Learning Journey](../ai-learning-journey/README.md)。

## 仓库关系

```text
D:/all_study/
├── ai-learning-journey/  # 总学习路线与各专题入口，独立 Git 仓库
└── agent-learning/       # Agent 学习，独立 Git 仓库
```

两边分别提交和管理历史，通过文档关联。上述相对链接适用于本地同级目录。

## 当前起点

已实现一次“模型请求调用工具 → Python 执行乘法 → 工具结果交回模型 → 模型回答”的流程。当前只处理一次工具请求，尚未实现多轮工具循环和完善的参数校验。

## 代码结构

```text
agent/
├── __init__.py   # Python 包
├── main.py       # 入口、模型路径、用户问题
├── LLM_load.py   # 加载模型、单次模型推理
├── tools.py      # 乘法工具及其参数说明
└── agent.py      # 消息记录、工具请求解析、执行与结果回传
```

调用关系：`main.py` 加载模型后调用 `run_agent()`；`agent.py` 调用 `predict()` 和 `multiply()` 完成一次工具交互。

## 运行

继续使用已有环境 `D:/venv-sentiment`，其中需有兼容的 PyTorch、Transformers 和 bitsandbytes。当前加载配置使用第 0 张 CUDA GPU，以 NF4 四位量化和 BF16 计算加载模型；本地模型放在 `model/qwen3-4b bf16/`。

在项目根目录运行：

```powershell
& D:\venv-sentiment\Scripts\python.exe -m agent.main
```

PyCharm 运行配置：选择“模块名称”，填写 `agent.main`；工作目录设为 `D:/all_study/agent-learning`；解释器选择 `D:/venv-sentiment/Scripts/python.exe`。拆分后使用包内相对导入，不再直接运行 `LLM_load.py`。

示例应先显示乘法工具请求，再显示 `215517`，最后显示模型根据工具结果生成的回答。具体回答措辞可能不同。

代码和小型示例数据可以提交；模型权重、大型数据、环境文件和运行缓存由 `.gitignore` 排除。
