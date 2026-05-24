import os
import soundfile as sf
import numpy as np

# Prevent execution dependency failures during fallback conditions
try:
    import librosa
except ImportError:
    librosa = None

def audit_audio_files(folder_path):
    valid_files = []
    list_of_individual_durations = []
    total_scanned = 0 
    total_duration_secs = 0.0
    
    extensions = ('.wav', '.flac', '.mp3', '.ogg')
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(extensions)]
    
    print("\n" + "="*75)
    print("DETAILED PER-FILE AUDIO AUDIT:")
    print("="*75)
    
    for f_path in files:
        filename = os.path.basename(f_path)
        total_scanned += 1
        try:
            info = sf.info(f_path)
            duration = len(info) / info.samplerate
            total_duration_secs += duration
            list_of_individual_durations.append(duration)
            print(f" [+] {filename:<40} -> [PASS] Format Verified ({int(duration)}s) | Rate: {info.samplerate}Hz")
            valid_files.append(f_path)
        except Exception:
            try:
                if librosa is None: raise ImportError("Librosa interface missing.")
                duration = librosa.get_duration(path=f_path)
                total_duration_secs += duration
                list_of_individual_durations.append(duration)
                print(f" [+] {filename:<40} -> [PASS] Fallback Read Verified ({int(duration)}s)")
                valid_files.append(f_path)
            except Exception:
                print(f" [x] {filename:<40} -> [ERROR] Unreadable file metadata")
                continue
                
    print("\n" + "="*75)
    print("AUDIT MATRIX EXECUTIVE SUMMARY")
    print("="*75)
    print(f" Total Audio Tracks Scanned:        {total_scanned}")
    print(f" Successful Passes (Ready):         {len(valid_files)}")
    print(f" Total Dataset Playback Duration:   {int(total_duration_secs // 60)}m {int(total_duration_secs % 60)}s")
    print("="*75)
            
    return valid_files, total_duration_secs, list_of_individual_durations

def analyze_similarity_and_quality(files, target_chunk_len):
    """
    Returns dummy metrics placeholder for analysis metrics to keep decoupling complete.
    Replace with your actual DSP math engine layer logic.
    """
    # bpm_std, centroid_var, cohesion_pct, mean_centroid, quality_score, quality_tier
    return 1.45, 0.12, 88.5, 2450.0, 92.0, "Tier S [Premium Studio Grade]"