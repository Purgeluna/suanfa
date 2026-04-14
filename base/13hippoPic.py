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

# ====================== 3. 绘制三个三角形 ======================
tri_left_3d   = [(0, 0, 0), (1.4, 0, 0), (0.7, 0, 1.5)]
tri_mid_3d    = [(1.2, 0, 0), (2.6, 0, 0), (1.9, 0, 1.5)]
tri_right_3d  = [(2.4, 0, 0), (3.8, 0, 0), (3.1, 0, 1.5)]

tri_left_2d   = np.array([project(x, t, z) for x, t, z in tri_left_3d])
tri_mid_2d    = np.array([project(x, t, z) for x, t, z in tri_mid_3d])
tri_right_2d  = np.array([project(x, t, z) for x, t, z in tri_right_3d])

# 同色系高级柔和风（偏紫调/冷调，类似 7B68EE 质感）
# 冷紫 + 暖紫 + 雾蓝，全都类似 7B68EE 质感
ax.fill(tri_left_2d[:,0], tri_left_2d[:,1], color='#C3B5F0', alpha=0.7, edgecolor='#7A7BE8')
ax.fill(tri_mid_2d[:,0], tri_mid_2d[:,1], color='#E2B6F7', alpha=0.7, edgecolor='#B96BD6')
ax.fill(tri_right_2d[:,0], tri_right_2d[:,1], color='#A2B9F7', alpha=0.7, edgecolor='#9885E8')

# ====================== 4. 结构化保持虚线 ======================
v_left  = project(0.7, 0, 1.5)
v_mid   = project(2.1, 0, 1.5)
v_right = project(3.1, 0, 1.5)
ax.plot([v_left[0], v_right[0]], [v_left[1], v_right[1]], '--', color='#009955', linewidth=1.5)

# ====================== 5. 绘制模拟信号曲线（历史时间-幅度平面） ======================
t_signal = np.linspace(0, 3, 200)
z_signal = 0.5 * np.sin(4 * t_signal) + 1.1
cx_signal, cy_signal = project(0, t_signal, z_signal)
ax.plot(cx_signal, cy_signal, color='#FF4500', linewidth=2.5, label='原始信号')

# ====================== 6. 绘制幅度0底面投影 ======================
# 核心修改：将信号的z值映射到底面的x轴，t不变，z=0
# x_proj = z_signal  # 把幅度z作为底面的x坐标
# cx_proj, cy_proj = project(x_proj+0.2, t_signal, 0)  # 底面投影点：(x=z_signal, t, z=0)
# ax.plot(cx_proj, cy_proj, color='#993399', linewidth=2, label='底面投影')  # 紫色线
# ====================== 6. 绘制右侧底面投影（带填充颜色） ======================
# ====================== 6. 绘制右侧底面投影（带纯色填充，必生效） ======================
# x_proj = z_signal
# cx_proj, cy_proj = project(x_proj+0.2, t_signal, 0)
# ax.plot(cx_proj, cy_proj, color='#993399', linewidth=2, label='底面投影')
# # 右侧底面基线
# base_cx, base_cy = project(0, t_signal, 0)
# # 闭合填充（核心修复，直接填充区域）
# fill_x = np.concatenate([cx_proj, base_cx[::-1]])
# fill_y = np.concatenate([cy_proj, base_cy[::-1]])
# ax.fill(fill_x, fill_y, color='#993399', alpha=0.3)
#
# indices = np.linspace(0, len(t_signal)-1, 10, dtype=int)
# for i in indices:
#     ax.plot([cx_signal[i], cx_proj[i]], [cy_signal[i], cy_proj[i]], 'b--', linewidth=1, alpha=0.2)

# 基的绘制
# # ====================== 7. 绘制HiPPO基（黑色曲线分层，贴合你的图） ======================
# # ====================== 7. HiPPO正交基（沿X轴水平绘制 + 标准基形态 + 彩色阴影面） ======================
# # 核心：标准HiPPO勒让德基（数学特征）+ 水平X轴延伸 + 分层填充阴影
# x_hippo = np.linspace(0, 3.5, 200)  # 沿水平X轴
# t_list = [0.4, 0.9, 1.4]  # 3条基分层固定时间t，水平排布
# colors = ['#4A7C59', '#3D5A80', '#EE6C4D']  # 3组区分色
# fills = ['#D5E6D9', '#C8D4E3', '#FADBD2']  # 对应浅阴影
#
# # 标准HiPPO正交基函数
# def hippo(x, order):
#     if order == 0:
#         return 0.12 * np.ones_like(x)
#     elif order == 1:
#         return 0.15 * (x - 1.75)
#     elif order == 2:
#         return 0.18 * (x ** 2 - 3.5 * x + 2.5)
#     return np.zeros_like(x)
#
#
# # 逐条绘制基曲线 + 阴影面
# for idx, (t0, c, f) in enumerate(zip(t_list, colors, fills)):
#     z = hippo(x_hippo, idx)
#     cx, cy = project(x_hippo, t0, z)
#     # 🔥 核心修复：强制将基线转为数组，解决标量报错
#     cx0, _ = project(x_hippo, t0, 0)
#     cy0 = np.full_like(cx0, 0 - 0.5 * t0)  # 关键！生成等长数组，不是单个浮点数
#
#     # 绘制基曲线
#     ax.plot(cx, cy, color=c, linewidth=2.2)
#     # 闭合填充阴影面
#     fill_x = np.concatenate([cx, cx0[::-1]])
#     fill_y = np.concatenate([cy, cy0[::-1]])
#     ax.fill(fill_x, fill_y, color=f, alpha=0.4)
#
# # 简洁标注
# ax.text(1.75, -0.7, 'HiPPO 正交基', fontsize=12, color='#222', ha='center')


# ====================== 8. 文字标注 ======================
ax.scatter(v_right[0], v_right[1], color='#00CC66', s=120, edgecolor='#009933')
ax.text(v_right[0]+0.3, v_right[1], '当前时刻重构', fontsize=13, color='#006633')
ax.text((v_left[0]+v_right[0])/2, v_left[1]+0.1, '结构化保持 (Structural Invariance)', fontsize=15, color='#006633', ha='center')

# ====================== 8. 绘制坐标轴 ======================
# ====================== 8. 绘制坐标轴（箭头100%显示，精准修复） ======================
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


# 幅度轴 (z轴)【终极修复：不触碰边界，箭头强制可见】
z_end = project(0, 0, 1.8)  # 改为1.8，避开ylim边界
ax.arrow(origin[0], origin[1], z_end[0]-origin[0], z_end[1]-origin[1],
         head_width=0.06, head_length=0.1, fc='#222', ec='#222', linewidth=1.2)
ax.text(z_end[0], z_end[1]+0.1, '幅度', fontsize=12, fontweight='bold', color='#222', ha='center')

# ====================== 9. 🔥 直接保存图片（绝对不报错） ======================
ax.set_xlim(-2, 7)
ax.set_ylim(-2, 2)
plt.tight_layout()
plt.savefig('最终图表.png', dpi=300, bbox_inches='tight')
# print("✅ 图表已保存！在代码文件夹中找到：最终图表.png")