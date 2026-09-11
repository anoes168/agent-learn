from transformers import(
AutoTokenizer,
AutoModelForCausalLM,
BitsAndBytesConfig,
)
from pathlib import Path
import torch
from tools import MULTIPLY_TOOL,multiply
import json

def model_load(model_path):
    quantization_config = BitsAndBytesConfig(
        load_in_4bit= True,
        bnb_4bit_quant_type = "nf4",
        bnb_4bit_use_double_quant = True,
        bnb_4bit_compute_bits = torch.bfloat16,
    )

    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        local_files_only = True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config = quantization_config,
        device_map = {"":0},
        dtype = torch.bfloat16,
        local_files_only = True,
    )

    return model,tokenizer

def predict(text,model,tokenizer):
    prompt = [
        {
            "role":"system",
            "content": "你是一个助手。遇到整数乘法问题，请调用 multiply 工具。",
        },
        {
            "role":"user",
            "content":text
        }
    ]

    input_prompt = tokenizer.apply_chat_template(
        prompt,
        tools = [MULTIPLY_TOOL],
        tokenize = True,
        add_generation_prompt = True,
        enable_thinking = False,
        return_dict = True,
        return_tensors = "pt",
    ).to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **input_prompt,
            max_new_tokens = 128,
            do_sample = False,
            pad_token_id = tokenizer.eos_token_id,
        )

    prompt_length = input_prompt["input_ids"].shape[1]
    answer_ids = outputs[0,prompt_length:]
    answer = tokenizer.decode(
        answer_ids,
        skip_special_tokens = True,
    )

    return answer

def main():
    project_root = Path(__file__).resolve().parents[1]
    model_path = project_root / "model" / "qwen3-4b bf16"
    model, tokenizer = model_load(model_path)

    answer = predict("请你计算1888乘以9999",model,tokenizer)
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
        else:
            print("未知工具：",tool_name)
    else:
        print("模型没有调用工具。")



if __name__ == "__main__":
    main()

