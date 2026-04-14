

# 🔥 核心修复：强制使用无界面后端，彻底解决PyCharm报错
import matplotlib
matplotlib.use('Agg')  # 不弹窗，直接渲染保存图片
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

# ====================== 3. 绘制三个三角形（严格保留原版尺寸+高度递减） ======================
tri_left_3d   = [(0, 0, 0), (0.7, 0, 0), (0.35, 0, 0.5)]   # 远期
tri_mid_3d    = [(1.0, 0, 0), (2.0, 0, 0), (1.5, 0, 1.0)]  # 中期
tri_right_3d  = [(2.4, 0, 0), (3.8, 0, 0), (3.1, 0, 1.5)]  # 近期

tri_left_2d   = np.array([project(x, t, z) for x, t, z in tri_left_3d])
tri_mid_2d    = np.array([project(x, t, z) for x, t, z in tri_mid_3d])
tri_right_2d  = np.array([project(x, t, z) for x, t, z in tri_right_3d])

ax.fill(tri_left_2d[:,0], tri_left_2d[:,1], color='#4169E1', alpha=0.5, edgecolor='#0000FF')
ax.fill(tri_mid_2d[:,0], tri_mid_2d[:,1], color='#BA55D3', alpha=0.5, edgecolor='#8A2BE2')
ax.fill(tri_right_2d[:,0], tri_right_2d[:,1], color='#00BFFF', alpha=0.5, edgecolor='#00B2EE')

# ====================== 4. 结构化保持虚线 ======================
v_left  = project(0.0, 0, 0.0)
v_mid   = project(1.4, 0, 0)
v_right = project(0.7, 0, 1.5)

v_left2  = project(1.2, 0, 0.0)
v_mid2   = project(2.6, 0, 0)
v_right2 = project(1.9, 0, 1.5)

# 绘制左侧虚线框架
ax.plot([v_mid[0], v_right[0]], [v_mid[1], v_right[1]], '--', color='#888888', linewidth=1.2, alpha=0.6)
ax.plot([v_right[0], v_left[0]], [v_right[1], v_left[1]], '--', color='#888888', linewidth=1.2, alpha=0.6)

# 绘制中部虚线框架（对齐 newHippo 风格）
ax.plot([v_mid2[0], v_right2[0]], [v_mid2[1], v_right2[1]], '--', color='#888888', linewidth=1.2, alpha=0.6)
ax.plot([v_right2[0], v_left2[0]], [v_right2[1], v_left2[1]], '--', color='#888888', linewidth=1.2, alpha=0.6)

# ====================== 5. 绘制高度不为0的灰色截面平面 ======================
z_plane = 0.1
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

# ====================== 6. 绘制立体的指数衰减梯度曲线 (RNN Vanishing Gradient) ======================
x_curve = np.linspace(0, 3.8, 200)
# 梯度从最近时刻(x=3.8)向远期(x=0)呈指数衰减
grad_z = 0.9 * np.exp(1.2 * (x_curve - 3.8))
t_curve = np.full_like(x_curve, 0.8)  # 在截面上的固定历史轴位置

cx, cy = project(x_curve, t_curve, grad_z + z_plane)
cx0, cy0 = project(x_curve, t_curve, z_plane)

# 画立体的带状梯度曲线
ax.plot(cx, cy, color='#D62728', linewidth=3.0, zorder=3)
fill_x = np.concatenate([cx, cx0[::-1]])
fill_y = np.concatenate([cy, cy0[::-1]])
ax.fill(fill_x, fill_y, color='#D62728', alpha=0.4, zorder=2)

# 在梯度终点添加标签
label_pt = project(3.8, 0.8, grad_z[-1] + z_plane)
ax.text(label_pt[0] - 0.5, label_pt[1]-0.1, r'$\nabla h_t$', color='#D62728', fontsize=20, fontweight='bold', zorder=6)

