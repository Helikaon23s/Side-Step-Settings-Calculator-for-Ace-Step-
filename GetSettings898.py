import os
import math
import re
import csv
import ctypes
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk

# Link to external DSP module
import audio_analyzer 

def calculate_adjusted_lr(base_lr, rank, alpha, is_lokr):
    """Encapsulates scaling logic to keep the main script clean."""
    if is_lokr or rank <= 0:
        return base_lr
    
    scaling_ratio = alpha / rank
    if scaling_ratio == 1.0:
        return base_lr
    
    # Apply adjustment factor
    adjustment = (1.0 / scaling_ratio) if scaling_ratio < 1.0 else (1.0 / (scaling_ratio * 0.85))
    return base_lr * adjustment

def get_automated_vram():
    """Queries NVIDIA Management Library (NVML) or PyTorch directly for real hardware VRAM."""
    try:
        nvml = None
        for lib in ["nvml.dll", "libnvidia-ml.so", "nvcuvid.dll"]:
            try:
                nvml = ctypes.CDLL(lib)
                break
            except Exception: continue
        if nvml:
            nvml.nvmlInit()
            device = ctypes.c_void_p()
            nvml.nvmlDeviceGetHandleByIndex(0, ctypes.byref(device))
            class struct_nvmlMemory_t(ctypes.Structure):
                _fields_ = [("total", ctypes.c_ulonglong), ("free", ctypes.c_ulonglong), ("used", ctypes.c_ulonglong)]
            mem_info = struct_nvmlMemory_t()
            nvml.nvmlDeviceGetMemoryInfo(device, ctypes.byref(mem_info))
            nvml.nvmlShutdown()
            detected = round(mem_info.total / (1024**3))
            print(f"[+] AUTOMATED HARDWARE SCAN: Successfully mapped primary GPU. Detected {detected}GB Dedicated VRAM.")
            return detected
    except Exception: pass
    try:
        import torch
        if torch.cuda.is_available():
            detected = round(torch.cuda.get_device_properties(0).total_memory / (1024**3))
            print(f"[+] AUTOMATED PYTORCH SCAN: Detected {detected}GB Dedicated VRAM.")
            return detected
    except Exception: pass
    print("[i] Hardware Scan Note: Native hooks unavailable.")
    try: return int(input(" -> Enter Available Dedicated VRAM manually (GB, default 24): ") or 24)
    except ValueError: return 24

def parse_training_log(log_path):
    """Parses training logs to extract step/epoch error metrics and generates an MA5 curve."""
    if not log_path or not os.path.exists(log_path): return None, None, None
    epochs, losses, ma5_values = [], [], []
    try:
        if log_path.lower().endswith('.csv'):
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header:
                    epoch_idx, loss_idx = -1, -1
                    for i, h in enumerate(header):
                        h_low = h.lower().strip()
                        if 'epoch' in h_low or 'step' in h_low: epoch_idx = i
                        elif 'loss' in h_low: loss_idx = i
                    if epoch_idx != -1 and loss_idx != -1:
                        for row in reader:
                            if len(row) > max(epoch_idx, loss_idx):
                                try:
                                    epochs.append(float(row[epoch_idx]))
                                    losses.append(float(row[loss_idx]))
                                except ValueError: continue
            if epochs and losses:
                for idx in range(len(losses)):
                    start_idx = max(0, idx - 4)
                    ma5_values.append(np.mean(losses[start_idx:idx + 1]))
                return epochs, losses, ma5_values
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                epoch_match = re.search(r'\b(ep|epoch)[:\s]*([0-9.]+)', line, re.IGNORECASE)
                loss_match = re.search(r'\bloss[:\s]*([0-9.]+)', line, re.IGNORECASE)
                if epoch_match and loss_match:
                    try:
                        epochs.append(float(epoch_match.group(2)))
                        losses.append(float(loss_match.group(1)))
                    except ValueError: continue
        if epochs and losses:
            combined = sorted(zip(epochs, losses))
            epochs, losses = zip(*combined)
            epochs, losses = list(epochs), list(losses)
            for idx in range(len(losses)):
                start_idx = max(0, idx - 4)
                ma5_values.append(np.mean(losses[start_idx:idx + 1]))
            return epochs, losses, ma5_values
    except Exception as e: print(f" [!] Non-critical log parse error: {e}")
    return None, None, None

