# educational_matrices.py

def print_optimizer_matrix_menu(dev_mode=False):
    """
    Prints the educational pros, cons, and implementation menu for optimizers.
    If dev_mode is False, experimental options (3-6) are hidden entirely.
    """
    print("\n" + "="*85)
    print("OPTIMIZER SELECTION ARCHITECTURE: PROS, CONS & IMPLEMENTATION MATRIX")
    print("="*85)
    print("1. AdamW [Standard Baseline]")
    print("   -> Pros: Bulletproof stability; predictable; universally compatible; low compute overhead.")
    print("   -> Cons: Lacks second-order curvature tracking; can stall out on complex multi-singer textures.")
    print("   -> Best For: Standard baseline runs, limited-size vocal samples, or debugging configurations.")
    print("-" * 85)
    print("2. Adafactor [Memory-Optimized Scaling]")
    print("   -> Pros: Massive VRAM savings by factoring state matrices; sub-linear memory footprint.")
    print("   -> Cons: Can exhibit sudden convergence instability or jagged step tracking on unchunked data.")
    print("   -> Best For: Large datasets or high-rank/alpha constraints running on tight VRAM limitations (<16GB).")
    
    # Hide everything else if not in developer mode
    if not dev_mode:
        print("="*85)
        return

    print("-" * 85)
    print("3. SOAP [Second-Order Preconditioned Eigenbasis] (DEV ONLY)")
    print("   -> Pros: Incredible convergence speed; ultra-precise alignment of deep structural text prompts.")
    print("   -> Cons: Huge VRAM consumption; periodic preconditioning cycles add brief computational overhead.")
    print("   -> Best For: Premium studio high-fidelity training where capturing flawless frequency response is critical.")
    print("-" * 85)
    print("4. SCAO [Self-Correcting Adaptive Optimization] (DEV ONLY)")
    print("   -> Pros: Automates internal learning velocity tracking; strong resistance against clipping and artifacts.")
    print("   -> Cons: Slow initialization; requires continuous native tracking metrics.")
    print("   -> Best For: Highly dynamic or chaotic raw recordings with varied background environments.")
    print("-" * 85)
    print("5. C-AdamW [Cautious AdamW] (DEV ONLY)")
    print("   -> Pros: Enforces strict gradient directional consensus; completely filters out chaotic high-heat spikes.")
    print("   -> Cons: Slightly slower structural pickup during the initial phase; requires precise initial alignment.")
    print("   -> Best For: Eradicating high-frequency metallic artifacts and harsh, bright sibilance defects.")
    print("-" * 85)
    print("6. C-Lion [Cautious Lion] (DEV ONLY)")
    print("   -> Pros: Ultra-efficient sign-based updates optimized for raw throughput speed; high textural clarity.")
    print("   -> Cons: High sensitivity to learning rate values; can easily result in model collapse if over-driven.")
    print("   -> Best For: Fast experimental training passes or sweeping massive raw instrument/backing tracks.")
    print("="*85)