# ====================== 7. 将每个三角形与梯度曲线相连 ======================
tri_list_3d = [tri_left_3d, tri_mid_3d, tri_right_3d]
for idx, tri in enumerate(tri_list_3d):
    # 提取三角形顶点
    pt_peak = project(tri[2][0], tri[2][1], tri[2][2])

    # 绘制顶点（源点）
    ax.scatter(pt_peak[0], pt_peak[1], color='#333', s=40, edgecolor='white', linewidth=1, zorder=10)

    # 对应 x 坐标处的梯度高度
    z_grad_pt = 0.9 * np.exp(1.2 * (tri[2][0] - 3.8)) + z_plane
    pt_base = project(tri[2][0], 0.8, z_grad_pt)

    # 连线下落到梯度曲线上
    ax.plot([float(pt_peak[0]), float(pt_base[0])], [float(pt_peak[1]), float(pt_base[1])], color='#D62728', linestyle=':', lw=2.0, alpha=0.7, zorder=5)

    # 画截面上的投影连接点
    ax.scatter(float(pt_base[0]), float(pt_base[1]), color='#D62728', s=30, edgecolor='white', linewidth=0.8, marker='o', zorder=10)

# 【核心新增】基于用户原有灰色虚线绘制偏差箭头
peak_left_actual = project(0.35, 0, 0.5)
ax.annotate('', xy=(float(peak_left_actual[0]), float(peak_left_actual[1])), 
            xytext=(float(v_right[0]), float(v_right[1])),
            arrowprops=dict(facecolor='black', shrink=0.08, width=3.5, headwidth=10, zorder=15))

peak_mid_actual = project(1.5, 0, 1.0)
ax.annotate('', xy=(float(peak_mid_actual[0]), float(peak_mid_actual[1])), 
            xytext=(float(v_right2[0]), float(v_right2[1])),
            arrowprops=dict(facecolor='black', shrink=0.08, width=3.5, headwidth=10, zorder=15))

# 添加文字说明
ax.text(float(v_right[0] - 0.40), float(v_right[1] - 0.35), 'Bias',
        fontsize=17, fontweight='bold', color='black')

# ====================== 8. 绘制模拟信号曲线与阴影 ======================
t_signal = np.linspace(0, 3, 600)  # 采样点提升至 600
# 振幅调制增强（高低明显） + 频率调制增强（疏密明显）
env = 0.5 + 0.45 * np.cos(4 * t_signal)
# 增加偏移量 +1.3 以获得结尾处的下降趋势
phase = 5 * t_signal + 12 * np.sin(0.6 * t_signal) + 1.3
z_signal = env * np.sin(phase) + 1.1
cx_signal, cy_signal = project(0, t_signal, z_signal)
ax.plot(cx_signal, cy_signal, color='#FF7F0E', linewidth=3.0, label='Original Signal')

cx_signal_base, cy_signal_base = project(0, t_signal, 0)
fill_sig_x = np.concatenate([cx_signal, cx_signal_base[::-1]])
fill_sig_y = np.concatenate([cy_signal, cy_signal_base[::-1]])
ax.fill(fill_sig_x, fill_sig_y, color='#FF7F0E', alpha=0.2)
ax.text(float(cx_signal[0] - 0.33), float(cy_signal[0] - 0.5), r'Original Signal $f(t)$',
        fontsize=19, fontweight='bold', color='#FF7F0E', ha='right', va='center', zorder=10)

# ====================== 9. 文字标注（适配参考图说明） ======================
v_left_raw  = project(tri_left_3d[2][0], tri_left_3d[2][1], tri_left_3d[2][2])
v_mid_raw   = project(tri_mid_3d[2][0], tri_mid_3d[2][1], tri_mid_3d[2][2])
v_right_raw = project(tri_right_3d[2][0], tri_right_3d[2][1], tri_right_3d[2][2])

# 远期标注
ax.text(float(v_left_raw[0]), float(v_left_raw[1]+0.13), 'Far History', fontsize=16, color='#D32F2F', ha='center', fontweight='bold')
# 中期标注
ax.text(float(v_mid_raw[0]), float(v_mid_raw[1]+0.23), 'Mid History', fontsize=16, color='#E65A5A', ha='center', fontweight='bold')
# 近期标注
ax.text(float(v_right_raw[0]+0.3), float(v_right_raw[1]), 'Recent', fontsize=16, color='#1565C0', fontweight='bold')
# ax.text(float((v_left_raw[0]+v_right_raw[0])/2), float(v_right_raw[1]+0.2), 'Sequence Input', fontsize=16, color='#666666', ha='center', fontweight='bold')

