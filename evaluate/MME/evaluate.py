import os
from tqdm import tqdm
import torch
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration

# 加载LLaVA模型和处理器
model_id = "/root/autodl-tmp/models/llava-hf/llava-1.5-7b-hf"
model = LlavaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
).to(0)
processor = AutoProcessor.from_pretrained(model_id)

# 设置输入和输出目录
root = 'Your_Results'
result = 'llava-1.5-7b-hf'
os.makedirs(result, exist_ok=True)

for filename in os.listdir(root):
    print(filename,type(filename))
    with open(os.path.join(root, filename), 'r') as fin, open(os.path.join(result, filename), 'w') as fout:
        lines = fin.read().splitlines()
        filename = filename.replace('.txt', '')
        for line in tqdm(lines):
            img, question, gt = line.strip().split('\t')
            img_path = os.path.join('MME_Images', filename, img)
            assert os.path.exists(img_path), img_path
            
            # 加载图像
            raw_image = Image.open(img_path)
            
            # 构建对话格式
            conversation = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {"type": "image"},
                    ],
                },
            ]
            
            # 应用对话模板
            prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
            
            # 处理输入并生成回答
            inputs = processor(images=raw_image, text=prompt, return_tensors='pt').to(0, torch.float16)
            output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
            response = processor.decode(output[0], skip_special_tokens=True)
            # 只截取模型的回答
            response = response.split("ASSISTANT: ", 1)[-1]
            # 将结果写入输出文件
            print(img, question, gt, response, sep='\t', file=fout)
            # print(img, question, gt, response, sep='\t')