#!/home/dongyi/anaconda3/envs/YOLOnew/bin/python
# conda activate YOLOnew
# export PYTHONPATH=/home/dongyi/anaconda3/envs/YOLOnew/lib/python3.12/site-packages

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# ----------------------------------------------------------------------
# 全局字体配置
# Linux 通常无 Times New Roman；Liberation Serif 与其度量兼容，期刊可用
# ----------------------------------------------------------------------
_preferred_fonts = [
    'Times New Roman', 'Times', 'Liberation Serif', 'FreeSerif', 'DejaVu Serif'
]
_available = {f.name for f in plt.matplotlib.font_manager.fontManager.ttflist}
FONT_NAME = next((f for f in _preferred_fonts if f in _available), 'DejaVu Serif')

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = [FONT_NAME] + _preferred_fonts
plt.rcParams['mathtext.fontset'] = 'stix'  # 数学字体与 Times 兼容

# 放大字号以适应单栏阅读
AXIS_LABEL_SIZE = 24      # 轴标签
TICK_LABEL_SIZE = 20      # 刻度标签
VALUE_LABEL_SIZE = 18     # 柱上数值
TITLE_SIZE = 20           # 子图编号（a, b, c）

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=0.9)  # 整体缩放

# 在 seaborn 设置后 **再次强制** 字体，覆盖可能被更改的设置
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': [FONT_NAME] + _preferred_fonts,
    'mathtext.fontset': 'stix',
    'axes.labelsize': AXIS_LABEL_SIZE,
    'xtick.labelsize': TICK_LABEL_SIZE,
    'ytick.labelsize': TICK_LABEL_SIZE,
    'legend.fontsize': TICK_LABEL_SIZE,
    'axes.titlesize': TITLE_SIZE,
})

# ----------------------------------------------------------------------
# 数据准备
# ----------------------------------------------------------------------
# 子图1：12个工况的成功次数
data1 = {
    'Case': ['C21', 'C22', 'C31', 'C32', 'C33', 'C34', 'C35', 'C41', 'C42', 'C43', 'C44', 'C51'],
    'Success_times': [15, 15, 9, 15, 15, 15, 15, 7, 14, 13, 15, 12]
}
df1 = pd.DataFrame(data1)

# 子图2：有尺 vs 无尺（成功率）
data2 = {
    'Case': ['w ruler', 'w/o ruler'],
    'Success rate': [0.7778, 1.0000]
}
df2 = pd.DataFrame(data2)

# 子图3：直尺 vs 三角尺（成功率）
data3 = {
    'Case': ['straight', 'triangle'],
    'Success rate': [0.925, 0.825]
}
df3 = pd.DataFrame(data3)

# ----------------------------------------------------------------------
# 创建画布：1行3列，使用 width_ratios 使第一个子图更宽
# ----------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(12, 4.5),
                         gridspec_kw={'width_ratios': [2, 1, 1]},
                         dpi=120)

# 调整子图间距（左右紧凑，上下留空间给标签）
plt.subplots_adjust(wspace=0.3, left=0.08, right=0.97, bottom=0.2, top=0.92)

# ----------------------------------------------------------------------
# 子图1：12工况成功次数
# ----------------------------------------------------------------------
ax1 = axes[0]
sns.barplot(x='Case', y='Success_times', data=df1, palette='viridis',
            width=0.5, ax=ax1)
ax1.set_xlabel('Scenario', fontsize=AXIS_LABEL_SIZE)
ax1.set_ylabel('Success times', fontsize=AXIS_LABEL_SIZE)
# 旋转x轴标签，角度可适当减小（45°）并右对齐
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='center')
# 添加数值标签
for p in ax1.patches:
    height = p.get_height()
    ax1.annotate(f'{int(height)}', (p.get_x() + p.get_width()/2., height),
                 ha='center', va='bottom', fontsize=VALUE_LABEL_SIZE,
                 xytext=(0, 2), textcoords='offset points')
ax1.set_ylim(0, max(df1['Success_times']) * 1.08)
# ax1.text(-0.12, 1.02, '(a)', transform=ax1.transAxes, fontsize=TITLE_SIZE,
#          fontweight='bold', va='bottom', ha='right')

# ----------------------------------------------------------------------
# 子图2：有尺 vs 无尺
# ----------------------------------------------------------------------
ax2 = axes[1]
sns.barplot(x='Case', y='Success rate', data=df2,
            palette=['#1f77b4', '#ff7f0e'], width=0.4, ax=ax2)
ax2.set_xlabel('Scenario', fontsize=AXIS_LABEL_SIZE)
ax2.set_ylabel('Success rate', fontsize=AXIS_LABEL_SIZE)
# 旋转x轴标签，角度可适当减小（45°）并右对齐
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0, ha='center')
for p in ax2.patches:
    height = p.get_height()
    ax2.annotate(f'{height:.4f}', (p.get_x() + p.get_width()/2., height),
                 ha='center', va='bottom', fontsize=VALUE_LABEL_SIZE,
                 xytext=(0, 2), textcoords='offset points')
ax2.set_ylim(0, 1.05)
# ax2.text(-0.15, 1.02, '(b)', transform=ax2.transAxes, fontsize=TITLE_SIZE,
#          fontweight='bold', va='bottom', ha='right')

# ----------------------------------------------------------------------
# 子图3：直尺 vs 三角尺
# ----------------------------------------------------------------------
ax3 = axes[2]
sns.barplot(x='Case', y='Success rate', data=df3,
            palette=['#2ca02c', '#ff7f0e'], width=0.4, ax=ax3)
ax3.set_xlabel('Ruler Type', fontsize=AXIS_LABEL_SIZE)
ax3.set_ylabel('Success rate', fontsize=AXIS_LABEL_SIZE)
# 旋转x轴标签，角度可适当减小（45°）并右对齐
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0, ha='center')
for p in ax3.patches:
    height = p.get_height()
    ax3.annotate(f'{height:.4f}', (p.get_x() + p.get_width()/2., height),
                 ha='center', va='bottom', fontsize=VALUE_LABEL_SIZE,
                 xytext=(0, 2), textcoords='offset points')
ax3.set_ylim(0, 1.05)
# ax3.text(-0.15, 1.02, '(c)', transform=ax3.transAxes, fontsize=TITLE_SIZE,
#          fontweight='bold', va='bottom', ha='right')

# ----------------------------------------------------------------------
# 调整布局并显示/保存
# ----------------------------------------------------------------------
plt.tight_layout(pad=0.8, w_pad=1.0, h_pad=0.5)

# 显示图形
plt.show()

# 保存为矢量格式（PDF）供期刊使用
# plt.savefig('combined_barplots.pdf', format='pdf', bbox_inches='tight')
# plt.savefig('combined_barplots.png', dpi=300, bbox_inches='tight')