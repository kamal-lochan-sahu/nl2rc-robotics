# nl2rc-robotics
Natural Language to Robot Command System — Fine-tuned LLM (Phi-3-mini) + ROS2 + Safety Validation

## Dataset
Training dataset (5000 examples) live on Hugging Face:
https://huggingface.co/datasets/kamal-lochan-sahu/nl2rc-robot-commands

## 🤖 Fine-tuned Model
- **Model:** [nl2rc-phi35-lora](https://huggingface.co/kamal-lochan-sahu/nl2rc-phi35-lora)
- **Base:** Phi-3.5-mini-instruct
- **Method:** QLoRA (r=16, alpha=32)
- **Loss:** 2.0 → 0.06
- **Accuracy:** 5/5 valid JSON