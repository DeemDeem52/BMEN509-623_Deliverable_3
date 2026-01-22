"""
Data Generation Script for Deliverable 3: Ultrasound Physics & Imaging
BMEN 509/623 - Introduction to Biomedical Imaging

This script generates all data files needed for the deliverable:
1. Tissue acoustic properties (CSV)
2. Clinical scenarios (CSV)
3. Doppler signals (NPY files)
4. Wire phantom for resolution (NPY)
5. Artifact images (NPY files)

Run this script from the data directory to generate all files.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import signal
from scipy.ndimage import gaussian_filter


# Set random seed for reproducibility
np.random.seed(509)

# Output directory
OUTPUT_DIR = Path(__file__).parent


def generate_tissue_properties():
    """Generate tissue acoustic properties database."""
    
    # Tissue properties: density (kg/m³), speed of sound (m/s), attenuation (dB/cm/MHz)
    tissues = {
        'air': (1.2, 330, 12.0),
        'water': (1000, 1480, 0.002),
        'blood': (1060, 1570, 0.2),
        'fat': (920, 1450, 0.6),
        'liver': (1060, 1550, 0.5),
        'kidney': (1050, 1560, 0.9),
        'spleen': (1060, 1570, 0.5),
        'muscle': (1050, 1580, 1.0),
        'bone_cortical': (1900, 3500, 10.0),
        'bone_trabecular': (1100, 1800, 5.0),
        'cartilage': (1100, 1660, 1.0),
        'tendon': (1100, 1750, 1.2),
        'skin': (1100, 1600, 1.5),
        'breast_fat': (930, 1460, 0.75),
        'breast_gland': (1020, 1510, 1.0),
        'thyroid': (1050, 1575, 0.8),
        'prostate': (1040, 1560, 0.8),
        'lung_inflated': (400, 600, 8.0),
        'amniotic_fluid': (1000, 1510, 0.005),
        'vitreous_humor': (1000, 1520, 0.1),
        'lens': (1100, 1620, 1.5),
        'gallstone': (1800, 2500, 4.0),
        'kidney_stone': (2000, 3000, 6.0),
        'soft_tissue_avg': (1050, 1540, 0.7),
    }
    
    data = []
    for tissue, (density, speed, atten) in tissues.items():
        impedance = density * speed / 1e6  # Convert to MRayl
        data.append({
            'tissue': tissue,
            'density_kg_m3': density,
            'speed_of_sound_m_s': speed,
            'attenuation_dB_cm_MHz': atten,
            'acoustic_impedance_MRayl': round(impedance, 3)
        })
    
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_DIR / 'tissue_acoustic_properties.csv', index=False)
    print(f"Generated tissue_acoustic_properties.csv with {len(df)} tissues")
    return df


def generate_clinical_scenarios():
    """Generate clinical imaging scenarios for analysis."""
    
    scenarios = [
        {
            'scenario_id': 1,
            'name': 'Abdominal liver imaging',
            'description': 'Standard transabdominal approach to image liver parenchyma',
            'layers': 'skin,fat,muscle,liver',
            'layer_thicknesses_cm': '0.2,2.0,1.5,5.0',
            'target_depth_cm': 8.7,
            'frequency_MHz': 3.5,
            'clinical_question': 'Evaluate liver echogenicity for fatty liver disease'
        },
        {
            'scenario_id': 2,
            'name': 'Thyroid examination',
            'description': 'High-frequency imaging of superficial thyroid gland',
            'layers': 'skin,muscle,thyroid',
            'layer_thicknesses_cm': '0.15,0.5,2.0',
            'target_depth_cm': 2.65,
            'frequency_MHz': 10.0,
            'clinical_question': 'Characterize thyroid nodule for malignancy risk'
        },
        {
            'scenario_id': 3,
            'name': 'Obstetric fetal imaging',
            'description': 'Second trimester fetal anatomy scan',
            'layers': 'skin,fat,muscle,amniotic_fluid',
            'layer_thicknesses_cm': '0.2,3.0,1.0,8.0',
            'target_depth_cm': 12.2,
            'frequency_MHz': 5.0,
            'clinical_question': 'Assess fetal anatomy and growth parameters'
        },
        {
            'scenario_id': 4,
            'name': 'Renal transplant assessment',
            'description': 'Imaging of transplanted kidney in iliac fossa',
            'layers': 'skin,fat,kidney',
            'layer_thicknesses_cm': '0.2,1.5,5.0',
            'target_depth_cm': 6.7,
            'frequency_MHz': 4.0,
            'clinical_question': 'Evaluate transplant perfusion and parenchyma'
        },
        {
            'scenario_id': 5,
            'name': 'Breast mass characterization',
            'description': 'High-frequency imaging of palpable breast mass',
            'layers': 'skin,breast_fat,breast_gland',
            'layer_thicknesses_cm': '0.2,1.0,2.0',
            'target_depth_cm': 3.2,
            'frequency_MHz': 12.0,
            'clinical_question': 'Differentiate cystic from solid mass'
        },
        {
            'scenario_id': 6,
            'name': 'Deep venous assessment',
            'description': 'Compression ultrasound for deep vein thrombosis',
            'layers': 'skin,fat,muscle,blood',
            'layer_thicknesses_cm': '0.2,1.0,2.5,0.5',
            'target_depth_cm': 4.2,
            'frequency_MHz': 7.5,
            'clinical_question': 'Detect presence of DVT in femoral vein'
        },
        {
            'scenario_id': 7,
            'name': 'Gallbladder examination',
            'description': 'Right upper quadrant imaging for cholelithiasis',
            'layers': 'skin,fat,liver',
            'layer_thicknesses_cm': '0.2,2.5,4.0',
            'target_depth_cm': 6.7,
            'frequency_MHz': 4.0,
            'clinical_question': 'Identify gallstones and wall thickening'
        },
        {
            'scenario_id': 8,
            'name': 'Carotid artery imaging',
            'description': 'Evaluation of carotid artery for stenosis',
            'layers': 'skin,muscle,blood',
            'layer_thicknesses_cm': '0.2,1.5,0.8',
            'target_depth_cm': 2.5,
            'frequency_MHz': 9.0,
            'clinical_question': 'Measure intima-media thickness and stenosis degree'
        },
    ]
    
    df = pd.DataFrame(scenarios)
    df.to_csv(OUTPUT_DIR / 'clinical_scenarios.csv', index=False)
    print(f"Generated clinical_scenarios.csv with {len(df)} scenarios")
    return df


def generate_doppler_signal(velocity_m_s, f0_hz, prf_hz, depth_m, theta_deg, 
                            duration_s=0.1, noise_level=0.1, aliased=False):
    """
    Generate simulated Doppler signal.
    
    Parameters
    ----------
    velocity_m_s : float
        True blood velocity in m/s
    f0_hz : float
        Transducer center frequency in Hz
    prf_hz : float
        Pulse repetition frequency in Hz
    depth_m : float
        Target depth in meters
    theta_deg : float
        Doppler angle in degrees
    duration_s : float
        Signal duration in seconds
    noise_level : float
        Relative noise level (0-1)
    aliased : bool
        If True, signal may show aliasing
    
    Returns
    -------
    dict
        Signal data dictionary
    """
    c = 1540  # Speed of sound in tissue
    theta_rad = np.deg2rad(theta_deg)
    
    # Calculate Doppler frequency shift
    f_doppler = 2 * f0_hz * velocity_m_s * np.cos(theta_rad) / c
    
    # Sample at PRF (simulating slow-time sampling)
    fs = prf_hz  # Sampling frequency
    n_samples = int(duration_s * fs)
    t = np.arange(n_samples) / fs
    
    # Generate Doppler signal
    # Add some spectral broadening
    broadening = 0.1 * f_doppler * np.random.randn(n_samples)
    
    signal_clean = np.sin(2 * np.pi * (f_doppler + broadening) * t)
    
    # Add noise
    noise = noise_level * np.random.randn(n_samples)
    doppler_signal = signal_clean + noise
    
    # Normalize
    doppler_signal = doppler_signal / np.max(np.abs(doppler_signal))
    
    # Calculate Nyquist limit
    v_nyquist = c * prf_hz / (4 * f0_hz * np.cos(theta_rad))
    is_aliased = np.abs(velocity_m_s) > v_nyquist
    
    return {
        'signal': doppler_signal,
        'fs': fs,
        'f0': f0_hz,
        'prf': prf_hz,
        'depth': depth_m,
        'angle_deg': theta_deg,
        'duration': duration_s,
        'metadata': {
            'true_velocity_m_s': velocity_m_s,
            'doppler_shift_hz': f_doppler,
            'nyquist_velocity_m_s': v_nyquist,
            'is_aliased': is_aliased,
            'noise_level': noise_level,
        }
    }


def generate_doppler_signals():
    """Generate suite of Doppler signals for analysis."""
    
    doppler_dir = OUTPUT_DIR / 'doppler_signals'
    doppler_dir.mkdir(exist_ok=True)
    
    # Signal configurations: (name, velocity, f0, prf, depth, angle, noise)
    configs = [
        # Normal arterial flow - not aliased
        ('carotid_normal', 0.8, 5e6, 8000, 0.025, 60, 0.1),
        
        # Fast arterial flow - may alias at low PRF
        ('carotid_stenosis', 2.5, 5e6, 6000, 0.025, 60, 0.1),
        
        # Venous flow - slow, not aliased
        ('femoral_vein', 0.15, 7.5e6, 4000, 0.04, 45, 0.15),
        
        # Portal vein - moderate flow
        ('portal_vein', 0.25, 3.5e6, 5000, 0.08, 50, 0.12),
        
        # Hepatic artery - pulsatile
        ('hepatic_artery', 0.6, 3.5e6, 6000, 0.06, 55, 0.1),
        
        # Umbilical artery - fetal
        ('umbilical_artery', 0.45, 5e6, 4000, 0.10, 30, 0.2),
        
        # Middle cerebral artery - TCD
        ('mca_tcd', 0.7, 2e6, 10000, 0.05, 0, 0.15),
        
        # Aorta - high velocity
        ('aorta_normal', 1.2, 2.5e6, 8000, 0.12, 50, 0.1),
        
        # Aortic stenosis - very high velocity, likely aliased
        ('aortic_stenosis', 4.5, 2.5e6, 6000, 0.10, 20, 0.1),
        
        # Renal artery
        ('renal_artery', 0.9, 3.5e6, 7000, 0.07, 55, 0.12),
        
        # Low PRF test - will alias moderate flow
        ('test_low_prf', 0.5, 5e6, 2000, 0.03, 60, 0.1),
        
        # High PRF test - won't alias same flow
        ('test_high_prf', 0.5, 5e6, 12000, 0.03, 60, 0.1),
        
        # Deep vessel - constrained PRF by depth
        ('deep_vessel', 0.6, 2e6, 3000, 0.20, 60, 0.2),
        
        # Superficial vessel - can use high PRF
        ('superficial_vessel', 1.5, 10e6, 15000, 0.01, 70, 0.08),
        
        # Venous insufficiency - reflux
        ('venous_reflux', -0.3, 7.5e6, 5000, 0.035, 60, 0.12),
    ]
    
    for name, vel, f0, prf, depth, angle, noise in configs:
        data = generate_doppler_signal(vel, f0, prf, depth, angle, noise_level=noise)
        np.save(doppler_dir / f'{name}.npy', data, allow_pickle=True)
    
    print(f"Generated {len(configs)} Doppler signal files")


def generate_wire_phantom():
    """Generate wire phantom image for resolution measurement."""
    
    # Image parameters
    nx, nz = 512, 512  # Image dimensions (lateral x axial)
    pixel_size_mm = 0.1  # 0.1 mm per pixel
    
    # Simulate typical 5 MHz transducer PSF
    frequency_mhz = 5.0
    c = 1540  # m/s
    wavelength_mm = c / (frequency_mhz * 1e6) * 1000  # Convert to mm
    
    # Axial resolution (determined by pulse length)
    axial_fwhm_mm = 2 * wavelength_mm  # Approximately 2 wavelengths
    
    # Lateral resolution (depends on depth and focusing)
    # Use different values at different depths to show depth dependence
    
    # Wire positions (lateral_mm, axial_mm)
    # Place wires at different depths to show resolution variation
    wire_positions = [
        (25.0, 10.0),   # Shallow - good lateral resolution
        (25.0, 20.0),
        (25.0, 30.0),   # Focal zone - best lateral resolution
        (25.0, 40.0),
        (25.0, 50.0),   # Deep - degraded lateral resolution
    ]
    
    # Create image
    image = np.zeros((nz, nx))
    
    # Background speckle
    speckle = np.random.rayleigh(0.15, size=(nz, nx))
    image += speckle
    
    # Add wire responses (point spread functions)
    for lat_mm, ax_mm in wire_positions:
        # Convert to pixel coordinates
        lat_px = int(lat_mm / pixel_size_mm)
        ax_px = int(ax_mm / pixel_size_mm)
        
        # Depth-dependent lateral resolution
        # Better at focal zone (30 mm), worse away from it
        focal_depth_mm = 30.0
        depth_factor = 1 + 0.02 * np.abs(ax_mm - focal_depth_mm)
        lateral_fwhm_mm = wavelength_mm * 2 * depth_factor
        
        # Convert FWHM to sigma
        axial_sigma = axial_fwhm_mm / pixel_size_mm / 2.355
        lateral_sigma = lateral_fwhm_mm / pixel_size_mm / 2.355
        
        # Create PSF
        y_range = np.arange(max(0, ax_px-50), min(nz, ax_px+50))
        x_range = np.arange(max(0, lat_px-50), min(nx, lat_px+50))
        
        for y in y_range:
            for x in x_range:
                r_axial = (y - ax_px) / axial_sigma
                r_lateral = (x - lat_px) / lateral_sigma
                psf_value = np.exp(-0.5 * (r_axial**2 + r_lateral**2))
                if psf_value > 0.01:
                    image[y, x] += 5.0 * psf_value  # Wire amplitude
    
    # Apply log compression (typical for ultrasound display)
    image = np.clip(image, 0.001, None)
    image_db = 20 * np.log10(image / image.max())
    image_display = np.clip(image_db, -60, 0) + 60  # 60 dB dynamic range
    
    data = {
        'image': image_display,
        'image_linear': image,
        'pixel_size_mm': pixel_size_mm,
        'frequency_mhz': frequency_mhz,
        'focal_depth_mm': focal_depth_mm,
        'wire_positions_mm': wire_positions,
        'theoretical_axial_resolution_mm': axial_fwhm_mm,
    }
    
    np.save(OUTPUT_DIR / 'us_phantom_wires.npy', data, allow_pickle=True)
    print("Generated us_phantom_wires.npy")


def generate_artifact_images():
    """Generate ultrasound images with common artifacts."""
    
    # Common parameters
    nx, nz = 400, 500
    pixel_size_mm = 0.15
    
    # 1. Acoustic shadowing (behind gallstone)
    def create_shadow_artifact():
        image = np.random.rayleigh(0.3, size=(nz, nx))
        
        # Gallbladder (anechoic region)
        gb_center = (200, 150)
        gb_radius = 40
        for y in range(nz):
            for x in range(nx):
                dist = np.sqrt((x - gb_center[0])**2 + (y - gb_center[1])**2)
                if dist < gb_radius:
                    image[y, x] *= 0.05  # Near anechoic
        
        # Gallstone (hyperechoic)
        stone_center = (180, 180)
        stone_radius = 12
        for y in range(nz):
            for x in range(nx):
                dist = np.sqrt((x - stone_center[0])**2 + (y - stone_center[1])**2)
                if dist < stone_radius:
                    image[y, x] = 2.0 + np.random.random() * 0.5
        
        # Shadow behind stone
        shadow_start_y = 192
        shadow_width = 30
        shadow_center_x = 180
        for y in range(shadow_start_y, nz):
            shadow_factor = 0.1 * np.exp(-0.005 * (y - shadow_start_y))  # Gradual recovery
            for x in range(shadow_center_x - shadow_width//2, shadow_center_x + shadow_width//2):
                if 0 <= x < nx:
                    falloff = 1 - np.abs(x - shadow_center_x) / (shadow_width/2)
                    image[y, x] *= (shadow_factor + (1 - falloff) * 0.3)
        
        # Log compress
        image = np.clip(image, 0.001, None)
        image_db = 20 * np.log10(image / image.max())
        image_display = np.clip(image_db, -50, 0) + 50
        
        return {
            'image': image_display,
            'pixel_size_mm': pixel_size_mm,
            'artifact_type': 'acoustic_shadow',
            'artifact_location': {'x': shadow_center_x, 'y_start': shadow_start_y},
            'cause': 'High attenuation gallstone blocking ultrasound beam',
            'metadata': {
                'stone_position': stone_center,
                'shadow_width_px': shadow_width,
            }
        }
    
    # 2. Posterior acoustic enhancement (behind cyst)
    def create_enhancement_artifact():
        image = np.random.rayleigh(0.3, size=(nz, nx))
        
        # Simple cyst (anechoic)
        cyst_center = (200, 120)
        cyst_radius = 35
        for y in range(nz):
            for x in range(nx):
                dist = np.sqrt((x - cyst_center[0])**2 + (y - cyst_center[1])**2)
                if dist < cyst_radius:
                    image[y, x] *= 0.02  # Anechoic
                elif dist < cyst_radius + 3:
                    image[y, x] *= 1.5  # Wall enhancement
        
        # Enhancement behind cyst
        enhance_start_y = cyst_center[1] + cyst_radius + 3
        enhance_width = int(cyst_radius * 1.8)
        enhance_center_x = cyst_center[0]
        
        for y in range(enhance_start_y, min(enhance_start_y + 150, nz)):
            enhance_factor = 1.8 * np.exp(-0.01 * (y - enhance_start_y))
            for x in range(enhance_center_x - enhance_width//2, enhance_center_x + enhance_width//2):
                if 0 <= x < nx:
                    falloff = 1 - np.abs(x - enhance_center_x) / (enhance_width/2)
                    image[y, x] *= (1 + (enhance_factor - 1) * falloff)
        
        # Log compress
        image = np.clip(image, 0.001, None)
        image_db = 20 * np.log10(image / image.max())
        image_display = np.clip(image_db, -50, 0) + 50
        
        return {
            'image': image_display,
            'pixel_size_mm': pixel_size_mm,
            'artifact_type': 'posterior_enhancement',
            'artifact_location': {'x': enhance_center_x, 'y_start': enhance_start_y},
            'cause': 'Low attenuation through cyst fluid allows more sound to reach deeper tissues',
            'metadata': {
                'cyst_position': cyst_center,
                'cyst_radius': cyst_radius,
                'enhancement_width_px': enhance_width,
            }
        }
    
    # 3. Reverberation artifact
    def create_reverberation_artifact():
        image = np.random.rayleigh(0.25, size=(nz, nx))
        
        # Simulate scanning near air interface or implant
        # Primary reflector (bright line)
        reflector_y = 80
        reflector_width_x = (100, 300)
        
        # Main reflector
        for x in range(reflector_width_x[0], reflector_width_x[1]):
            image[reflector_y, x] = 2.5 + np.random.random() * 0.3
            image[reflector_y+1, x] = 2.0 + np.random.random() * 0.3
        
        # Reverberation echoes (equally spaced)
        spacing = reflector_y  # Distance from transducer determines spacing
        n_reverbs = 5
        
        for i in range(1, n_reverbs + 1):
            reverb_y = reflector_y + i * spacing
            if reverb_y < nz - 2:
                amplitude = 2.5 * (0.6 ** i)  # Decreasing amplitude
                for x in range(reflector_width_x[0], reflector_width_x[1]):
                    # Reverberations are typically sharper
                    image[reverb_y, x] = amplitude + np.random.random() * 0.2
                    image[reverb_y+1, x] = amplitude * 0.7 + np.random.random() * 0.2
        
        # Log compress
        image = np.clip(image, 0.001, None)
        image_db = 20 * np.log10(image / image.max())
        image_display = np.clip(image_db, -50, 0) + 50
        
        return {
            'image': image_display,
            'pixel_size_mm': pixel_size_mm,
            'artifact_type': 'reverberation',
            'artifact_location': {'y_primary': reflector_y, 'x_range': reflector_width_x},
            'cause': 'Multiple reflections between transducer and strong reflector creating equally spaced echoes',
            'metadata': {
                'primary_reflector_depth_px': reflector_y,
                'reverberation_spacing_px': spacing,
                'n_reverberations': n_reverbs,
            }
        }
    
    # Generate all artifact images
    shadow_data = create_shadow_artifact()
    np.save(OUTPUT_DIR / 'us_artifact_shadow.npy', shadow_data, allow_pickle=True)
    
    enhance_data = create_enhancement_artifact()
    np.save(OUTPUT_DIR / 'us_artifact_enhancement.npy', enhance_data, allow_pickle=True)
    
    reverb_data = create_reverberation_artifact()
    np.save(OUTPUT_DIR / 'us_artifact_reverberation.npy', reverb_data, allow_pickle=True)
    
    print("Generated 3 artifact image files")


if __name__ == '__main__':
    print("Generating Deliverable 3 data files...")
    print("-" * 50)
    
    generate_tissue_properties()
    generate_clinical_scenarios()
    generate_doppler_signals()
    generate_wire_phantom()
    generate_artifact_images()
    
    print("-" * 50)
    print("Data generation complete!")
