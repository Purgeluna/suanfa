import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.special import legendre

# Force standard backend to resolve potential PyCharm/Anaconda compatibility issues
try:
    matplotlib.use('TkAgg')
except Exception:
    pass

# Global style configuration
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['axes.facecolor'] = '#fdfdfd'
plt.rcParams['grid.color'] = '#e5e7eb'
plt.rcParams['grid.linewidth'] = 0.5


def draw_rnn_decay(ax):
    """Draw Left Plot: RNN Exponential Decay Mechanism"""
    steps = np.arange(7)
    # Exponential decay formula: weights = (1-z)^k
    weights = 0.5 ** steps

    # Gradient colors from Dark Red to Light Orange
    colors = plt.cm.Reds(np.linspace(0.85, 0.3, len(steps)))

    # Horizontal bar plot
    bars = ax.barh(steps, weights, color=colors, edgecolor='none', height=0.6, alpha=0.9)

    # Annotate weight values
    for i, w in enumerate(weights):
        ax.text(w + 0.03, i, f"{w:.3f}", va='center', fontsize=12, color='#4b5563', fontweight='500')

    ax.set_yticks(steps)
    # Tick labels representing back-in-time steps X_{t-k}
    ax.set_yticklabels([f"$X_{{t-{i}}}$" for i in steps], fontsize=13)

    ax.set_xlabel("Memory Contribution to $h_t$\n(Weight for hidden state update)", fontsize=13, labelpad=10)
    ax.set_ylabel("Time Lag (Backtrack steps $k$)", fontsize=13)

    # Centered Title
    ax.set_title("Exponential Decay Mechanism", loc='center', pad=25,
                 fontsize=14, fontweight='bold', color='#991b1b')
    # Consolidated Mathematical Block in Top-Right
    combined_formula = (
        r"$\mathbf{h_t = \sigma(W h_{t-1} + U x_t)}$" "\n"
        r"$\frac{\partial h_t}{\partial h_{t-k}} \propto W^k$" "\n"
        # r"$\Longrightarrow$ Exponential Decay" "\n"
        # r"Long-term memory $\to 0$"
    )
    # ax.text(0.75, 7.5, combined_formula, fontsize=11, color='#991b1b')
    # ax.text(0.72, 7.5, combined_formula, fontsize=10, color='#b91c1c', va='top',
    #         bbox=dict(facecolor='#fef2f2', edgecolor='#fecaca', boxstyle='round,pad=0.7'))
    # Axis styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94a3b8')
    ax.spines['bottom'].set_color('#94a3b8')
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    ax.set_xlim(0, 1.2)


def draw_hippo_reconstruction(ax):
    """Draw Right Plot: HiPPO Orthogonal Polynomial Reconstruction"""
    t = np.linspace(0, 1, 600)
    # Input signal
    signal = np.sin(2 * np.pi * t) + 0.5 * np.cos(10 * np.pi * t) + 0.3 * np.sin(20 * np.pi * t)

    ax.axhline(0, color='#94a3b8', linewidth=0.8, alpha=0.5)
    ax.plot(t, signal, color='#1e293b', linestyle='--', label="Original $u(\\tau)$", linewidth=1.5, zorder=2, alpha=0.7)

    ns = [2, 12]
    colors = ['#ef4444', '#f59e0b', '#2563eb']
    # labels = ["$N=2$ (Coarse)", "$N=12$ (Fine)"]
    labels = ["$N=2$ (Low Precision)", "$N=12$ (High Precision)"]

    x = 2 * t - 1
    for n, color, label in zip(ns, colors, labels):
        coeffs = np.polyfit(x, signal, n)
        reconstruction = np.polyval(coeffs, x)
        ax.plot(t, reconstruction, color=color, label=label, linewidth=2.5, zorder=3)
        ax.fill_between(t, signal, reconstruction, color=color, alpha=0.08, zorder=1)

    # Centered Title
    ax.set_title("Polynomial Projection & Reconstruction", loc='center', pad=25,
                 fontsize=14, fontweight='bold', color='#1e40af')
    ax.set_xlabel("Continuous History Time $\\tau \in [0, t]$ (Lookback window)", fontsize=13, labelpad=10)
    ax.set_ylabel("Signal Amplitude / Reconstructed Value", fontsize=13)

    # Consolidated Mathematical Block in Top-Right (HiPPO)
    hippo_combined_formula = (
        r"$\mathbf{\dot{c}(t) = A c(t) + B u(t)}$" "\n"
        r"$u(t) \approx \sum_{n=0}^N c_n \phi_n(t)$" "\n"
        r"$\|u - \hat{u}_N\| = \mathcal{O}(N^{-1})$" "\n"
        # r"Precise long-term memory"
    )
    # ax.text(0.72, 1.22, hippo_combined_formula, fontsize=10, color='#1e40af', va='top',
    #         bbox=dict(facecolor='#eff6ff', edgecolor='#bfdbfe', boxstyle='round,pad=0.7'))

    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(['0', '$t/4$', '$t/2$', '$3t/4$', '$t$'], fontsize=10)

    ax.legend(loc='lower left', frameon=True, fancybox=True, shadow=False,
              fontsize=12, facecolor='white', edgecolor='#e5e7eb', borderpad=1)

    # Axis styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94a3b8')
    ax.spines['bottom'].set_color('#94a3b8')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_ylim(-1.6, 1.8)


# Create high-resolution canvas
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.5), dpi=100)
plt.subplots_adjust(wspace=0.25, bottom=0.15)

draw_rnn_decay(ax1)
draw_hippo_reconstruction(ax2)

plt.tight_layout(pad=4.0)

plt.savefig("rnn_hippo_comparison.png", dpi=300, bbox_inches='tight')
plt.show()


