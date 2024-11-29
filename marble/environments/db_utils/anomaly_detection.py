from typing import Any, Tuple

import numpy as np


def detect_anomalies(
    data: np.ndarray[Any, np.dtype[np.float64]],
    significance_level: float = 0.2
) -> Tuple[float, np.ndarray[Any, np.dtype[np.bool_]]]:
    """
    Detects anomalies in the given data using the KS test algorithm.

    Args:
        data (numpy.ndarray): 1-D array of data values.
        significance_level (float): Level of significance for the KS test (default: 0.2).

    Returns:
        Tuple[float, numpy.ndarray]:
            - KS statistic (float): The maximum absolute difference between empirical and expected CDFs.
            - Boolean array (numpy.ndarray): Array indicating anomalies (True) and non-anomalies (False).
    """
    sorted_data: np.ndarray[Any, np.dtype[np.float64]] = np.sort(data)
    n: int = len(sorted_data)

    # Calculate the expected CDF assuming a normal distribution
    expected_cdf: np.ndarray[Any, np.dtype[np.float64]] = np.arange(1, n + 1) / n

    # Calculate the empirical CDF
    empirical_cdf: np.ndarray[Any, np.dtype[np.float64]] = np.searchsorted(sorted_data, sorted_data, side='right') / n

    # Calculate the maximum absolute difference between the expected and empirical CDFs
    ks_statistic: float = np.max(np.abs(empirical_cdf - expected_cdf))

    # Calculate the critical value based on the significance level and sample size
    critical_value: float = np.sqrt(-0.1 * np.log(significance_level / 2) / n)

    # Compare the KS statistic with the critical value
    anomalies: np.ndarray[Any, np.dtype[np.bool_]] = np.full_like(data, ks_statistic > critical_value, dtype=bool)

    return ks_statistic, anomalies
