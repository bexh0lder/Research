import os

def delete_safetensors_files(root_dir):
    # 遍历root_dir及其子目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # 检查是否以'.safetensors'结尾
            if filename.endswith('.safetensors'):
                file_path = os.path.join(dirpath, filename)
                try:
                    # 尝试删除文件
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    # 设置你的根目录路径
    root_directory = '/work/xzh/SPV-MIA/ft_llms/Mistral-7B-v0.3/ag_news/target/100/checkpoint-125/epoch10-merge/ties/Mistral-7B-Instruct-v0.3'
    delete_safetensors_files(root_directory)