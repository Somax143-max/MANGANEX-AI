import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path
import os

OUT_DIR = Path(r"D:\2nd move from os\d\MANGANEX_AI_SIHPOLISH\ppt_assets")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Slide 2 Visual: System Workflow Architecture Badge
def create_slide2_diagram():
    fig, ax = plt.subplots(figsize=(6, 3.2), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')
    
    # 4 Steps Horizontal Flow
    steps = [
        ("🛰️ Space Tech\nSentinel-2 MSI\nSWIR / LST", "#0284C7"),
        ("⛰️ Host Geology\nSausar / Gondite\nSRTM DEM", "#1E293B"),
        ("🤖 AI Engine\nRandom Forest\nPotential + Shortfall", "#D97706"),
        ("📊 Decision GIS\n3D Heatmap\nAction Matrix", "#059669"),
    ]
    
    for i, (text, col) in enumerate(steps):
        x = 0.05 + i * 0.24
        # Box
        rect = patches.FancyBboxPatch(
            (x, 0.18), 0.20, 0.65,
            boxstyle="round,pad=0.03,rounding_size=0.04",
            facecolor=col, edgecolor='none', alpha=0.95
        )
        ax.add_patch(rect)
        ax.text(x + 0.10, 0.50, text, ha='center', va='center', color='white',
                fontsize=8.5, fontweight='bold', family='sans-serif', multialignment='center')
        
        # Arrow
        if i < 3:
            ax.annotate("", xy=(x + 0.235, 0.50), xytext=(x + 0.205, 0.50),
                        arrowprops=dict(arrowstyle="-|>", color="#0284C7", lw=2.2, mutation_scale=12))
            
    plt.tight_layout()
    fig.savefig(OUT_DIR / "workflow_diag.png", bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
    plt.close()
    print("Created workflow_diag.png")

# 2. Slide 3 Visual: Technical Approach Tech Stack Architecture
def create_slide3_diagram():
    fig, ax = plt.subplots(figsize=(5.5, 3.0), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')
    
    layers = [
        ("Layer 1: Space Earth Observation (Sentinel-2 + Landsat + DEM)", "#0284C7"),
        ("Layer 2: AI Feature Extraction (Ferrous, Clay, NDVI, Thermal)", "#1E293B"),
        ("Layer 3: Multi-Model RF Inference (Potential, Shortfall, Risk)", "#D97706"),
        ("Layer 4: 3D PyDeck GIS & Executive Decision Dashboard", "#059669"),
    ]
    
    for i, (label, color) in enumerate(layers):
        y = 0.78 - i * 0.24
        rect = patches.FancyBboxPatch(
            (0.02, y), 0.96, 0.18,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor=color, edgecolor='none', alpha=0.92
        )
        ax.add_patch(rect)
        ax.text(0.50, y + 0.09, label, ha='center', va='center', color='white',
                fontsize=8.5, fontweight='bold', family='sans-serif')
        
    plt.tight_layout()
    fig.savefig(OUT_DIR / "tech_layers.png", bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
    plt.close()
    print("Created tech_layers.png")

# 3. Slide 5 Visual: Quantitative Impact Metrics
def create_slide5_diagram():
    fig, ax = plt.subplots(figsize=(5.5, 2.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')
    
    kpis = [
        ("> 60%", "Faster Turnaround", "#0284C7"),
        ("3-6 Mo", "Shortfall Early Warning", "#D97706"),
        ("97.5%", "Risk Accuracy", "#059669"),
        ("592", "Mining Clusters", "#7C3AED"),
    ]
    
    for i, (val, label, col) in enumerate(kpis):
        x = 0.03 + i * 0.245
        rect = patches.FancyBboxPatch(
            (x, 0.10), 0.22, 0.80,
            boxstyle="round,pad=0.03,rounding_size=0.04",
            facecolor='#FFFFFF', edgecolor=col, linewidth=2.0
        )
        ax.add_patch(rect)
        ax.text(x + 0.11, 0.62, val, ha='center', va='center', color=col,
                fontsize=15, fontweight='bold', family='sans-serif')
        ax.text(x + 0.11, 0.30, label, ha='center', va='center', color='#1E293B',
                fontsize=7.5, fontweight='bold', family='sans-serif', multialignment='center')
        
    plt.tight_layout()
    fig.savefig(OUT_DIR / "impact_kpis.png", bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
    plt.close()
    print("Created impact_kpis.png")

if __name__ == "__main__":
    create_slide2_diagram()
    create_slide3_diagram()
    create_slide5_diagram()
