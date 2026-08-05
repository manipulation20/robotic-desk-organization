#!/home/dongyi/anaconda3/envs/YOLOnew/bin/python

# conda activate YOLOnew
# export PYTHONPATH=/home/dongyi/anaconda3/envs/YOLOnew/lib/python3.12/site-packages

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ----------------------------------------------------------------------
# 全局字体配置
# Linux 通常无 Times New Roman；Liberation Serif 与其度量兼容，期刊可用
# ----------------------------------------------------------------------
_preferred_fonts = [
    'Times New Roman', 'Times', 'Liberation Serif', 'FreeSerif', 'DejaVu Serif'
]
_available = {f.name for f in plt.matplotlib.font_manager.fontManager.ttflist}
FONT_NAME = next((f for f in _preferred_fonts if f in _available), 'DejaVu Serif')

FONT_SCALE = 1
BASE_FONTSIZE = 25
AXIS_LABEL_FONTSIZE = 30  # x/y 轴标签字体大小
TICK_LABEL_FONTSIZE = 23  # x/y 轴刻度标签字体大小
ANNOT_FONTSIZE = 23       # 单元格中数值字体大小
CBAR_LABEL_FONTSIZE = 30  # 颜色条标签字体大小
CBAR_TICK_FONTSIZE = 23   # 颜色条刻度字体大小

sns.set_style("whitegrid")
sns.set_context("talk", font_scale=FONT_SCALE)

# 在 seaborn 设置后 **再次强制** 字体，覆盖可能被更改的设置
plt.rcParams.update(
    {
        'font.family': 'serif',
        'font.serif': [FONT_NAME] + _preferred_fonts,
        'mathtext.fontset': 'stix',
        "font.size": BASE_FONTSIZE,
        "axes.labelsize": AXIS_LABEL_FONTSIZE,
        "xtick.labelsize": TICK_LABEL_FONTSIZE,
        "ytick.labelsize": TICK_LABEL_FONTSIZE,
        "axes.titlesize": AXIS_LABEL_FONTSIZE,
    }
)

# 数据准备
# thickness = [2.5, 6.5, 9, 12]  # 厚度 (mm)
thickness = [2.5, 6.5, 9, 12, 24]  # 厚度 (mm)
angles = [0, 3, 6, 9, 12, 15]  # 测试角度

# 表格数据
data = np.array([
    [1, 1, 1, 1, 1, 1],
    [0.9, 1, 1, 1, 1, 1],
    [0.8, 1, 1, 1, 1, 1],
    [0.2, 0.7, 0.8, 1, 0.6, 0.6],
    [0, 0, 0, 0, 0, 0]
])

# 创建热力图
plt.figure(figsize=(10, 6))
ax = sns.heatmap(data, 
            annot=True,  # 在单元格中显示数值
            fmt='.1f',   # 数值格式，保留1位小数
            cmap='YlGn',  # 颜色映射 # 'Greens' 'YlGn'
            annot_kws={'size': ANNOT_FONTSIZE},  # 单元格数值字体大小
            cbar_kws={'label': 'Success rate'},  # 颜色条标签
            xticklabels=[f'{angle}°' for angle in angles],  # x轴标签（不显示正号）
            yticklabels=thickness)  # y轴标签

# 设置标题和轴名称
# plt.title('Thickness and Angle Relationship Heatmap', fontsize=14, fontweight='bold')
plt.xlabel('Prying angle', fontsize=AXIS_LABEL_FONTSIZE)
plt.ylabel('Thickness (mm)', fontsize=AXIS_LABEL_FONTSIZE)

# 设置 x/y 轴刻度标签字体大小
ax.tick_params(axis='x', labelsize=TICK_LABEL_FONTSIZE)
ax.tick_params(axis='y', labelsize=TICK_LABEL_FONTSIZE)

# 设置颜色条字体大小（标签 + 刻度）
cbar = ax.collections[0].colorbar
cbar.ax.set_ylabel('Success rate', fontsize=CBAR_LABEL_FONTSIZE)
cbar.ax.tick_params(labelsize=CBAR_TICK_FONTSIZE)

# 调整布局
plt.tight_layout()
plt.show()


