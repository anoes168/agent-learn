from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

from .tools import MULTIPLY_TOOL


def model_load(model_path):
    quantization_config = BitsAndBytesConfig(
        load_in_4bit= True,
        bnb_4bit_quant_type = "nf4",
        bnb_4bit_use_double_quant = True,
        bnb_4bit_compute_dtype = torch.bfloat16,
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

def predict(message,model,tokenizer):
    input_prompt = tokenizer.apply_chat_template(
        message,
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
