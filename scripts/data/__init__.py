"""
EDA Preprocessing Pipeline
==========================
FIR low-pass filter (4 Hz), Gaussian smoothing, EDA decomposition (CDA or cvxEDA),
derivative channels (ΔSCR, Δ²SCR), window segmentation, Z-score normalization.

Supported EDA decomposition methods:
  - cda: Continuous Decomposition Analysis (sanchez2020deep)
  - cvxeda: Convex optimisation approach (Greco et al., IEEE TBME 2016)

References:
  - sanchez2020deep: Deep SVM for stress from EDA, IJNS 2020
  - sanchez2022one: 1D-CNN for EDA arousal, BSPC 2022
  - Greco2016: cvxEDA, IEEE TBME
  - Benedek2010: Ledalab, J. Neurosci. Meth.
  - SPR2012EDA: Publication recommendations for EDA
"""

import numpy as np
from scipy.signal import firwin, lfilter
from scipy.ndimage import gaussian_filter1d
from typing import Tuple, Optional, List, Literal

EDA_AVAILABLE_METHODS = ["cda", "cvxeda"]


def design_fir_lowpass(cutoff: float, fs: float, numtaps: int = 51) -> np.ndarray:
    """Design an FIR low-pass filter.

    Args:
        cutoff: Cut-off frequency in Hz (must be < fs/2).
        fs: Sampling frequency in Hz.
        numtaps: Number of filter taps.

    Returns:
        FIR filter coefficients.
    """
    nyquist = fs / 2.0
    if cutoff >= nyquist:
        cutoff = 0.99 * nyquist  # Clamp to just below Nyquist
    return firwin(numtaps, cutoff / nyquist, window="hamming")


def apply_fir_filter(signal: np.ndarray, cutoff: float = 4.0, fs: float = 4.0) -> np.ndarray:
    """Apply FIR low-pass filter to a 1D signal."""
    fir_coeffs = design_fir_lowpass(cutoff, fs)
    return lfilter(fir_coeffs, [1.0], signal)