# ====================== 10. 绘制右侧重构轨迹（全面体现“信息丢失”：衰减+模糊） ======================
np.random.seed(42)
t_recon = t_signal
env_recon = 0.5 + 0.45 * np.cos(4 * t_recon)

# 【核心修改 1】信息随历史深度（t 越小）剧烈丢失：幅度从 0.1 (远期) 渐变到 0.7 (近期)
decay = np.linspace(0.1, 0.7, len(t_recon))

# 【核心修改 2】相位简化：模拟高通/细节分量丢失 (将 12*sin 调成 3*sin)
phase_lost = 5 * t_recon + 3 * np.sin(0.6 * t_recon) + 1.3

# 基础失真信号
z_recon_base = decay * (env_recon * np.sin(phase_lost)) + 1.1

# 增加少许毛刺以体现不稳定性
z_recon = z_recon_base + 0.05 * np.sin(100 * t_recon) + 0.02 * np.random.normal(0, 1, len(t_recon))

x_recon_pos = 4.5  # 统一在 4.5 处，实现视觉对齐

cx_recon, cy_recon = project(x_recon_pos, t_recon, z_recon)
cx_r_base, cy_r_base = project(x_recon_pos, t_recon, 0)

# 绘制重构轨迹蓝线
ax.plot(cx_recon, cy_recon, color='#1E90FF', linewidth=3.5, zorder=20)
ax.plot(cx_r_base, cy_r_base, color='gray', linewidth=1.2, linestyle='--', alpha=0.5)

# 阴影填充
fill_recon_x = np.concatenate([cx_recon, cx_r_base[::-1]])
fill_recon_y = np.concatenate([cy_recon, cy_r_base[::-1]])
ax.fill(fill_recon_x, fill_recon_y, color='#1E90FF', alpha=0.15)

# 标注
ax.text(float(cx_recon[0] + 0.1), float(cy_recon[0] - 0.3), r'Reconstructed $\hat{f}(t)$',
        fontsize=19, fontweight='bold', color='#1E90FF', va='bottom', zorder=21)

# ====================== 11. 绘制坐标轴 (Premium Style) ======================
origin = project(0,0,0)

# 1. X轴：
x_end_pos = 5.0
x_end = project(x_end_pos, 0, 0)
ax.arrow(origin[0], origin[1], x_end[0]-origin[0], x_end[1]-origin[1],
         head_width=0.08, head_length=0.15, fc='#222', ec='#222', linewidth=1.5)
ax.text(float(x_end[0]+0.3), float(x_end[1]-0.05), r'Feature Space ($x$)', 
        fontsize=19, fontweight='bold', color='#222')

# 2. T轴：
t_end = project(0, 3.5, 0)
ax.arrow(origin[0], origin[1], t_end[0]-origin[0], t_end[1]-origin[1],
         head_width=0.03, head_length=0.05, fc='#222', ec='#222', linewidth=1.5)
ax.text(float(t_end[0]+1.0), float(t_end[1]-0.15), r'History Time $\tau$', 
        fontsize=19, fontweight='bold', color='#222', ha='right')

# 3. Z轴：
z_end = project(0, 0, 1.8)
ax.arrow(origin[0], origin[1], z_end[0]-origin[0], z_end[1]-origin[1],
         head_width=0.06, head_length=0.1, fc='#222', ec='#222', linewidth=1.5)
ax.text(float(z_end[0]), float(z_end[1]+0.15), r'Magnitude ($h_t$)', 
        fontsize=19, fontweight='bold', color='#222', ha='center')

# ====================== 12. 保存图片 ======================
ax.set_xlim(-2.5, 7.5)
ax.set_ylim(-3.5, 3.0)
plt.tight_layout()
plt.savefig('最终图表_rnn_v2.png', dpi=300, bbox_inches='tight')