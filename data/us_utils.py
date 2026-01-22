"""
Ultrasound Physics Utilities for Deliverable 3
BMEN 509/623 - Introduction to Biomedical Imaging

This module provides helper functions for ultrasound physics calculations
and data loading utilities.
"""

import numpy as np
import pandas as pd
from pathlib import Path


# Physical constants
SPEED_OF_SOUND_TISSUE = 1540  # m/s (average soft tissue)
SPEED_OF_SOUND_WATER = 1480   # m/s at 20°C


def load_tissue_properties(data_dir=None):
    """
    Load tissue acoustic properties from CSV file.
    
    Parameters
    ----------
    data_dir : str or Path, optional
        Directory containing data files. If None, uses current directory.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: tissue, density, speed_of_sound, attenuation_coeff
    """
    if data_dir is None:
        data_dir = Path(__file__).parent
    else:
        data_dir = Path(data_dir)
    
    return pd.read_csv(data_dir / 'tissue_acoustic_properties.csv')


def load_clinical_scenarios(data_dir=None):
    """
    Load clinical imaging scenarios from CSV file.
    
    Parameters
    ----------
    data_dir : str or Path, optional
        Directory containing data files.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with clinical scenario descriptions and layer configurations
    """
    if data_dir is None:
        data_dir = Path(__file__).parent
    else:
        data_dir = Path(data_dir)
    
    return pd.read_csv(data_dir / 'clinical_scenarios.csv')


def load_doppler_signal(signal_name, data_dir=None):
    """
    Load a Doppler signal from numpy file.
    
    Parameters
    ----------
    signal_name : str
        Name of the signal (without .npy extension)
    data_dir : str or Path, optional
        Directory containing data files.
    
    Returns
    -------
    dict
        Dictionary with keys: 'signal', 'fs', 'f0', 'prf', 'depth', 'angle', 'metadata'
    """
    if data_dir is None:
        data_dir = Path(__file__).parent / 'doppler_signals'
    else:
        data_dir = Path(data_dir)
    
    data = np.load(data_dir / f'{signal_name}.npy', allow_pickle=True).item()
    return data


def list_doppler_signals(data_dir=None):
    """
    List available Doppler signal files.
    
    Parameters
    ----------
    data_dir : str or Path, optional
        Directory containing doppler_signals folder.
    
    Returns
    -------
    list
        List of available signal names
    """
    if data_dir is None:
        data_dir = Path(__file__).parent / 'doppler_signals'
    else:
        data_dir = Path(data_dir)
    
    return [f.stem for f in data_dir.glob('*.npy')]


def load_phantom_data(data_dir=None):
    """
    Load wire phantom data for resolution measurement.
    
    Parameters
    ----------
    data_dir : str or Path, optional
        Directory containing data files.
    
    Returns
    -------
    dict
        Dictionary with 'image', 'pixel_size_mm', 'wire_positions'
    """
    if data_dir is None:
        data_dir = Path(__file__).parent
    else:
        data_dir = Path(data_dir)
    
    return np.load(data_dir / 'us_phantom_wires.npy', allow_pickle=True).item()


def load_artifact_image(artifact_type, data_dir=None):
    """
    Load an artifact image.
    
    Parameters
    ----------
    artifact_type : str
        Type of artifact: 'shadow', 'enhancement', 'reverberation'
    data_dir : str or Path, optional
        Directory containing data files.
    
    Returns
    -------
    dict
        Dictionary with 'image', 'pixel_size_mm', 'artifact_location', 'metadata'
    """
    if data_dir is None:
        data_dir = Path(__file__).parent
    else:
        data_dir = Path(data_dir)
    
    filename = f'us_artifact_{artifact_type}.npy'
    return np.load(data_dir / filename, allow_pickle=True).item()


# Helper physics functions (partially implemented - students complete these)

def calculate_wavelength(frequency_hz, speed_of_sound=SPEED_OF_SOUND_TISSUE):
    """
    Calculate ultrasound wavelength.
    
    Parameters
    ----------
    frequency_hz : float
        Ultrasound frequency in Hz
    speed_of_sound : float
        Speed of sound in m/s
    
    Returns
    -------
    float
        Wavelength in meters
    """
    return speed_of_sound / frequency_hz


def theoretical_axial_resolution(frequency_hz, n_cycles=2, speed_of_sound=SPEED_OF_SOUND_TISSUE):
    """
    Calculate theoretical axial resolution.
    
    Axial Resolution = n_cycles * wavelength / 2
    
    Parameters
    ----------
    frequency_hz : float
        Center frequency in Hz
    n_cycles : int
        Number of cycles in the pulse
    speed_of_sound : float
        Speed of sound in m/s
    
    Returns
    -------
    float
        Axial resolution in meters
    """
    wavelength = calculate_wavelength(frequency_hz, speed_of_sound)
    return n_cycles * wavelength / 2


def max_unambiguous_depth(prf):
    """
    Calculate maximum unambiguous imaging depth.
    
    d_max = c / (2 * PRF)
    
    Parameters
    ----------
    prf : float
        Pulse repetition frequency in Hz
    
    Returns
    -------
    float
        Maximum depth in meters
    """
    return SPEED_OF_SOUND_TISSUE / (2 * prf)


def max_unambiguous_velocity(prf, f0, theta_deg=0):
    """
    Calculate maximum unambiguous velocity (Nyquist limit).
    
    v_max = c * PRF / (4 * f0 * cos(theta))
    
    Parameters
    ----------
    prf : float
        Pulse repetition frequency in Hz
    f0 : float
        Center frequency in Hz
    theta_deg : float
        Doppler angle in degrees
    
    Returns
    -------
    float
        Maximum unambiguous velocity in m/s
    """
    theta_rad = np.deg2rad(theta_deg)
    return SPEED_OF_SOUND_TISSUE * prf / (4 * f0 * np.cos(theta_rad))
