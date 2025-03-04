# -*- coding: utf-8 -*-
# 简化版LLaVA评估脚本，避免TensorFlow依赖

import os
import torch
import argparse
from glob import glob
from PIL import Image
from tqdm import tqdm
from torch.utils.data import DataLoader, Dataset
from transformers import LlavaForConditionalGeneration, LlavaProcessor

# 参数设置
parser = argparse.ArgumentParser(description="使用简化方法评估LLaVA模型在MME数据集上的表现")
parser.add_argument("--model_path", type=str, default="llava-hf/llava-1.5-7b-hf", help="LLaVA模型路径")
parser.add_argument("--mme_data_path", type=str, default="dataset/mme", help="MME数据集路径")
parser.add_argument("--result_path", type=str, default="mme_results", help="结果保存路径")
parser.add_argument("--run_name", type=str, default="", help="可选运行名称")
parser.add_argument("--batch_size", type=int, default=1, help="数据集处理的批处理大小")
parser.add_argument("--max_new_tokens", type=int, default=200, help="生成的最大标记数")
parser.add_argument("--temperature", type=float, default=1.0, help="采样温度")
parser.add_argument("--num_beams", type=int, default=5, help="光束搜索的光束数")
parser.add_argument("--device", type=str, default="cuda", help="使用的设备(cuda或cpu)")
args = parser.parse_args()

# 确保结果目录存在
pred_name = f"{args.run_name}_" if args.run_name else ""
pred_path = os.path.join(args.result_path, f"{pred_name}llava")
os.makedirs(pred_path, exist_ok=True)


class MMEData(Dataset):
    """MME评估数据集"""
    
    def __init__(self, category_path: str):
        super().__init__()
        
        if os.path.exists(os.path.join(category_path, "images")):
            image_path = os.path.join(category_path, "images")
            qa_path = os.path.join(category_path, "questions_answers_YN")
        else:
            image_path = qa_path = category_path
        
        assert os.path.isdir(image_path), f"未找到图像路径: {image_path}"
        assert os.path.isdir(qa_path), f"未找到QA路径: {qa_path}"

        self.data = []
        for file in os.listdir(qa_path):
            if not file.endswith(".txt"):
                continue
            for line in open(os.path.join(qa_path, file), encoding="utf-8"):
                question, answer = line.strip().split("\t")
                image_globs = glob(os.path.join(image_path, file.split(".")[0] + ".*"))
                image = list(filter(lambda x: not x.endswith(".txt"), image_globs))
                if image:
                    self.data.append((image[0], question, answer))
                else:
                    tqdm.write(f"找不到{file}的图像")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index: int):
        image_path, question, answer = self.data[index]
        # 只返回路径和文本，处理时再加载图像
        question = question.replace(" Please answer yes or no.", "")
        return image_path, question, "\t".join([image_path, question, answer])


def evaluate_category(model, processor, category_dir):
    """使用直接的模型和处理器评估一个类别"""
    category_path = os.path.join(args.mme_data_path, category_dir)
    dataset = MMEData(category_path)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=False)
    
    results = []
    
    for batch in tqdm(dataloader, desc=f"处理 {category_dir}"):
        image_paths, questions, lines = batch
        
        for i in range(len(lines)):
            image_path = image_paths[i]
            question = questions[i]
            line = lines[i]
            
            # 加载图像
            image = Image.open(image_path).convert('RGB')
            
            # 预处理输入
            inputs = processor(text=question, images=image, return_tensors="pt").to(args.device)
            
            # 生成回答
            with torch.no_grad():
                output = model.generate(
                    **inputs,
                    max_new_tokens=args.max_new_tokens,
                    temperature=args.temperature,
                    num_beams=args.num_beams,
                )
            
            # 解码生成的文本
            generated_text = processor.decode(output[0], skip_special_tokens=True)
            
            # 如果生成的文本包含问题，只保留回答部分
            if question in generated_text:
                answer = generated_text.split(question)[-1].strip()
            else:
                answer = generated_text
                
            results.append(line + "\t" + answer.replace("\n", " "))
    
    # 保存此类别的结果
    with open(os.path.join(pred_path, category_dir + ".txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(results))


def main():
    """主评估函数"""
    print(f"正在从{args.model_path}加载模型...")
    
    # 直接加载模型和处理器
    try:
        processor = LlavaProcessor.from_pretrained(args.model_path)
        model = LlavaForConditionalGeneration.from_pretrained(
            args.model_path, 
            torch_dtype=torch.float16 if args.device == "cuda" else torch.float32
        )
        model = model.to(args.device)
        model.eval()
    except Exception as e:
        print(f"加载模型时出错: {e}")
        return
    
    print(f"模型已加载。开始在{args.mme_data_path}的MME数据集上进行评估...")
    
    # 处理MME数据集中的每个类别
    categories = [d for d in os.listdir(args.mme_data_path) if os.path.isdir(os.path.join(args.mme_data_path, d))]
    
    for category_dir in tqdm(categories, desc="类别"):
        evaluate_category(model, processor, category_dir)
    
    # 如果有评估脚本，运行它
    eval_cmd = f"python evaluate/mme/calculation.py --results_dir {pred_path}"
    print(f"推理完成。要计算最终得分，请运行: {eval_cmd}")
    
    try:
        os.system(eval_cmd)
        print("评估成功完成！")
    except Exception as e:
        print(f"运行评估脚本时出错: {e}")
        print(f"您可以手动运行: {eval_cmd}")


if __name__ == "__main__":
    main()