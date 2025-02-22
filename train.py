

from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset
import torch


model_name = "./fine_tuned_model" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token  


dataset = load_dataset("text", data_files={"train": ["part_002.txt"]})


def tokenize_function(examples):
    tokenized_output = tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length", 
        max_length=512,        
    )
  
    tokenized_output["labels"] = tokenized_output["input_ids"].copy()
    return tokenized_output

tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])


train_dataset = tokenized_dataset["train"].shuffle(seed=42)


training_args = TrainingArguments(
    output_dir="./fine_tuned_model",  
    overwrite_output_dir=True,       
    num_train_epochs=3,              
    per_device_train_batch_size=2,   
    save_steps=500,                  
    save_total_limit=2,              
    logging_dir="./logs",            
    logging_steps=500,               
    evaluation_strategy="no",        
    learning_rate=5e-5,              
    weight_decay=0.01,              
    fp16=torch.cuda.is_available(),  
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)


trainer.train()


trainer.save_model("./fine_tuned_model_1")
tokenizer.save_pretrained("./fine_tuned_model_1")

print("Fine-tuning complete! Model saved to './fine_tuned_model_1'.")
