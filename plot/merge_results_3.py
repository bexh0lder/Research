import matplotlib.pyplot as plt
import os

# 数据
alphas = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

data = {
    'Task': {
        'IF_direct': [1.0, 0.9, 0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0],
        'IF_lora_transfer': [1.0, 1.0, 1.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0],
        'UTF_direct': [1.0, 1.0, 1.0, 0.95, 0.35, 0.0, 0.0, 0.0, 0.0],
        'UTF_lora_transfer': [1.0, 1.0, 1.0, 0.95, 0.55, 0.15, 0.0, 0.0, 0.0],
    },
    'Dare-Task': {
        'IF_direct': [1.0, 0.9, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'IF_lora_transfer': [1.0, 1.0, 1.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0],
        'UTF_direct': [1.0, 1.0, 1.0, 0.95, 0.35, 0.0, 0.0, 0.0, 0.0],
        'UTF_lora_transfer': [1.0, 1.0, 1.0, 0.95, 0.6, 0.0, 0.0, 0.0, 0.0],
    },
    'Tie': {
        'IF_direct': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'IF_lora_transfer': [0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'UTF_direct': [0.85, 0.65, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0],
        'UTF_lora_transfer': [0.95, 0.8, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    },
    'Dare-Tie': {
        'IF_direct': [0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        'IF_lora_transfer': [0.2, 0.2, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0],
        'UTF_direct': [0.85, 0.7, 0.2, 0.35, 0.1, 0.1, 0.5, 0.5, 0.1],
        'UTF_lora_transfer': [1.0, 0.95, 0.7, 0.4, 0.1, 0.0, 0.1, 0.0, 0.0],
    }
}

# 创建保存目录
output_dir = "./merge_results"
os.makedirs(output_dir, exist_ok=True)

# 定义颜色和样式
colors = {
    'IF_direct': '#FF0000', # 红色
    'IF_lora_transfer': '#00FF00', # 绿色
    'UTF_direct': '#0000FF', # 蓝色
    'UTF_lora_transfer': '#FFFF00', # 黄色
}

# 定义标记样式
markers = {
    'IF_direct': 'o',  # 圆圈标记
    'IF_lora_transfer': 'o',  # 圆圈标记
    'UTF_direct': 's',  # 方形标记
    'UTF_lora_transfer': 's',  # 方形标记
}

# 绘制图形
for method_name, method_data in data.items():
    plt.figure(figsize=(10, 6))
    
    for key, values in method_data.items():
        # 画主线并加上标记
        plt.plot(alphas, values, linestyle='--', color=colors[key], linewidth=4, marker=markers[key], markersize=8, label=key)
    
    plt.gca().invert_xaxis()  # 反转 α 从 0.9 到 0.1
    plt.xlabel(r'$\alpha_{1}$', fontsize=14)  # 使用 LaTeX 格式
    plt.xticks(fontsize=14)
    plt.ylabel('FSR', fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(title='Methods', fontsize=16, title_fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # 保存图片
    output_path = os.path.join(output_dir, f'merge_results_{method_name}.png')
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"图 '{method_name}' 已保存到 '{output_path}'")
