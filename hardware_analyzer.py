# hardware_analyzer.py
import ctypes

def get_automated_vram():
    """
    Queries NVML or PyTorch for hardware topology configurations.
    """
    detected_vram = 12
    precision_mode = "fp16"

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
            detected_vram = round(mem_info.total / (1024**3))
            
            name_buffer = ctypes.create_string_buffer(64)
            nvml.nvmlDeviceGetName(device, name_buffer, 64)
            gpu_name = name_buffer.value.decode('utf-8', errors='ignore').upper()
            nvml.nvmlShutdown()

            if any(x in gpu_name for x in ["RTX 30", "RTX 40", "A30", "A40", "A16", "A2", "A100", "H100", "RTX 6000", "RTX 5000"]):
                precision_mode = "bf16"
                print(f"[+] AUTOMATED HARDWARE SCAN: Mapped {gpu_name}. Detected {detected_vram}GB VRAM. Architecture supports native BF16.")
            else:
                print(f"[+] AUTOMATED HARDWARE SCAN: Mapped {gpu_name}. Detected {detected_vram}GB VRAM. Defaulting to FP16.")
            return detected_vram, precision_mode
    except Exception: pass

    try:
        import torch
        if torch.cuda.is_available():
            detected_vram = round(torch.cuda.get_device_properties(0).total_memory / (1024**3))
            major_version = torch.cuda.get_device_capability(0)[0]
            if major_version >= 8:
                precision_mode = "bf16"
                print(f"[+] PYTORCH SCAN: CUDA Device Capability {major_version}.x detected. Detected {detected_vram}GB VRAM. Enabling BF16.")
            else:
                print(f"[+] PYTORCH SCAN: CUDA Device Capability {major_version}.x detected. Detected {detected_vram}GB VRAM. Enabling FP16.")
            return detected_vram, precision_mode
    except Exception: pass

    print("[-] HARDWARE UTILITY: No native discrete GPU found in address space.")
    try:
        vram_input = int(input(" -> Enter Available Dedicated VRAM manually (GB, default 12): ") or 12)
        gpu_series = input(" -> Is your GPU an NVIDIA RTX 30-series or 40-series? (y/n, default n): ").lower() == 'y'
        precision_mode = "bf16" if gpu_series else "fp16"
        return vram_input, precision_mode
    except ValueError:
        return 12, "fp16"