def generate_smart_plan():
    print("="*85)
    print("ACE-STEP COMMAND CENTER: CONTINUOUS GRADIENT MATRIX ENGINE V2.50 (256-CAP)")
    print("="*85)

    print("\nSelect Operation Framework Interface:")
    print("  1. Standard User Mode (Safe Defaults)")
    print("  2. Developer Diagnostics Mode (Advanced Overrides)")
    try: mode_choice = int(input("Enter choice (1 or 2): ") or 1)
    except ValueError: mode_choice = 1
    dev_mode = (mode_choice == 2)

    print("\nSelect target network model format:\n  1. Standard LoRA\n  2. LoKRs")
    try: net_choice = int(input("Enter choice (1 or 2): ") or 1)
    except ValueError: net_choice = 1
    is_lokr = (net_choice == 2)

    print("\nSelect Training Objectives Mode:\n  1. Standard Baseline\n  2. Diagnostic Redo\n  3. Custom Matrix Override")
    try: mode = int(input("Enter choice (1, 2, or 3): ") or 1)
    except ValueError: mode = 1

    vram_gb = get_automated_vram()

    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Training Dataset Folder")
    if not folder_path: 
        print("[CRITICAL] Folder selection canceled. Aborting.")
        root.destroy()
        return

    log_path = ""
    if dev_mode:
        log_path = filedialog.askopenfilename(title="Select Runtime Training Log File (Diagnostic Mode)", filetypes=[("Log Files", "*.csv *.txt *.log"), ("All Files", "*.*")])
    
    root.destroy()
    
    audit_res = audio_analyzer.audit_audio_files(folder_path)
    raw_files = audit_res[0] if isinstance(audit_res, tuple) else audit_res
    
    if len(raw_files) == 0: 
        print("\n[!] Technical breakdown: No valid training materials present.")
        return

    files = []
    total_duration = 0.0
    dropped_tails = 0

    for f in raw_files:
        try:
            dur = audio_analyzer.get_duration(f) if hasattr(audio_analyzer, 'get_duration') else (audit_res[1] / len(raw_files) if isinstance(audit_res, tuple) else 30.0)
        except Exception:
            dur = (audit_res[1] / len(raw_files) if isinstance(audit_res, tuple) else 30.0)
            
        if dur >= 15.0:
            files.append(f)
            total_duration += dur
        else:
            dropped_tails += 1

    num_tracks = len(files)
    if num_tracks == 0:
        print("\n[!] Technical breakdown: Math context cleared. No files survived the 15s tail filter.")
        return
    if dropped_tails > 0:
        print(f"[i] Filter Matrix: Isolated and dropped {dropped_tails} short tail chunk(s) under 15s from system calculations.")

    target_chunk_len = 30.0
    avg_track_len = total_duration / num_tracks

    if avg_track_len <= 65.0:
        num_samples = num_tracks
        dataset_repeats = 1
        print(f"[i] Automated Dataset Scan: Pre-Chunked Slices Detected (Avg Length: {avg_track_len:.1f}s).\n    >> Repeats locked to 1.")
    else:
        virtual_chunks_needed = math.ceil(total_duration / target_chunk_len)
        dataset_repeats = max(1, math.ceil(virtual_chunks_needed / num_tracks))
        num_samples = num_tracks
        print(f"[i] Automated Dataset Scan: Raw/Continuous Tracks Detected (Avg Length: {avg_track_len:.1f}s).\n    >> Dynamic Balancing Multiplier: {dataset_repeats} Repeats.\n    >> Total Virtual Chunks: {num_tracks * dataset_repeats}")

    val_reasons = []
    use_val = input("\nWill you be utilizing a validation holdout set for this run? (y/n): ").lower() == 'y'
    val_pct = 0.0
    if use_val:
        try: val_pct = float(input("Enter validation set percentage (1-50%, default is 10): ") or 10)
        except ValueError: val_pct = 10.0
        val_pct = max(1.0, min(50.0, val_pct))
        val_multiplier = 1.0 - (val_pct / 100.0)
        raw_virtual_total = num_samples * dataset_repeats
        effective_total_dataset_size = raw_virtual_total * val_multiplier
        val_chunks_count = raw_virtual_total - effective_total_dataset_size
        val_reasons.append(f"Validation Holdout Active: {val_pct}% allocated away from training data steps.")
        val_reasons.append(f"   -> Training Pool: {effective_total_dataset_size:.2f} virtual chunks.")
        val_reasons.append(f"   -> Validation Pool: {val_chunks_count:.2f} virtual chunks.")
    else:
        effective_total_dataset_size = num_samples * dataset_repeats

    try: num_singers = int(input("\nEnter number of unique singers/concepts (default 1): ") or 1)
    except ValueError: num_singers = 1
    num_singers = max(1, num_singers)

    is_turbo = input("Using a TURBO model? (y/n): ").lower() == 'y'

    print("\n" + "="*85)
    print("ADVANCED OPTIMIZER SELECTION ARCHITECTURE: PROS, CONS & IMPLEMENTATION MATRIX")
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
    
    if dev_mode:
        print("-" * 85)
        print("3. SOAP [Second-Order Preconditioned Eigenbasis]")
        print("   -> Pros: Incredible convergence speed; ultra-precise alignment of deep structural text prompts.")
        print("   -> Cons: Huge VRAM consumption; periodic preconditioning cycles add brief computational overhead.")
        print("   -> Best For: Premium studio high-fidelity training where capturing flawless frequency response is critical.")
        print("-" * 85)
        print("4. SCAO [Self-Correcting Adaptive Optimization]")
        print("   -> Pros: Automates internal learning velocity tracking; strong resistance against clipping and artifacts.")
        print("   -> Cons: Slow initialization; requires continuous native tracking metrics.")
        print("   -> Best For: Highly dynamic or chaotic raw recordings with varied background environments.")
        print("-" * 85)
        print("5. C-AdamW [Cautious AdamW]")
        print("   -> Pros: Enforces strict gradient directional consensus; completely filters out chaotic high-heat spikes.")
        print("   -> Cons: Slightly slower structural pickup during the initial phase; requires precise initial alignment.")
        print("   -> Best For: Eradicating high-frequency metallic artifacts and harsh, bright sibilance defects.")
        print("-" * 85)
        print("6. C-Lion [Cautious Lion]")
        print("   -> Pros: Ultra-efficient sign-based updates optimized for raw throughput speed; high textural clarity.")
        print("   -> Cons: High sensitivity to learning rate values; can easily result in model collapse if over-driven.")
        print("   -> Best For: Fast experimental training passes or sweeping massive raw instrument/backing tracks.")
    print("="*85)
    
    try:
        if dev_mode:
            opt_choice = int(input("Select Optimizer (1-6, default 1): ") or 1)
        else:
            opt_choice = int(input("Select Optimizer (1-2, default 1): ") or 1)
            if opt_choice not in [1, 2]: opt_choice = 1
    except ValueError: opt_choice = 1
    
    opt_map = {1: "AdamW", 2: "Adafactor", 3: "SOAP", 4: "SCAO", 5: "C-AdamW", 6: "C-Lion"}
    opt_type = opt_map.get(opt_choice, "AdamW")

    b_std, c_std, sim_percent, mean_centroid, quality_score, quality_tier = audio_analyzer.analyze_similarity_and_quality(files, target_chunk_len)

    print(f"\n" + "="*85)
    print("AUDIO SPECTRUM READOUTS & ADAPTATION VECTOR DETAILS:")
    print("="*85)
    print(f"[-] STABILIZED BPM STANDARD DEVIATION: {b_std:.2f}")
    print(f"[-] SPECTRAL CENTROID VARIANCE:       {c_std:.4f}")
    print(f"[-] MEAN SPECTRAL CENTROID:           {mean_centroid:.1f} Hz")
    print(f"[-] ALBUM STYLE COHESION SCORE:       {sim_percent:.1f}%")
    print(f"[-] AUDIO QUALITY RATING SCORE:       {quality_score:.1f}% -> Tier: {quality_tier}")
    print("="*85)

    # --- CONTINUOUS SPECTRAL GRADIENT ENGINE ---
    min_rank, max_rank = 32, 256
    rank_sensitivity = 400.0 
    calculated_rank = min_rank + (c_std * rank_sensitivity)
    rank = int(round(max(min_rank, min(max_rank, calculated_rank)) / 8) * 8)
    alpha = rank 
    rank_strategy = "Continuous Spectral Gradient Engine (Adaptive Expansion)"
    rank_reason = f"Rank/Alpha dynamically mapped to c_std: {c_std:.4f} -> {rank}/{alpha}."
    
    if mode == 3:
        print("\n" + "-"*40 + " CUSTOM MATRIX SETTINGS " + "-"*40)
        try:
            custom_rank = int(input("Enter Custom Rank/Dimension (default 32): ") or 32)
            custom_alpha = int(input("Enter Custom Network Alpha (default 32): ") or 32)
        except ValueError: custom_rank, custom_alpha = 32, 32
        rank, alpha = custom_rank, custom_alpha
        rank_strategy = f"Manual Override Matrix Configuration ({rank}/{alpha})"
        rank_reason = f"User defined constraints enforced. Multiplier Ratio: {alpha/rank:.2f}x."

    trouble_reasons, lr_modifier, epoch_modifier, exponent_modifier = [], 1.0, 0, 0.0
    force_rank_upgrade = False

    if mode == 2:
        print("\n" + "="*85)
        print("                 AUDIO DIAGNOSTIC AND FLAW TROUBLESHOOTING MATRIX")
        print("="*85)
        print("Select known issues:\n  [1] Metallic Artifacts  [2] Severe Sibilance  [3] Muddy Backing Tracks\n  [4] Prompt Paralysis   [5] Vocal Meltdown    [6] Low Presence")
        issues_input = input("\nEnter choices separated by commas (e.g., 1,2): ")
        issues_selected = [int(x.strip()) for x in re.split(r'[,\s]+', issues_input) if x.strip().isdigit()]
        
        if 1 in issues_selected:
            lr_modifier *= 0.65; exponent_modifier += 0.15
            trouble_reasons.append("Metallic Artifacts Mitigation: Dropped LR 35%, accelerated cooling timeline.")
        if 2 in issues_selected:
            lr_modifier *= 0.75; epoch_modifier += 15
            trouble_reasons.append("Sibilance Reduction Configuration: Lowered base LR 25%, padded runway +15 epochs.")
        if 3 in issues_selected:
            exponent_modifier -= 0.18; epoch_modifier += 25; force_rank_upgrade = True
            trouble_reasons.append("Instrumental Reconstruction Injection: Added +25 epochs, sustained energy path.")
        if 4 in issues_selected:
            if alpha > (rank // 2): alpha = max(1, rank // 2)
            lr_modifier *= 0.85
            trouble_reasons.append("Prompt Paralysis Counter-Balance: Reduced Alpha to limit attention momentum.")
        if 5 in issues_selected:
            lr_modifier *= 0.50; epoch_modifier -= 20
            trouble_reasons.append("Vocal Meltdown Prevention: Cut LR in half, trimmed runway by -20 epochs.")
        if 6 in issues_selected:
            lr_modifier *= 1.35; epoch_modifier += 15; force_rank_upgrade = True
            trouble_reasons.append("Presence & Tone Boost Matrix: Accelerated learning 35%, deepened matrix boundaries.")
        if force_rank_upgrade and rank < 64:
            rank, alpha = 64, 64
            rank_strategy = "Diagnostic Enforced High Capacity Matrix (64/64 Override)"

    if is_lokr:
        lokr_factor = 4 if num_singers < 3 else 2
        lora_crn_specs = f"network_module='lycoris.koala' | lora_crn_dim=10000 | lora_crn_alpha=1 | factor={lokr_factor}"
        rank_strategy = f"LoKRs Matrix Engine Enabled (Factor={lokr_factor})"
        rank_reason = lora_crn_specs

# --- UNIFIED CONTINUOUS QUALITY GRADIENT ---
    q_norm = max(0.0, min(100.0, quality_score)) / 100.0
    
    # LR Gradient: Smooths from 0.50x (at 0 quality) to 1.15x (at 100 quality)
    lr_gradient = 0.5 + (q_norm * 0.65)
    
    # Exponent Gradient: Smooths from +0.25 (at 0 quality) to -0.05 (at 100 quality)
    exponent_gradient = 0.25 - (q_norm * 0.30)
    
    # Epoch Gradient: Truncates from -12 epochs (at 0 quality) to 0 (at 100 quality)
    epoch_gradient = -int((1.0 - q_norm) * 12)

    lr_modifier *= lr_gradient
    exponent_modifier += exponent_gradient
    epoch_modifier += epoch_gradient

    quality_reasons = [
        f"Continuous Gradient Modification Summary:",
        f"   -> Quality Learning Rate Step Scalar:  {lr_gradient:.3f}x",
        f"   -> Exponential Curvature Tuning Bias: {exponent_gradient:+.3f}",
        f"   -> Timeline Horizon Truncation:       {epoch_gradient:+d} epochs"
    ]

    base_epoch_ceiling = 140
    similarity_reduction = (sim_percent / 100.0) * 50.0
    singer_expansion = (num_singers - 1) * 15.0
    centroid_factor = max(0.0, min(1.0, (mean_centroid - 2500.0) / 1000.0))
    std_factor = max(0.0, min(1.0, (0.35 - c_std) / 0.15))
    vintage_boost = 35.0 * (centroid_factor * std_factor)
    
    calculated_ideal_epochs = int(base_epoch_ceiling - similarity_reduction + singer_expansion + vintage_boost) + epoch_modifier
    dynamic_target_epochs = max(55, min(220, calculated_ideal_epochs))

    calculated_warmup_pct = max(4.0, min(11.0, 11.0 - (sim_percent / 10.0)))
    step_comp = 1 + (calculated_warmup_pct / 100)

    min_chunks, max_chunks = 5.0, 30.0
    min_target_steps, max_target_steps = 1500.0, 2800.0
    
    chunk_factor = (effective_total_dataset_size - min_chunks) / (max_chunks - min_chunks)
    clamped_factor = max(0.0, min(1.0, chunk_factor))
    ideal_target_steps = min_target_steps + (max_target_steps - min_target_steps) * clamped_factor
    
    if is_turbo: ideal_target_steps *= 0.7

    base_lr = (0.0001 if is_turbo else 0.0003) * lr_modifier
    if is_lokr: base_lr *= 1.45

    if opt_type == "C-Lion": base_lr *= 0.35 
    elif opt_type == "SOAP": base_lr *= 1.15 

    # APPLY UNIVERSAL SCALING
    base_lr = calculate_adjusted_lr(base_lr, rank, alpha, is_lokr)

    opt_args = ""
    if opt_type == "AdamW": opt_args = "'weight_decay=0.005'"
    elif opt_type == "Adafactor": opt_args = "'scale_parameter=False', 'relative_step=False', 'warmup_init=False'"
    elif opt_type == "SOAP":
        opt_args = "'weight_decay=0.01', 'precondition_freq=10', 'decouple=True'"
        if vram_gb < 24: print(f"\n[WARNING] SOAP requires 24GB VRAM. (Detected {vram_gb}GB). Risks OOM error.")
    elif opt_type == "SCAO":
        opt_args = "'weight_decay=0.01', 'adaptive_rank=True', 'quantize_int8=True'"
        if vram_gb < 16: print(f"\n[WARNING] SCAO state tracking requires 16GB VRAM. (Detected {vram_gb}GB).")
    elif opt_type == "C-AdamW": opt_args = "'weight_decay=0.01', 'caution=True'"
    elif opt_type == "C-Lion": opt_args = "'weight_decay=0.05', 'caution=True', 'betas=(0.9,0.99)'"

    precision_mode = "bfloat16"
    if vram_gb <= 12: 
        topologies = {"Option 1 [SAFE PERFORMANCE HEADROOM]": (1, 4), "Option 2 [ON THE EDGE OPTIMIZATION]": (2, 2)}
        precision_mode = "fp16 --mixed_precision"
    elif vram_gb <= 16: 
        topologies = {"Option 1 [SAFE PERFORMANCE HEADROOM]": (2, 2), "Option 2 [ON THE EDGE OPTIMIZATION]": (4, 1)}
        precision_mode = "bf16 --mixed_precision"
    elif vram_gb <= 24: 
        topologies = {"Option A [SAFE BALANCED PROFILE]": (4, 1), "Option B [MAX PERFORMANCE ACCELERATION]": (8, 1)}
        precision_mode = "bf16 --full_bf16_precision"
    else: 
        topologies = {"Option 1 [THROUGHPUT BANDWIDTH MAX]": (16, 1), "Option 2 [ULTRA STAGE COMPLETION ENGINE]": (32, 1)}
        precision_mode = "bf16 --full_bf16_precision --pure_bf16"

    print(f"\n[DEBUG] FINAL PARAMETER CHECK: Rank={rank}, Alpha={alpha} | Mode={mode}")
    
    print("\n" + "="*85)
    print(f"REQUIRED TRAINER SETUP PARAMETERS (ALGO: {'LoKRs' if is_lokr else 'LoRA'} | MODE {mode})")
    print("="*85)
    print(f">> LEARNING RATE:       {base_lr:.6f}")
    print(f">> OPTIMIZER TYPE:      {opt_type}")
    print(f">> DETECTED VRAM SCALE: {vram_gb}GB Available")
    print(f">> TARGET PRECISION:    {precision_mode.upper()}")
    if opt_args: print(f">> OPTIMIZER ARGS:      {opt_args}")
    if is_lokr: print(f">> LOKR CONFIGS:        {lora_crn_specs}")
    else: print(f">> RANK / DIMENSION:    {rank}  |  NETWORK ALPHA: {alpha}")
    print(f"   Optimization Matrix: {rank_strategy}\n   Reasoning:           {rank_reason}\n" + "-"*85)
    
    for name, (b, a) in topologies.items():
        total_effective_files = effective_total_dataset_size
        batches_per_epoch = math.ceil(total_effective_files / b)
        steps_per_epoch = math.ceil(batches_per_epoch / a)
        target_steps_with_warmup = ideal_target_steps * step_comp
        suggested_epochs = math.ceil(target_steps_with_warmup / steps_per_epoch)
        
        final_epochs = max(55, min(220, suggested_epochs)) if not use_val else dynamic_target_epochs
        total_steps = steps_per_epoch * final_epochs
        warmup = int(total_steps * (calculated_warmup_pct / 100))
        
        print(f"\n{name}:\n   -> DATASET REPEATS:  {dataset_repeats}\n   -> BATCH SIZE:       {b}\n   -> GRAD ACCUM:       {a} (Effective: {b*a})\n   -> MAX TRAIN EPOCHS: {final_epochs}\n   -> STEPS PER EPOCH:  {steps_per_epoch}\n   -> TOTAL RUN STEPS:  {total_steps}\n   -> WARMUP STEPS:     {warmup} ({calculated_warmup_pct:.1f}%)")

    base_power_anchor = 0.75
    calculated_power = base_power_anchor + (0.25 * (num_singers - 1)) - ((sim_percent / 100.0) * 0.35) + exponent_modifier
    f1_power = 0.50 
    f2_power = max(0.30, min(1.80, round(calculated_power, 2)))

    print("\n" + "="*85)
    print("DYNAMIC CURVATURE PROFILE: CORE ROOT FORMULA ANALYSIS & USAGE CONTEXT")
    print("="*85)
    print("DESCRIPTION & STRATEGIC APPLICATION:")
    print(" * TEXTURE REFINER (Option 1): Uses a static square-root progression profile (0.50 power).")
    print("   Enforces prolonged sustained energy across mid-epochs to firmly lock in fine audio artifacts.")
    print(" * ANTI-FRACTION ENGINE (Option 2): Calculates a dynamically scaled geometric boundary exponent.")
    print("   Prevents micro-fractional model divergence and early collapse when processing multi-singer concept fields.")
    print("-"*85)
    print(f"[OPTION 1: THE ACCENTUATED TEXTURE REFINER]\n   Formula:    base_lr * (cos(progress**{f1_power:.2f} * 3.1415) * 0.5 + 0.5)")
    print(f"\n[OPTION 2: THE ADAPTIVE ANTI-FRACTION CONCEPT CURVE]\n   Formula:    base_lr * (cos(progress**{f2_power:.2f} * 3.1415) * 0.5 + 0.5)\n" + "="*85)

    phase_1_boundary = max(1.0, min(dynamic_target_epochs * 0.40, dynamic_target_epochs * ((calculated_warmup_pct / 100.0) * 2.2)))
    phase_2_boundary = max(phase_1_boundary + 5.0, min(dynamic_target_epochs * 0.92, dynamic_target_epochs * (0.65 + (sim_percent / 300.0))))
    goldi_entry = max(phase_1_boundary + 1, min(dynamic_target_epochs * 0.50, phase_1_boundary * 1.15))
    goldi_exit = max(goldi_entry + 5.0, min(phase_2_boundary - 2.0, phase_2_boundary * (0.82 + (sim_percent / 500.0))))

    print("\n" + "="*85 + f"\nCRITICAL TARGET WINDOW: HIGHEST GENERALIZATION PROBABILITY\n" + "="*85)
    print(f">> CONVERGENCE SWEET SPOT: Epoch {int(goldi_entry)} to Epoch {int(goldi_exit)}\n" + "="*85)
    
    if val_reasons:
        print("\nVALIDATION ENGINE CONFIGURATION MATRIX:\n" + "-" * 85)
        for v_reason in val_reasons: print(f" * {v_reason}")
        print("-" * 85)

    if quality_reasons:
        print("\nDATASET QUALITY ADAPTATION MATRIX LOG:\n" + "-" * 85)
        for q_reason in quality_reasons: print(f" * {q_reason}")
        print("-" * 85)

    if mode == 2 and trouble_reasons:
        print("\nDIAGNOSTIC ADJUSTMENT LOG & REPORT SUMMARY:\n" + "-" * 85)
        for reason in trouble_reasons: print(f" * {reason}\n")
        print("-" * 85)
    elif mode == 3 and not is_lokr:
        print("\nMANUAL MATRIX ADJUSTMENT REPORT:\n" + "-" * 85)
        if alpha > rank: print(f" * Attention: Alpha > Rank. Engine scaled down base learning rate to prevent audio clipping.")
        elif alpha < rank: print(f" * Attention: Alpha < Rank. Engine boosted learning velocity to maintain momentum.")
        else: print(f" * Matrix running in 1:1 Unity ({rank}/{alpha}). Learning rate flows cleanly.")
        print("-" * 85)
    elif is_lokr:
        print("\nLOKR CONFIGURATION LOGS:\n" + "-" * 85 + f"\n * Kronecker layers require separate convergence steps. Base LR boosted 1.45x.\n * Dimension locked to 10000. Set your GUI setup package to 'lokr'.\n" + "-" * 85)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6.5))
    p = np.linspace(0, 1, 100)
    chart_lr = base_lr
    ax.plot(p * dynamic_target_epochs, (np.cos(p**f1_power * np.pi)*0.5+0.5)*chart_lr, label='Opt 1: Texture Control (0.50)', color='#00ffff', linewidth=2.5)
    ax.plot(p * dynamic_target_epochs, (np.cos(p**f2_power * np.pi)*0.5+0.5)*chart_lr, label=f'Opt 2: Adaptive Curve ({f2_power:.2f})', color='#ff00ff', linestyle='--', linewidth=2.5)
    ax.set_ylabel("Theoretical Learning Rate Curve", color='#00ffff', fontsize=10)
    ax.tick_params(axis='y', labelcolor='#00ffff')

    ax.axvspan(0, phase_1_boundary, color='#0044ff', alpha=0.12, label=f'Structure Acquisition (Ep 0-{int(phase_1_boundary)})')
    ax.axvspan(phase_1_boundary, phase_2_boundary, color='#00ff44', alpha=0.06, label=f'Texture Refinement Phase')
    ax.axvspan(phase_2_boundary, dynamic_target_epochs, color='#ff0000', alpha=0.08, label=f'Danger Zone / Saturation (Ep {int(phase_2_boundary)}+)')
    ax.axvspan(goldi_entry, goldi_exit, facecolor='#ffaa00', alpha=0.25, hatch='//', edgecolor='#ffaa00', linewidth=0, label=f'GOLDILOCKS ZONE: Peak Performance')
    
    ax.axvline(x=phase_1_boundary, color='#00bcff', linestyle=':', alpha=0.4)
    ax.axvline(x=phase_2_boundary, color='#ff3333', linestyle=':', alpha=0.4)
    
    ax2 = ax.twinx()
    loss_line, = ax2.plot([], [], label='Real-world Loss Tracking', color='#ff3366', alpha=0.3, linewidth=1)
    ma5_line, = ax2.plot([], [], label='MA5 Convergence Baseline', color='#ffcc00', alpha=0.9, linewidth=1.8)
    ax2.set_ylabel("Error Loss Gradient / MA5", color='#ff3366', fontsize=10)
    ax2.tick_params(axis='y', labelcolor='#ff3366')
    
    plot_state = {'log_path': log_path, 'dynamic_target_epochs': dynamic_target_epochs}

    def update_plot_metrics():
        log_eps, log_losses, log_ma5 = parse_training_log(plot_state['log_path'])
        if log_eps and log_losses:
            loss_line.set_data(log_eps, log_losses)
            if log_ma5: ma5_line.set_data(log_eps, log_ma5)
            max_x = max(plot_state['dynamic_target_epochs'], max(log_eps))
            ax.set_xlim(0, max_x)
            all_vals = log_losses + (log_ma5 if log_ma5 else [])
            ax2.set_ylim(min(all_vals) * 0.9, max(all_vals) * 1.1)
            lines_1, labels_1 = ax.get_legend_handles_labels()
            lines_2, labels_2 = ax2.get_legend_handles_labels()
            if ax.get_legend(): ax.get_legend().remove()
            ax.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', frameon=True, facecolor='#111111', edgecolor='#333333')
            fig.canvas.draw_idle()

    def on_key(event):
        if event.key and event.key.lower() == 'r':
            if not plot_state['log_path']:
                root_sub = Tk(); root_sub.withdraw()
                selected = filedialog.askopenfilename(title="Select Log File", filetypes=[("Log Files", "*.csv *.txt *.log"), ("All Files", "*.*")])
                root_sub.destroy()
                if selected: plot_state['log_path'] = selected
                else: return
            update_plot_metrics()

    fig.canvas.mpl_connect('key_press_event', on_key)
    if log_path: update_plot_metrics()
    else:
        lines_1, labels_1 = ax.get_legend_handles_labels()
        ax.legend(lines_1, labels_1, loc='upper right', frameon=True, facecolor='#111111', edgecolor='#333333')
        
    ax.set_title(f"Adaptive Training Framework vs Real-World Analytics | Dataset Cohesion: {sim_percent:.1f}%", fontsize=11, pad=12)
    ax.set_xlabel("Training Duration (Epochs)", fontsize=10)
    ax.grid(True, alpha=0.08, color='#ffffff')
    ax.set_xlim(0, dynamic_target_epochs)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    generate_smart_plan()