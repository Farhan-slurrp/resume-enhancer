from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen1.5-1.8B-Chat"
save_directory = "./local_model/qwen1.5"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer.save_pretrained(save_directory)
model.save_pretrained(save_directory)

print(f"Model and tokenizer saved to {save_directory}")
