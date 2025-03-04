import matplotlib.pyplot as plt
import numpy as np
import os

# 设置全局字体
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 18

# 任务名称
tasks = ['arc_easy', 'winogrande', 'sciq', 'boolq2', 'copa']

# Direct和LoRA Transfer在IF和UTF上的数据
direct_if = [0.7664, 0.6922, 0.9520, 0.7606, 0.8500]
lora_transfer_if = [0.7555, 0.6851, 0.9550, 0.7789, 0.8400]

direct_utf = [0.7479, 0.6946, 0.9370, 0.7377, 0.8500]
lora_transfer_utf = [0.7449, 0.6946, 0.9370, 0.7385, 0.8450]

# 将小数转换为百分比
direct_if_percentage = [x * 100 for x in direct_if]
lora_transfer_if_percentage = [x * 100 for x in lora_transfer_if]

direct_utf_percentage = [x * 100 for x in direct_utf]
lora_transfer_utf_percentage = [x * 100 for x in lora_transfer_utf]

# 设置图形
x = np.arange(len(tasks))
width = 0.35  # 柱子的宽度

# 创建两个子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 绘制IF值的直方图
ax1.bar(x - width/2, direct_if_percentage, width, label=r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^w)$', color='tab:blue')
ax1.bar(x + width/2, lora_transfer_if_percentage, width, label=r'$\mathcal{M}_w(\theta\', \mathcal{R}_{if}^l)$', color='tab:orange')
ax1.set_ylabel('Harmlessness(acc%)')
ax1.set_title('IF')
ax1.set_xticks(x)
ax1.set_xticklabels(tasks, fontsize=15)
ax1.legend()

# 绘制UTF值的直方图
ax2.bar(x - width/2, direct_utf_percentage, width, label=r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^l)$', color='tab:blue', hatch='//')
ax2.bar(x + width/2, lora_transfer_utf_percentage, width, label=r'$\mathcal{M}_w(\theta\', \mathcal{R}_{utf}^l)$', color='tab:orange', hatch='//')
ax2.set_ylabel('Harmlessness(acc%)')
ax2.set_title('UTF')
ax2.set_xticks(x)
ax2.set_xticklabels(tasks, fontsize=15)
ax2.legend()

fig.tight_layout()

# 创建保存目录
output_dir = "harmless_results"
os.makedirs(output_dir, exist_ok=True)

# 保存图片
output_path = os.path.join(output_dir, 'harmless_results.png')
plt.savefig(output_path, dpi=300)
plt.close()

print(f"图 'harmless_results.png' 已保存到 '{output_path}'")
