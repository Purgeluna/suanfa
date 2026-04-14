# 🔥 核心修复：强制使用无界面后端，彻底解决PyCharm报错
import matplotlib
matplotlib.use('Agg')  # 不弹窗，直接渲染保存图片
from numpy.polynomial.legendre import Legendre  # HiPPO基于勒让德多项式
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题
# ====================== 1. 斜二测投影（匹配原图斜轴风格） ======================
def project(x, t, z, k=0.5):
    cx = x - k * t
    cy = z - k * t
    return cx, cy

# ====================== 2. 创建画布 ======================
fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
ax.set_aspect('equal')
ax.set_facecolor('white')

# 隐藏边框刻度（和原图一致）
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
ax.spines[['top', 'right', 'bottom', 'left']].set_visible(False)

# ====================== 3. 绘制三个三角形（严格保留原版尺寸+高度递减） ======================
# 🔥 核心：宽度/间距100%复刻原版 | 高度：远期(0.5) < 中期(1.0) < 近期(1.5=原版大小)
tri_left_3d   = [(0, 0, 0), (0.7, 0, 0), (0.35, 0, 0.5)]   # 远期：宽度同原版，高度减半
tri_mid_3d    = [(1.0, 0, 0), (2.0, 0, 0), (1.5, 0, 1.0)]# 中期：宽度同原版，中等高度
tri_right_3d  = [(2.4, 0, 0), (3.8, 0, 0), (3.1, 0, 1.5)]# 近期：和你原版完全一致！

tri_left_2d   = np.array([project(x, t, z) for x, t, z in tri_left_3d])
tri_mid_2d    = np.array([project(x, t, z) for x, t, z in tri_mid_3d])
tri_right_2d  = np.array([project(x, t, z) for x, t, z in tri_right_3d])

ax.fill(tri_left_2d[:,0], tri_left_2d[:,1], color='#E6E6FA', alpha=0.9, edgecolor='#7B68EE')
ax.fill(tri_mid_2d[:,0], tri_mid_2d[:,1], color='#FFE4B5', alpha=0.9, edgecolor='#FF8C00')
ax.fill(tri_right_2d[:,0], tri_right_2d[:,1], color='#E0FFFF', alpha=0.9, edgecolor='#00CED1')

# ====================== 4. 结构化保持虚线（原版水平等高样式，匹配新三角形） ======================
# 严格沿用原版风格：两段水平虚线，连接三个三角形顶部顶点（高度均为1.5）
v_left  = project(0.0, 0, 0.0)   # 左三角顶点
v_mid   = project(1.4, 0, 0)   # 中三角顶点
v_right = project(0.7, 0, 1.5)   # 右三角顶点
# 第一段虚线：左→中
# ax.plot([v_left[0], v_mid[0]], [v_left[1], v_mid[1]], '--', color='#888888', linewidth=1.5)
# 第二段虚线：中→右
ax.plot([v_mid[0], v_right[0]], [v_mid[1], v_right[1]], '--', color='#888888', linewidth=1.5)
ax.plot([v_right[0], v_left[0]], [v_right[1], v_left[1]], '--', color='#888888', linewidth=1.5)  # 左边（补全缺失部分）




# ====================== 5. 绘制模拟信号曲线（历史时间-幅度平面） ======================
t_signal = np.linspace(0, 3, 200)
z_signal = 0.5 * np.sin(4 * t_signal) + 1.1
cx_signal, cy_signal = project(0, t_signal, z_signal)
ax.plot(cx_signal, cy_signal, color='#FF4500', linewidth=2.5, label='原始信号')


# ====================== 6. 绘制幅度0底面投影 ======================
x_proj = z_signal
cx_proj, cy_proj = project(x_proj+0.2, t_signal, 0)
ax.plot(cx_proj, cy_proj, color='#343399', linewidth=2, label='底面投影')
# 右侧底面基线
base_cx, base_cy = project(0, t_signal, 0)
# 闭合填充（核心修复，直接填充区域）
fill_x = np.concatenate([cx_proj, base_cx[::-1]])
fill_y = np.concatenate([cy_proj, base_cy[::-1]])
ax.fill(fill_x, fill_y, color='#998654', alpha=0.3)

# 优化：均匀选取少量关键点，仅绘制6条连线，整洁不凌乱
indices = np.linspace(0, len(t_signal)-1, 10, dtype=int)
for i in indices:
    ax.plot([cx_signal[i], cx_proj[i]], [cy_signal[i], cy_proj[i]], 'b--', linewidth=1, alpha=0.2)

# ====================== 8. 【修改】文字标注（适配参考图说明） ======================
# 远期标注
ax.text(v_left[0], v_left[1]-0.3, '远期', fontsize=13, color='#D32F2F', ha='center', fontweight='bold')
# 中期标注
ax.text(v_mid[0], v_mid[1]-0.3, '中期', fontsize=13, color='#E65A5A', ha='center', fontweight='bold')
# 近期标注
ax.text(v_right[0]+0.3, v_right[1], '近期', fontsize=13, color='#1565C0', fontweight='bold')
# 原始输入标注
ax.text((v_left[0]+v_right[0])/2, v_right[1]+0.2, '原始输入 (Ground Truth)', fontsize=12, color='#666666', ha='center')

# ====================== 9. 绘制坐标轴（保持不变） ======================
origin = project(0,0,0)
# 信号特征轴 (x轴)
x_end = project(5, 0, 0)
ax.arrow(origin[0], origin[1], x_end[0]-origin[0], x_end[1]-origin[1],
         head_width=0.08, head_length=0.15, fc='#222', ec='#222', linewidth=1.2)
ax.text(x_end[0]+0.25, x_end[1], '信号特征 (x)', fontsize=12, fontweight='bold', color='#222')

# 历史时间轴 (t轴)
t_end = project(0, 3.5, 0)
ax.arrow(origin[0], origin[1], t_end[0]-origin[0], t_end[1]-origin[1],
         head_width=0.03, head_length=0.05, fc='#222', ec='#222', linewidth=1.2)
ax.text(t_end[0]-0.35, t_end[1]-0.15, '历史时间 (t)', fontsize=12, fontweight='bold', color='#222', ha='right')

# 幅度轴 (z轴)
z_end = project(0, 0, 1.8)
ax.arrow(origin[0], origin[1], z_end[0]-origin[0], z_end[1]-origin[1],
         head_width=0.06, head_length=0.1, fc='#222', ec='#222', linewidth=1.2)
ax.text(z_end[0], z_end[1]+0.1, '幅度', fontsize=12, fontweight='bold', color='#222', ha='center')

# ====================== 10. 保存图片 ======================
ax.set_xlim(-2, 7)
ax.set_ylim(-2, 2)
plt.tight_layout()
plt.savefig('最终图表2.png', dpi=300, bbox_inches='tight')