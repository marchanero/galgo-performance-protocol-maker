"""Classical baseline: handcrafted EDA features + SVM.

Sanchez-Reolid et al., "Deep Learning for Electrodermal Activity-based
Stress Detection," Int. J. Neural Systems, 2020.

Features:
  - SCR amplitude, rise time, AUC, NS-SCR frequency
  - Mean, standard deviation, skewness, kurtosis of SCR
  - Max deviation, RMS

Reference F1: 0.80-0.83 on the 147-subject dataset with LOSO.
"""

import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from typing import Optional
from scripts.data.preprocessing import extract_handcrafted_features


class ClassicalSVMBaseline:
    """SVM baseline with handcrafted EDA features.

    Feature extraction is applied per window, then an SVM with RBF kernel
    is trained under LOSO protocol.
    """

    def __init__(
        self,
        C: float = 1.0,
        kernel: str = "rbf",
        gamma: str = "scale",
        class_weight: str = "balanced",
    ):
        self.pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("svm", SVC(
                C=C, kernel=kernel, gamma=gamma,
                class_weight=class_weight,
                probability=True,
            )),
        ])

    def extract_features(self, scr_windows: np.ndarray, fs: float = 4.0,
                         window_seconds: int = 40) -> np.ndarray:
        """Extract handcrafted features from SCR windows.

        Args:
            scr_windows: (n_windows, n_channels=3, window_samples).
            fs: Sampling frequency (Hz).
            window_seconds: Window length.

        Returns:
            Feature matrix of shape (n_windows, n_features).
        """
        # Use only the SCR channel (index 0)
        scr_data = scr_windows[:, 0, :]

        features_list = []
        for i in range(len(scr_data)):
            feats = extract_handcrafted_features(scr_data[i], fs, window_seconds)
            features_list.append(feats)

        return np.stack(features_list, axis=0)

    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> "ClassicalSVMBaseline":
        """Fit SVM on features extracted from training windows."""
        self.pipeline.fit(X_train, y_train)
        return self

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict class labels."""
        return self.pipeline.predict(X_test)

    def predict_proba(self, X_test: np.ndarray) -> np.ndarray:
        """Predict class probabilities."""
        return self.pipeline.predict_proba(X_test)
