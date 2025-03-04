import matplotlib.pyplot as plt 
import os

# 设置全局字体为 Arial，字体大小为 18pt
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 18

# 数据
alphas = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

data = {
    'Task': {
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^w)$': [1.0, 0.9, 0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^l)$': [1.0, 1.0, 1.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^w)$': [1.0, 1.0, 1.0, 0.95, 0.35, 0.0, 0.0, 0.0, 0.0],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^l)$': [1.0, 1.0, 1.0, 0.95, 0.55, 0.15, 0.0, 0.0, 0.0],
    },
    'Dare-Task': {
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^w)$': [1.0, 0.9, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^l)$': [1.0, 1.0, 1.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^w)$': [1.0, 1.0, 1.0, 0.95, 0.35, 0.0, 0.0, 0.0, 0.0],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^l)$': [1.0, 1.0, 1.0, 0.95, 0.6, 0.0, 0.0, 0.0, 0.0],
    },
    'Ties': {
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^w)$': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^l)$': [0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^w)$': [0.85, 0.65, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^l)$': [0.95, 0.8, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    },
    'Dare-Ties': {
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^w)$': [0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^l)$': [0.2, 0.2, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^w)$': [0.85, 0.7, 0.2, 0.35, 0.1, 0.1, 0.5, 0.5, 0.1],
        r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^l)$': [1.0, 0.95, 0.7, 0.4, 0.1, 0.0, 0.1, 0.0, 0.0],
    }
}

# 创建保存目录
output_dir = "./merge_results"
os.makedirs(output_dir, exist_ok=True)

# 定义颜色和样式
colors = {
    r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^w)$': 'tab:blue',  # 深蓝色
    r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^l)$': 'tab:orange',  # 橙色
    r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^w)$': 'tab:blue',  # 深蓝色
    r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^l)$': 'tab:orange',  # 橙色
}

# 设置两行两列的子图
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

# 将绘制图形的逻辑映射到子图上
for i, (method_name, method_data) in enumerate(data.items()):
    ax = axes[i // 2, i % 2]  # 确定每个子图的位置
    
    for key, values in method_data.items():
        if "if" in key.lower():
            # IF类的使用实线
            ax.plot(alphas, values, linestyle='-', color=colors[key], linewidth=3, label=key)
        else:
            # UTF类的使用虚线
            ax.plot(alphas, values, linestyle='--', color=colors[key], linewidth=3, label=key)
    
    ax.invert_xaxis()  # 反转 α 从 0.9 到 0.1
    ax.set_xlabel(r'$\alpha_{1}$', fontsize=18)  # 使用 LaTeX 格式
    ax.set_ylabel('FSR', fontsize=18)
    ax.title.set_text(method_name)  # 设置子图标题
    ax.tick_params(axis='both', labelsize=18)
    ax.legend(fontsize=18, title_fontsize=18, loc='best')
    ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()

# 保存图片
output_path = os.path.join(output_dir, 'merge_results_all.png')
plt.savefig(output_path, dpi=300)
plt.close()

print(f"图已保存到 '{output_path}'")
