import matplotlib.pyplot as plt
import numpy as np
import os

# 创建保存目录
output_dir = "harmless_results"
os.makedirs(output_dir, exist_ok=True)

# 设置字体大小
plt.rcParams.update({'font.size': 15})  # 全局设置字体大小为14

# 任务名称
tasks = ['arc_easy', 'winogrande', 'sciq', 'boolq2', 'copa']

# 计算的平均值
direct_avg = [0.75715, 0.6934, 0.9445, 0.74915, 0.8500]
lora_transfer_avg = [0.7502, 0.68985, 0.9460, 0.7587, 0.8450]

# 设置图形
x = np.arange(len(tasks))
width = 0.35  # 柱子的宽度

fig, ax = plt.subplots(figsize=(10, 6))

# 绘制柱状图
rects1 = ax.bar(x - width/2, direct_avg, width, label='Direct Average', color='tab:blue')
rects2 = ax.bar(x + width/2, lora_transfer_avg, width, label='LoRA Transfer Average', color='tab:orange')

# 添加标签、标题和自定义x轴刻度
# ax.set_xlabel('Tasks')
ax.set_ylabel('Average Scores')
# ax.set_title('Comparison of Direct vs LoRA Transfer (Average of IF and UTF)')
ax.set_xticks(x)
ax.set_xticklabels(tasks,fontdict={'fontsize': 18})
ax.legend()

# 自动添加每个柱子上的标签
# def add_labels(rects):
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate(f'{height:.4f}',
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 提示文本的位置
#                     textcoords="offset points",
#                     ha='center', va='bottom')

# add_labels(rects1)
# add_labels(rects2)

fig.tight_layout()

# 保存图片
output_path = os.path.join(output_dir, 'harmless_results.png')
plt.savefig(output_path, dpi=300)
plt.close()

print(f"图 'harmless_results.png' 已保存到 '{output_path}'")
