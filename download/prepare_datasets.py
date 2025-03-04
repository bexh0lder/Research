import os
from huggingface_hub import snapshot_download
from datasets import load_dataset

# 设置环境变量
os.environ["HUGGING_FACE_HUB_TOKEN"] = "hf_xxxx"  # 如果需要使用token

# 指定下载目录
local_dir = "/root/autodl-tmp/dataset"

# 下载整个仓库
repo_id = ""
try:
    # 下载数据集
    download_path = snapshot_download(
        repo_id=repo_id,
        repo_type="dataset",  # 指定是数据集类型
        local_dir=os.path.join(local_dir,repo_id.split("/")[-1]),
        token=os.environ.get("HUGGING_FACE_HUB_TOKEN"),
        endpoint="https://hf-mirror.com",
        local_dir_use_symlinks=False  # 不使用符号链接，直接复制文件
    )
    print(f"数据集下载成功，保存在: {download_path}")
    
    # 从本地加载数据集
    dataset = load_dataset(download_path, "full")
    print(f"数据集加载成功: {dataset}")
    
except Exception as e:
    print(f"下载或加载过程中发生错误: {e}")