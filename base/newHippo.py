# 🔥 核心修复：强制使用无界面后端，彻底解决PyCharm报错
import matplotlib
matplotlib.use('Agg')  # 不弹窗，直接渲染保存图片
from numpy.polynomial.legendre import Legendre  # HiPPO基于勒让德多项式
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['Times New Roman', 'Arial', 'sans-serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False
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

# 色彩转为鲜明的高对比度色：明蓝、品紫、天蓝
ax.fill(tri_left_2d[:,0], tri_left_2d[:,1], color='#4169E1', alpha=0.5, edgecolor='#0000FF')
ax.fill(tri_mid_2d[:,0], tri_mid_2d[:,1], color='#BA55D3', alpha=0.5, edgecolor='#8A2BE2')
ax.fill(tri_right_2d[:,0], tri_right_2d[:,1], color='#00BFFF', alpha=0.5, edgecolor='#00B2EE')

# ====================== 4. 结构化保持虚线 ======================
v_left  = project(0.7, 0, 1.5)
v_mid   = project(2.1, 0, 1.5)
v_right = project(3.1, 0, 1.5)
ax.plot([v_left[0], v_right[0]], [v_left[1], v_right[1]], '--', color='#009955', linewidth=1.5)

# ====================== 5. 绘制模拟信号曲线（历史时间-幅度平面） ======================
t_signal = np.linspace(0, 3, 600)  # 采样点提升至 600 以支撑更极端的动态
# 振幅调制增强（高低明显） + 频率调制增强（疏密明显）
env = 0.5 + 0.45 * np.cos(4 * t_signal)
# 加入偏移量 +1.3 以确保结尾处（t=3）信号处于下降趋势
phase = 5 * t_signal + 12 * np.sin(0.6 * t_signal) + 1.3
z_signal = env * np.sin(phase) + 1.1
cx_signal, cy_signal = project(0, t_signal, z_signal)
ax.plot(cx_signal, cy_signal, color='#D62728', linewidth=3.0, label='Original Signal')

# 添加左侧红色曲线到时间t轴的垂直阴影面
cx_signal_base, cy_signal_base = project(0, t_signal, 0)
fill_sig_x = np.concatenate([cx_signal, cx_signal_base[::-1]])
fill_sig_y = np.concatenate([cy_signal, cy_signal_base[::-1]])
ax.fill(fill_sig_x, fill_sig_y, color='#D62728', alpha=0.2)
ax.text(cx_signal[0] - 0.43, cy_signal[0] - 0.5, r'Original $f(t)$',
        fontsize=19, fontweight='bold', color='#D62728',
        ha='right', va='center',  # 水平右对齐，垂直居中对齐
        zorder=10)

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
# ====================== 7. 绘制HiPPO基（黑色曲线分层，贴合你的图） ======================
# ====================== 7. 绘制高度不为0的灰色截面及其内波动的特征基 ======================
# 将截面往上移，与坐标轴位置相当，单高度不为0
z_plane = 0.1  
# 画类似手绘图中的斜向灰色截面
t_plane_min, t_plane_max = -0.2, 1.8
x_plane_min, x_plane_max = -0.2, 4.2
corners = [
    project(x_plane_min, t_plane_min, z_plane),
    project(x_plane_max, t_plane_min, z_plane),
    project(x_plane_max, t_plane_max, z_plane),
    project(x_plane_min, t_plane_max, z_plane)
]
px = [c[0] for c in corners] + [corners[0][0]]
py = [c[1] for c in corners] + [corners[0][1]]
ax.fill(px, py, color='#b5b5b5', alpha=0.4, zorder=1) # 灰色截面
ax.plot(px, py, color='#666666', linewidth=1.5, zorder=2)

x_hippo = np.linspace(0, 3.5, 200)
t_list = [0.4, 0.9, 1.4]
colors = ['#2CA02C', '#1F77B4', '#FF7F0E']  # 学术经典配色：绿、蓝、橙

# 改为明显的截面上波动的曲线
def hippo(x, order):
    if order == 0:
        return 0.15 * np.sin(4 * x)
    elif order == 1:
        return 0.18 * np.cos(5 * x)
    elif order == 2:
        return 0.12 * np.sin(7 * x + 1)
    return np.zeros_like(x)

tri_list_3d = [tri_left_3d, tri_mid_3d, tri_right_3d]
for idx, (t0, c) in enumerate(zip(t_list, colors)):
    # 将基函数偏移至截面高度作画
    z = hippo(x_hippo, idx) + z_plane
    cx, cy = project(x_hippo, t0, z)
    
    # 截面上波动的基底曲线
    ax.plot(cx, cy, color=c, linewidth=2.8, zorder=3)

    # 每一条基进行标注
    label_pt = project(3.6, t0, hippo(np.array([3.6]), idx)[0] + z_plane)
    ax.text(label_pt[0] + 0.1, label_pt[1], f'$P_{idx}(x)$', color='black', fontsize=17, fontweight='bold', zorder=6)

# 亮点：每个三角形的最顶点（代表特定时刻的记忆窗口状态）都与所有的特征基相连
# 体现：同一个时序截面里的信息，是被拆解投影到了 P0, P1, P2 等多个正交基的组合上的
for tri in tri_list_3d:
    # 1. 计算三角形顶点的投影坐标
    # 注意：tri[2] 通常代表三角形的顶点 (x, t, z)
    pt_peak = project(tri[2][0], tri[2][1], tri[2][2])

    # 【新增】绘制顶点（源点）：深色中心 + 白色描边
    ax.scatter(pt_peak[0], pt_peak[1], color='#333', s=40,
               edgecolor='white', linewidth=1, zorder=10,
               label='State Feature' if 'State Feature' not in [t.get_label() for t in ax.texts] else "")

    # 2. 遍历基函数，绘制连线与落点
    for base_idx, (t0, c) in enumerate(zip(t_list, colors)):
        # 计算在第 base_idx 条基上的 Z 轴落点
        # 这里的 z_plane 是你定义的基函数基准高度
        z_base_pt = hippo(np.array([tri[2][0]]), base_idx)[0] + z_plane
        pt_base = project(tri[2][0], t0, z_base_pt)

        # --- 绘制虚连线 ---
        ax.plot([pt_peak[0], pt_base[0]], [pt_peak[1], pt_base[1]],
                color=c, linestyle=':', lw=2, alpha=0.5, zorder=5)

        # --- 【核心新增】绘制基空间落点（投影点） ---
        # 颜色与对应的基函数保持一致，突出映射关系
        ax.scatter(pt_base[0], pt_base[1], color=c, s=25,
                   edgecolor='black', linewidth=0.8, marker='o', zorder=10)
# ====================== 7.5 重构黑色轨迹（严格与左侧一致） ======================
# 读取原信号 t_signal, z_signal，保证黑线外形100%一致
t_recon = t_signal
env_recon = 0.5 + 0.45 * np.cos(4 * t_recon)
phase_recon = 5 * t_recon + 12 * np.sin(0.6 * t_recon) + 1.3
z_recon = env_recon * np.sin(phase_recon) + 1.1

cx_recon, cy_recon = project(5.0, t_recon, z_recon)
ax.plot(cx_recon, cy_recon, color='blue', linewidth=3.5, zorder=20)

# 底面参考线
cx_r_base, cy_r_base = project(5.0, t_recon, 0)
ax.plot(cx_r_base, cy_r_base, color='gray', linewidth=1.2, linestyle='--', alpha=0.5)

# 增加右侧黑色曲线到时间t轴平面的阴影面
fill_recon_x = np.concatenate([cx_recon, cx_r_base[::-1]])
fill_recon_y = np.concatenate([cy_recon, cy_r_base[::-1]])
ax.fill(fill_recon_x, fill_recon_y, color='blue', alpha=0.15)

# 黑线的起点标注，不再与内部三角形强行相连
black_start = project(4.5, 0, z_recon[0])
ax.text(black_start[0] - 0.3, black_start[1] -0.3, r'Reconstructed $\hat{f}(t)$',
        fontsize=17, fontweight='bold', color='blue')
# ====================== 8. 文字标注（适配参考图说明） ======================
v_left_raw  = project(tri_left_3d[2][0], tri_left_3d[2][1], tri_left_3d[2][2])
v_mid_raw   = project(tri_mid_3d[2][0], tri_mid_3d[2][1], tri_mid_3d[2][2])
v_right_raw = project(tri_right_3d[2][0], tri_right_3d[2][1], tri_right_3d[2][2])

# 远期标注
ax.text(float(v_left_raw[0]), float(v_left_raw[1]+0.13), 'Far History', fontsize=16, color='#D32F2F', ha='center', fontweight='bold')
# 中期标注
ax.text(float(v_mid_raw[0]), float(v_mid_raw[1]+0.13), 'Mid History', fontsize=16, color='#E65A5A', ha='center', fontweight='bold')
# 近期标注
ax.text(float(v_right_raw[0]+0.3), float(v_right_raw[1]), 'Recent', fontsize=16, color='#1565C0', fontweight='bold')

ax.scatter(v_right[0], v_right[1], color='#00CC66', s=120, edgecolor='#009933')
# ax.text((v_left[0]+v_right[0])/2, v_left[1]+0.15, 'Structural Invariance', fontsize=17, fontweight='bold', color='#006633', ha='center')

# ====================== 8. 绘制坐标轴 ======================
origin = project(0,0,0)

# 1. X轴：强调多项式投影空间
x_end = project(5, 0, 0)
ax.arrow(origin[0], origin[1], x_end[0]-origin[0], x_end[1]-origin[1],
         head_width=0.08, head_length=0.15, fc='#222', ec='#222', linewidth=1.5)
# 使用 Latent Space 或 Polynomial Space，配上花体 P
ax.text(float(x_end[0]+0.3), float(x_end[1]-0.05), r'Feature Space ($x$)', 
        fontsize=19, fontweight='bold', color='#222')

# 2. T轴：强调历史时间窗口（通常用 \tau 表示历史偏移）
t_end = project(0, 3.5, 0)
ax.arrow(origin[0], origin[1], t_end[0]-origin[0], t_end[1]-origin[1],
         head_width=0.03, head_length=0.05, fc='#222', ec='#222', linewidth=1.5)
ax.text(float(t_end[0]+1.0), float(t_end[1]-0.15), r'History Time $\tau$', 
        fontsize=19, fontweight='bold', color='#222', ha='right')

# 3. Z轴：强调信号的幅度或状态值
z_end = project(0, 0, 1.8)
ax.arrow(origin[0], origin[1], z_end[0]-origin[0], z_end[1]-origin[1],
         head_width=0.06, head_length=0.1, fc='#222', ec='#222', linewidth=1.5)
ax.text(float(z_end[0]), float(z_end[1]+0.35), r'Magnitude ($z(t)$)',
        fontsize=19, fontweight='bold', color='#222', ha='center')

# ====================== 9. 🔥 直接保存图片（绝对不报错） ======================
ax.set_xlim(-2.5, 7.5)
ax.set_ylim(-3.5, 3.0)
plt.tight_layout()
plt.savefig('最终图表hippo.png', dpi=300, bbox_inches='tight')
# print("✅ 图表已保存！在代码文件夹中找到：最终图表.png")