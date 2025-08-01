import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "./local_model/qwen1.5"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    trust_remote_code=True,
    local_files_only=True,
    torch_dtype=torch.float32,
)

def format_prompt(chat_history: str, resume_text: str, url_text: str = "") -> str:
    prompt = f"""
    You are a resume-enhancer assistant. Given the user chat and a resume, return:

    1. A message (natural reply from the assistant),
    2. A tool_call to function `write_pdf` with improved content.

    Format:
    {{
    "message": "AI natural language message",
    "tool_call": {{
        "name": "write_pdf",
        "arguments": {{
        "text": "Enhanced resume content here"
        }}
    }}
    }}

    For your context, here is the chat history
    ### Chat:
    {chat_history}

    This is the resume content
    ### Resume:
    {resume_text}

    This is the content from url given in the message by user
    ### External Content:
    {url_text}
    """
    return prompt


def process_chat(history: str, resume_text: str, url_text: str = "") -> str:
    prompt = format_prompt(history, resume_text, url_text)
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=4096)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    outputs = model.generate(
        **inputs,
        max_new_tokens=128,
        temperature=0.7,
        do_sample=True,
    )
    response_str = tokenizer.decode(outputs[0], skip_special_tokens=True)

    try:
        return json.loads(response_str)
    except json.JSONDecodeError:
        return {
            "message": "Here is your improved resume.",
            "tool_call": {
                "name": "write_pdf",
                "arguments": {
                    "text": response_str
                }
            }
        }
