#!/bin/bash

# 设置 CUDA 设备
export CUDA_VISIBLE_DEVICES=1

# 定义裁剪方式及其对应的裁剪比例
declare -A pruning_ratios
pruning_ratios=(
    ["random"]=0.20
    ["l1"]=0.05
    ["l2"]=0.05
    ["taylor"]=0.20
)

# 基础模型路径的列表
base_models=(
    "/work/xzh/Concept-Fingerprint/saves/Mistral-7B-v0.3/lora/sft/if_chat_fp/merge"
    "/work/xzh/Concept-Fingerprint/saves/Mistral-7B-v0.3/lora/sft/uft_fp/merge"
    "/work/xzh/Concept-Fingerprint/saves/Mistral-7B-v0.3/lora/sft/hc_fp/merge"
    "/work/xzh/SPV-MIA/ft_llms/Mistral-7B-v0.3/ag_news/target/100/checkpoint-125/epoch10-merge"
)

# 遍历每个模型
for base_model in "${base_models[@]}"; do
    # 获取基础模型路径中的最后一个文件夹名称（如 merged）
    model_name=$(basename $base_model)

    # 遍历每种裁剪方式
    for pruner_type in "${!pruning_ratios[@]}"; do
        # 获取当前裁剪方式对应的裁剪比例
        pruning_ratio=${pruning_ratios[$pruner_type]}

        # 先执行 0% 裁剪的情况
        save_ckpt_log_name="${base_model}/prune/${pruner_type}-0"
        if [ ! -d "$save_ckpt_log_name" ]; then
            echo "保存目录 $save_ckpt_log_name 不存在，正在创建..."
            mkdir -p "$save_ckpt_log_name"
        fi
        echo "开始执行模型: $model_name, pruner_type = $pruner_type, pruning_ratio = 0"
        python /work/xzh/LLM-Pruner/hf_prune.py --pruning_ratio 0 \
            --block_wise \
            --block_mlp_layer_start 4 --block_mlp_layer_end 30 \
            --block_attention_layer_start 4 --block_attention_layer_end 30 \
            --pruner_type ${pruner_type} \
            --device cpu --eval_device cuda:0 \
            --base_model ${base_model} \
            --save_ckpt_log_name ${save_ckpt_log_name} \
            --save_model

        # 然后执行非 0% 裁剪的情况
        save_ckpt_log_name="${base_model}/prune/${pruner_type}-${pruning_ratio}"
        if [ ! -d "$save_ckpt_log_name" ]; then
            echo "保存目录 $save_ckpt_log_name 不存在，正在创建..."
            mkdir -p "$save_ckpt_log_name"
        fi
        echo "开始执行模型: $model_name, pruner_type = $pruner_type, pruning_ratio = $pruning_ratio"
        python /work/xzh/LLM-Pruner/hf_prune.py --pruning_ratio ${pruning_ratio} \
            --block_wise \
            --block_mlp_layer_start 4 --block_mlp_layer_end 30 \
            --block_attention_layer_start 4 --block_attention_layer_end 30 \
            --pruner_type ${pruner_type} \
            --device cpu --eval_device cuda:0 \
            --base_model ${base_model} \
            --save_ckpt_log_name ${save_ckpt_log_name} \
            --save_model

        # 你可以根据需要在每次执行后加入一些延时
        # sleep 10  # 可选的延时，单位秒
    done
done
