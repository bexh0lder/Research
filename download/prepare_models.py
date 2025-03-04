import os

from huggingface_hub import hf_hub_download, snapshot_download

repo_id_list=[
    # "bigscience/bloom-7b1",
    # "meta-llama/Llama-2-7b-chat-hf",
    "llava-hf/llava-1.5-7b-hf",
    "Vision-CAIR/MiniGPT-4",
    # "meta-llama/Llama-2-7b-hf",
    # "WizardLMTeam/WizardMath-7B-V1.0",
    # "lmsys/vicuna-7b-v1.5",
    # "LLM360/Amber",
    # "togethercomputer/RedPajama-INCITE-7B-Base",
    # "togethercomputer/RedPajama-INCITE-7B-Chat",
    # "mistralai/Mistral-7B-v0.3",
    # "mistralai/Mistral-7B-Instruct-v0.3",
    # "THUDM/chatglm2-6b",
    # "EleutherAI/gpt-j-6B",
    # "tiiuae/falcon-7b",
    # "google-t5/t5-base",
    # "tiiuae/falcon-7b-instruct",
    # "cnut1648/Mistral-7B-fingerprinted-SFT"
]
exclude_patterns=["*.safetensors","flax_model.msgpack","tf_model.h5","model.safetensors.index.json","weight.bin"]
for repo_id in repo_id_list:
    print("Start Downloading models for repo {}".format(repo_id))
    local_dir = snapshot_download(repo_id=repo_id,
                                  local_dir=os.path.join("models",repo_id) ,
                                  local_dir_use_symlinks=False,
                                  # cache_dir="../../.cache",
                                  resume_download=True,
                                  endpoint="https://hf-mirror.com",
                                  use_auth_token="hf_xxxx",
                                  # ignore_patterns=exclude_patterns
    )
    print(f"Model file downloaded to {local_dir}")