def apply_gaussian_smoothing(signal: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """Apply Gaussian smoothing to attenuate acquisition noise."""
    return gaussian_filter1d(signal, sigma=sigma)


def cda_decomposition(
    sc: np.ndarray,
    fs: float = 4.0,
    tau0: float = 2.0,
    tau1: float = 0.7,
    delta_t: float = 0.25,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Continuous Decomposition Analysis (CDA) for EDA signals.

    Decomposes the skin conductance signal into tonic (SCL) and phasic (SCR)
    components via iterative deconvolution based on the Bateman function.

    The phasic driver is extracted from the SC derivative by solving a
    constrained non-negative deconvolution. The SCR is then reconstructed
    using the biexponential impulse response function.

    Args:
        sc: Raw skin conductance signal.
        fs: Sampling frequency (Hz).
        tau0: Rise time constant of the SCR (seconds).
        tau1: Decay time constant of the SCR (seconds).
        delta_t: Time step (seconds) = 1/fs.

    Returns:
        Tuple of (SCR, SCL, phasic_driver).
    """
    n_samples = len(sc)
    dt = delta_t

    # Impulse response function (Bateman / biexponential)
    t = np.arange(0, n_samples * dt, dt)[:n_samples]
    h = np.exp(-t / tau0) - np.exp(-t / tau1)
    h[h < 0] = 0

    # Remove baseline for cleaner deconvolution
    sc_centered = sc - np.mean(sc)

    # Non-negative deconvolution via modified Richardson-Lucy
    driver = _non_negative_deconvolution(sc_centered, h, dt)

    # Reconstruct SCR from driver
    scr = np.convolve(driver, h, mode="full")[:n_samples]

    # Tonic = residual
    scl = sc - scr

    return scr, scl, driver


def decompose_eda_cvxeda(
    sc: np.ndarray,
    fs: float = 4.0,
    tau0: float = 2.0,
    tau1: float = 0.7,
    alpha: float = 8e-4,
    gamma: float = 1e-2,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """cvxEDA decomposition (Greco et al., IEEE TBME 2016).

    Formulates EDA decomposition as a convex optimisation problem:
      EDA = phasic (Bateman biexponential convolved with sparse SMNA driver)
          + tonic (cubic spline with roughness penalty)
          + baseline drift + noise

    Uses the official `cvxeda` Python package (Luca Citi) with cvxopt QP solver.
    Falls back to CDA if cvxeda is not installed.

    Args:
        sc: Raw skin conductance signal.
        fs: Sampling frequency (Hz).
        tau0: Rise time constant (seconds).
        tau1: Decay time constant (seconds).
        alpha: L1 sparsity penalty on phasic driver (default 8e-4).
        gamma: Roughness penalty on tonic spline (default 1e-2).

    Returns:
        Tuple of (SCR, SCL, phasic_driver).
    """
    try:
        from cvxeda import cvxEDA
    except ImportError:
        print("cvxEDA not installed. Falling back to CDA.")
        print("Install: pip install cvxeda cvxopt")
        return cda_decomposition(sc, fs, tau0, tau1)

    dt = 1.0 / fs
    n_samples = len(sc)

    # cvxEDA expects column vector
    yn = sc.reshape(-1, 1).astype(np.float64)

    r, p, t, l, d, e, obj = cvxEDA(
        yn, dt,
        tau0=tau0, tau1=tau1,
        delta_knot=10.0,
        alpha=alpha, gamma=gamma,
        solver="cvxopt",
        options={"show_progress": False},
    )

    scr = r.flatten()
    scl = t.flatten()
    driver = p.flatten()

    return scr, scl, driver


def eda_decomposition(
    sc: np.ndarray,
    method: str = "cda",
    fs: float = 4.0,
    **kwargs,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Unified EDA decomposition dispatcher.

    Args:
        sc: Raw skin conductance signal.
        method: Decomposition method: 'cda' (default) or 'cvxeda'.
        fs: Sampling frequency (Hz).
        **kwargs: Method-specific parameters.

    Returns:
        Tuple of (SCR, SCL, phasic_driver).
    """
    if method == "cvxeda":
        tau0 = kwargs.get("tau0", 2.0)
        tau1 = kwargs.get("tau1", 0.7)
        alpha = kwargs.get("alpha", 8e-4)
        gamma = kwargs.get("gamma", 1e-2)
        return decompose_eda_cvxeda(sc, fs, tau0, tau1, alpha, gamma)
    elif method == "cda":
        tau0 = kwargs.get("tau0", 2.0)
        tau1 = kwargs.get("tau1", 0.7)
        return cda_decomposition(sc, fs, tau0, tau1)
    else:
        raise ValueError(f"Unknown EDA decomposition method '{method}'. "
                         f"Available: {EDA_AVAILABLE_METHODS}")


def _non_negative_deconvolution(
    signal: np.ndarray, kernel: np.ndarray, dt: float, n_iter: int = 30
) -> np.ndarray:
    """Non-negative deconvolution for EDA phasic driver extraction.

    Modified Richardson-Lucy algorithm adapted for EDA signals.
    """
    n = len(signal)
    driver = np.ones(n) * 0.01
    kernel_full = np.convolve(kernel, np.ones(int(1.0 / dt)), mode="full")

    for _ in range(n_iter):
        conv_est = np.convolve(driver, kernel_full, mode="full")
        conv_est = conv_est[:n]
        relative_blur = signal / (conv_est + 1e-8)
        correction = np.convolve(relative_blur, kernel_full[::-1], mode="full")[:n]
        correction = correction / (np.sum(kernel_full) + 1e-8)
        driver = driver * correction
        driver[driver < 0] = 0

    return driver


def compute_derivative_channels(
    scr: np.ndarray, fs: float = 4.0
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute first and second temporal derivatives of SCR.

    Args:
        scr: Phasic skin conductance response.
        fs: Sampling frequency (Hz).

    Returns:
        Tuple of (delta_SCR, delta2_SCR).
    """
    dt = 1.0 / fs
    delta_scr = np.gradient(scr, dt)
    delta2_scr = np.gradient(delta_scr, dt)
    return delta_scr, delta2_scr


def segment_into_windows(
    x: np.ndarray,
    window_seconds: int = 40,
    fs: float = 4.0,
    stride_seconds: Optional[int] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Segment multichannel signal into windows.

    Args:
        x: Signal of shape (n_channels, total_samples).
        window_seconds: Window length in seconds.
        fs: Sampling frequency (Hz).
        stride_seconds: Stride for sliding windows. If None, uses non-overlapping windows.

    Returns:
        Tuple of (windows, valid_mask) where windows is (n_windows, n_channels, window_samples)
        and valid_mask indicates windows that are not padded.
    """
    window_samples = int(window_seconds * fs)
    stride_samples = int(stride_seconds * fs) if stride_seconds else window_samples
    n_channels, total_samples = x.shape

    n_windows = max(1, (total_samples - window_samples) // stride_samples + 1)
    windows = np.zeros((n_windows, n_channels, window_samples), dtype=x.dtype)
    valid_mask = np.ones(n_windows, dtype=bool)

    for i in range(n_windows):
        start = i * stride_samples
        end = start + window_samples
        if end <= total_samples:
            windows[i] = x[:, start:end]
        else:
            pad_len = end - total_samples
            windows[i, :, : total_samples - start] = x[:, start:]
            valid_mask[i] = False

    return windows, valid_mask


def zscore_normalize(
    windows: np.ndarray, train_mean: Optional[np.ndarray] = None,
    train_std: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Apply Z-score normalisation per channel.

    When train_mean/std are provided (test subjects during LOSO),
    uses training statistics to avoid data leakage.

    Args:
        windows: (n_windows, n_channels, window_samples).
        train_mean: Per-channel means from training set.
        train_std: Per-channel standard deviations from training set.

    Returns:
        Tuple of (normalized_windows, mean, std).
    """
    n_channels = windows.shape[1]

    if train_mean is None:
        train_mean = windows.mean(axis=(0, 2), keepdims=True)
        train_std = windows.std(axis=(0, 2), keepdims=True)
    else:
        train_mean = train_mean.reshape(1, n_channels, 1)
        train_std = train_std.reshape(1, n_channels, 1)

    train_std = np.maximum(train_std, 1e-8)
    normalized = (windows - train_mean) / train_std

    return normalized, train_mean.squeeze(), train_std.squeeze()


def preprocess_eda_pipeline(
    sc: np.ndarray,
    window_seconds: int = 40,
    fs: float = 4.0,
    fir_cutoff: float = 4.0,
    gaussian_sigma: float = 1.0,
    stride_seconds: Optional[int] = None,
    decomposition_method: str = "cda",
) -> np.ndarray:
    """Full EDA preprocessing pipeline.

    Processes raw skin conductance into windowed, normalised
    3-channel input (SCR, ΔSCR, Δ²SCR).

    Args:
        sc: Raw skin conductance signal (1D array).
        window_seconds: Window length in seconds.
        fs: Sampling frequency (Hz).
        fir_cutoff: FIR low-pass cutoff (Hz).
        gaussian_sigma: Gaussian smoothing sigma.
        stride_seconds: Stride for sliding windows (None = non-overlapping).
        decomposition_method: 'cda' (sanchez2020deep) or 'cvxeda' (Greco2016).

    Returns:
        Array of shape (n_windows, n_channels=3, window_samples).
    """
    filtered = apply_fir_filter(sc, cutoff=fir_cutoff, fs=fs)
    smoothed = apply_gaussian_smoothing(filtered, sigma=gaussian_sigma)

    scr, scl, _ = eda_decomposition(smoothed, method=decomposition_method, fs=fs)

    delta_scr, delta2_scr = compute_derivative_channels(scr, fs=fs)
    multichannel = np.stack([scr, delta_scr, delta2_scr], axis=0)  # (3, T)

    windows, valid_mask = segment_into_windows(
        multichannel, window_seconds=window_seconds, fs=fs,
        stride_seconds=stride_seconds,
    )
    windows = windows[valid_mask]

    return windows  # (n_windows, 3, T)


def extract_handcrafted_features(
    scr: np.ndarray, fs: float = 4.0, window_seconds: int = 40,
) -> np.ndarray:
    """Extract handcrafted EDA features for the classical SVM baseline.

    Features (from sanchez2020deep):
        - SCR amplitude (peak - onset)
        - Rise time (time from onset to peak)
        - AUC (area under the SCR curve)
        - NS-SCR frequency (number of significant SCRs per minute)
        - Mean SCR value
        - Standard deviation of SCR
        - Skewness of SCR
        - Kurtosis of SCR

    Args:
        scr: Phasic SCR signal (1D).
        fs: Sampling frequency (Hz).
        window_seconds: Window length in seconds.

    Returns:
        Feature vector of shape (n_features,).
    """
    features = []
    dt = 1.0 / fs

    # Basic statistics
    features.append(np.mean(scr))
    features.append(np.std(scr))

    # Skewness and kurtosis (handle edge cases)
    std_val = np.std(scr)
    if std_val > 1e-8:
        features.append(np.mean((scr - np.mean(scr)) ** 3) / (std_val ** 3))
        features.append(np.mean((scr - np.mean(scr)) ** 4) / (std_val ** 4) - 3)
    else:
        features.append(0.0)
        features.append(0.0)

    # SCR amplitude (max - min within window)
    features.append(np.max(scr) - np.min(scr))

    # AUC (trapezoidal integration)
    features.append(np.trapz(np.abs(scr), dx=dt))

    # Rise time (time from min to max)
    min_idx = np.argmin(scr)
    max_idx = np.argmax(scr)
    rise_time = abs(max_idx - min_idx) * dt
    features.append(rise_time)

    # NS-SCR frequency: threshold crossings of 0.02 μS amplitude
    threshold = 0.02
    peaks = _detect_scr_peaks(scr, fs, threshold=threshold)
    n_peaks = len(peaks)
    ns_scr_freq = n_peaks / (window_seconds / 60.0) if window_seconds > 0 else 0
    features.append(ns_scr_freq)

    # Additional features
    features.append(np.max(scr) - np.mean(scr))  # max deviation
    features.append(np.sqrt(np.mean(scr ** 2)))  # RMS

    return np.array(features, dtype=np.float32)


def _detect_scr_peaks(
    scr: np.ndarray, fs: float, threshold: float = 0.02,
    min_distance_seconds: float = 2.0,
) -> List[int]:
    """Detect significant SCR peaks above amplitude threshold."""
    from scipy.signal import find_peaks

    min_distance = int(min_distance_seconds * fs)
    peaks, properties = find_peaks(
        scr, height=threshold, distance=min_distance,
    )
    return list(peaks)
