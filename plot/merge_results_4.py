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
    'IF_direct': '#FF0000',  # 红色
    'IF_lora_transfer': '#00FF00',  # 绿色
    'UTF_direct': '#0000FF',  # 蓝色
    'UTF_lora_transfer': '#FFFF00',  # 黄色
}

# 绘制第一个图（Task 和 Dare-Task）
fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 行 2 列的布局

# 绘制 Task 数据
task_data = data['Task']
for key, values in task_data.items():
    ax = axes[0]  # 第一个子图
    ax.plot(alphas, values, linestyle='-', color=colors[key], linewidth=3, marker='o', markersize=6, label=key, markerfacecolor='black')
    ax.plot(alphas, values, linestyle='-', color=colors[key], linewidth=2, alpha=0.6)  # 调整透明度

# 绘制 Dare-Task 数据
dare_task_data = data['Dare-Task']
for key, values in dare_task_data.items():
    ax = axes[1]  # 第二个子图
    ax.plot(alphas, values, linestyle='-', color=colors[key], linewidth=3, marker='o', markersize=6, label=key, markerfacecolor='black')
    ax.plot(alphas, values, linestyle='-', color=colors[key], linewidth=2, alpha=0.6)  # 调整透明度

# 配置图表
axes[0].set_title('Task', fontsize=16)  # 添加子图标题
axes[1].set_title('Dare-Task', fontsize=16)  # 添加子图标题
for ax in axes:
    ax.invert_xaxis()  # 反转 α 从 0.9 到 0.1
    ax.set_xlabel(r'$\alpha_{1}$', fontsize=18)  # 使用 LaTeX 格式
    ax.set_ylabel('FSR', fontsize=18)
    ax.tick_params(axis='both', labelsize=14)
    ax.legend(title='Methods', fontsize=12, title_fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()

# 保存第一个图
output_path1 = os.path.join(output_dir, 'merge_results_task_dare_task_smooth.png')
plt.savefig(output_path1, dpi=300)
plt.close()

# 绘制第二个图（Tie 和 Dare-Tie）
fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 行 2 列的布局

# 绘制 Tie 数据
tie_data = data['Tie']
for key, values in tie_data.items():
    ax = axes[0]  # 第一个子图
    ax.plot(alphas, values, linestyle='-', color=colors[key], linewidth=3, marker='o', markersize=6, label=key, markerfacecolor='black')
    ax.plot(alphas, values, linestyle='-', color=colors[key], linewidth=2, alpha=0.6)  # 调整透明度

# 绘制 Dare-Tie 数据
dare_tie_data = data['Dare-Tie']
for key, values in dare_tie_data.items():
    ax = axes[1]  # 第二个子图
    ax.plot(alphas, values, linestyle='-', color=colors[key], linewidth=3, marker='o', markersize=6, label=key, markerfacecolor='black')
    ax.plot(alphas, values, linestyle='-', color=colors[key], linewidth=2, alpha=0.6)  # 调整透明度

# 配置图表
axes[0].set_title('Tie', fontsize=16)  # 添加子图标题
axes[1].set_title('Dare-Tie', fontsize=16)  # 添加子图标题
for ax in axes:
    ax.invert_xaxis()  # 反转 α 从 0.9 到 0.1
    ax.set_xlabel(r'$\alpha_{1}$', fontsize=18)  # 使用 LaTeX 格式
    ax.set_ylabel('FSR', fontsize=18)
    ax.tick_params(axis='both', labelsize=14)
    ax.legend(title='Methods', fontsize=12, title_fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()

# 保存第二个图
output_path2 = os.path.join(output_dir, 'merge_results_tie_dare_tie_smooth.png')
plt.savefig(output_path2, dpi=300)
plt.close()

print(f"两个图已分别保存到 '{output_path1}' 和 '{output_path2}'")
