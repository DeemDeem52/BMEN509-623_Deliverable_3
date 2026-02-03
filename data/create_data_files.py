#!/usr/bin/env python3
"""
Create data files for BMEN 509 Deliverable 3: Ultrasound Physics & Imaging
"""
import numpy as np
import pandas as pd

# ==================== TISSUE PROPERTIES CSV ====================
tissue_data = {
    'Tissue': ['Air', 'Lung', 'Fat', 'Water', 'Blood', 'Liver', 'Kidney', 'Muscle', 'Soft Tissue (avg)', 'Gallstone', 'Bone'],
    'Density_kg_m3': [1.2, 300, 920, 1000, 1060, 1060, 1040, 1050, 1040, 1800, 1900],
    'Speed_m_s': [343, 600, 1450, 1480, 1570, 1550, 1560, 1580, 1540, 2500, 3500],
    'Impedance_MRayl': [0.0004, 0.18, 1.33, 1.48, 1.66, 1.64, 1.62, 1.66, 1.60, 4.50, 6.65],
    'Attenuation_dB_cm_MHz': [12.0, 41.0, 0.63, 0.002, 0.18, 0.50, 0.50, 1.09, 0.50, 1.0, 10.0]
}

df_tissue = pd.DataFrame(tissue_data)
df_tissue.to_csv('tissue_properties.csv', index=False)
print("Created tissue_properties.csv")

# ==================== DOPPLER SIGNAL ====================
# Create a simulated Doppler signal with a known velocity
# Parameters that will create aliasing to test student understanding

f0 = 5e6  # 5 MHz transmit frequency
PRF = 8000  # 8 kHz PRF
angle_deg = 60  # Doppler angle
c = 1540  # speed of sound m/s

# Target blood velocity (will cause aliasing)
true_velocity = 0.95  # m/s - high but below Nyquist

# Calculate expected Doppler shift
theta_rad = np.radians(angle_deg)
expected_fd = (2 * true_velocity * f0 * np.cos(theta_rad)) / c
print(f"True velocity: {true_velocity} m/s")
print(f"Expected Doppler shift: {expected_fd:.1f} Hz")

# Nyquist limit
v_max = (c * PRF) / (4 * f0 * np.cos(theta_rad))
print(f"Nyquist velocity limit: {v_max:.3f} m/s")

# Generate signal
sample_rate = 20000  # 20 kHz sampling
duration = 0.5  # 0.5 seconds
t = np.arange(0, duration, 1/sample_rate)

# Doppler signal with some noise
np.random.seed(42)
signal = np.sin(2 * np.pi * expected_fd * t) + 0.2 * np.random.randn(len(t))

# Add a small secondary component (simulating spectral broadening)
signal += 0.3 * np.sin(2 * np.pi * (expected_fd * 0.8) * t)

doppler_data = {
    'signal': signal,
    'f0': f0,
    'PRF': PRF,
    'angle_deg': angle_deg,
    'sample_rate': sample_rate,
    'true_velocity': true_velocity,  # Hidden from students - for solution
    'c': c
}

np.save('doppler_signal.npy', doppler_data)
print("Created doppler_signal.npy")

# ==================== VERIFICATION ====================
print("\n--- Verification ---")
print(f"Tissue properties table has {len(df_tissue)} tissues")
print(f"Doppler signal has {len(signal)} samples")
print(f"  Duration: {duration} s")
print(f"  Sample rate: {sample_rate} Hz")
