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


def draw_mechanism_comparison(ax):
    """Draw Left Plot: Memory Weights of RNN vs HiPPO Measures"""
    steps_total = 11
    steps = np.arange(steps_total)

    # 1. RNN: Exponential decay
    rnn_weights = 0.5 ** steps

    # 2. HiPPO-LegT (Translated): True uniform sliding window (e.g., window size 8)
    window_size = 8
    legt_weights = np.zeros_like(steps, dtype=float)
    legt_weights[:window_size] = 0.8  # Uniform inside window

    # 3. HiPPO-LegS (Scaled): Full history, but older data is diluted (~ 1/t scaling)
    legs_weights = 1.0 / (steps + 1.5)

    bar_height = 0.25

    # Generate gradient colors for RNN (from dark red to light red/orange)
    rnn_colors = plt.cm.Reds(np.linspace(0.8, 0.3, len(steps)))

    # Draw RNN with gradient
    ax.barh(steps + bar_height, rnn_weights, height=bar_height,
            color=rnn_colors, label='RNN (Exp. Decay)', edgecolor='none', alpha=0.9)

    # Draw HiPPO-LegS (Solid blueish)
    ax.barh(steps, legs_weights, height=bar_height,
            color='#3b82f6', label='HiPPO-LegS (Scaled)', edgecolor='none', alpha=0.9)

    # Draw HiPPO-LegT (Solid green)
    ax.barh(steps - bar_height, legt_weights, height=bar_height,
            color='#10b981', label='HiPPO-LegT (Window)', edgecolor='none', alpha=0.9)

    # Add text labels for RNN weights back
    for i, w in enumerate(rnn_weights):
        ax.text(w + 0.02, i + bar_height, f"{w:.2f}", va='center', fontsize=8, color='#991b1b')

    ax.set_yticks(steps)
    ax.set_yticklabels([f"$X_{{t-{i}}}$" for i in steps], fontsize=9)
    ax.set_xlabel("Memory Contribution Weight", fontsize=10)
    ax.set_ylabel("Time Lag (Steps backward)", fontsize=10)
    ax.set_title("Memory Mechanism: RNN vs HiPPO Measures", loc='center', pad=20, fontsize=13, fontweight='bold')

    # Combined Math Box explaining both RNN forgetting and HiPPO uniform nature
    comparison_math = (
            r"$\mathbf{Truth\ about\ Memory\ Weights:}$" + "\n" +
            r"$\bullet$ $\text{RNN: } \partial h_t / \partial h_{t-k} \propto e^{-k} \to \text{Forgets}$" + "\n" +
            r"$\bullet$ $\text{HiPPO-LegT: Uniform window }[t-T, t]$" + "\n" +
            r"$\bullet$ $\text{HiPPO-LegS: Full }[0, t]\text{, scaled by } 1/t$"
    )
    ax.text(0.40, 7.5, comparison_math, fontsize=9, color='#1e293b',
            bbox=dict(facecolor='#f8fafc', edgecolor='#cbd5e1', boxstyle='round,pad=0.6'))

    ax.legend(loc='upper right', fontsize=9, frameon=True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(0, 1.25)
    ax.grid(axis='x', linestyle='--', alpha=0.4)


def draw_hippo_reconstruction(ax):
    """Draw Right Plot: HiPPO Signal Reconstruction Result"""
    t = np.linspace(0, 1, 600)
    signal = np.sin(2 * np.pi * t) + 0.5 * np.cos(10 * np.pi * t) + 0.3 * np.sin(20 * np.pi * t)

    ax.plot(t, signal, color='#1e293b', linestyle='--', label="Target $u(\\tau)$", linewidth=1.2, alpha=0.6)

    ns = [2, 12]
    colors = ['#ef4444', '#2563eb']
    labels = ["$N=2$ (Low Precision)", "$N=12$ (High Precision)"]

    from numpy.polynomial.legendre import Legendre
    x_map = 2 * t - 1  # Map [0, 1] to [-1, 1] for proper Legendre fitting

    for n, color, label in zip(ns, colors, labels):
        # Use theoretically correct Legendre orthogonal projection
        leg_fit = Legendre.fit(x_map, signal, n)
        reconstruction = leg_fit(x_map)
        ax.plot(t, reconstruction, color=color, label=label, linewidth=2.2)

    ax.set_title("HiPPO Reconstruction Performance", loc='center', pad=20, fontsize=13, fontweight='bold',
                 color='#1e40af')
    ax.set_xlabel("Continuous History $\\tau \in [0, t]$", fontsize=10)
    ax.set_ylabel("Signal Amplitude", fontsize=10)

    math_box = (
            r"$\dot{c}(t) = Ac(t) + Bu(t)$" + "\n" +
            r"$\text{Coefficients } c(t) \text{ capture entire history}$" + "\n" +
            r"$\|u - \hat{u}_N\|^2 \to 0 \text{ with uniform precision}$"
    )
    ax.text(0.05, 1.25, math_box, color='#1e40af', fontsize=9,
            bbox=dict(facecolor='#eff6ff', edgecolor='#bfdbfe', boxstyle='round,pad=0.5'))

    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xticklabels(['Start (0)', 'Mid ($t/2$)', 'Now ($t$)'])
    ax.legend(loc='upper right', fontsize=9, frameon=True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(-1.6, 2.4)


# Create 2-panel figure for side-by-side logic and result comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7), dpi=100)
plt.subplots_adjust(wspace=0.25, bottom=0.15)

draw_mechanism_comparison(ax1)
draw_hippo_reconstruction(ax2)

plt.tight_layout(pad=4.0)
plt.show()