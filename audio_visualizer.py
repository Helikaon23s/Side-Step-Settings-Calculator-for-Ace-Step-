import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk

def launch_live_analytics_plot(base_lr, f1_power, f2_power, target_epochs, sim_percent, log_path, parse_log_func):
    """
    Spawns custom visualizer overlay to compare ideal metrics curves against actual metrics.
    """
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(11, 6))
    ax2 = ax.twinx()
    
    epochs_range = np.linspace(1, target_epochs, 250)
    curve_1 = base_lr * (np.cos((epochs_range / target_epochs)**f1_power * np.pi) * 0.5 + 0.5)
    curve_2 = base_lr * (np.cos((epochs_range / target_epochs)**f2_power * np.pi) * 0.5 + 0.5)
    
    ax.plot(epochs_range, curve_1, label='Option 1: Texture Refiner', color='#00ffcc', linestyle='--', alpha=0.7)
    ax.plot(epochs_range, curve_2, label='Option 2: Anti-Fraction Curve', color='#ff007f', linewidth=2)
    ax.set_xlabel('Training Epoch Horizon Path')
    ax.set_ylabel('Learning Rate Scale Profile', color='#ff007f')
    ax.tick_params(axis='y', labelcolor='#ff007f')
    
    plot_state = {'log_path': log_path}
    
    def update_plot_metrics():
        ep, loss, ma5 = parse_log_func(plot_state['log_path'])
        if ep and loss:
            ax2.clear()
            ax2.plot(ep, loss, color='#ffffff', alpha=0.25, label='Raw Step Loss')
            ax2.plot(ep, ma5, color='#ffff00', linewidth=2.5, label='MA5 Convergence Trend')
            ax2.set_ylabel('Real-World Convergence Loss Engine', color='#ffff00')
            ax2.tick_params(axis='y', labelcolor='#ffff00')
            
            lines_1, labels_1 = ax.get_legend_handles_labels()
            lines_2, labels_2 = ax2.get_legend_handles_labels()
            ax.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
            fig.canvas.draw_idle()

    if log_path:
        try: update_plot_metrics()
        except Exception: pass
    else:
        ax.legend(loc='upper right')
        
    ax.set_title(f"Adaptive Training Framework Engine vs Real-World Convergence Trends")
    plt.grid(True, color='#222222')
    plt.tight_layout()
    plt.show()