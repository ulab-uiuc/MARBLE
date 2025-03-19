import numpy as np


def detect_anomalies(data, significance_level=0.2):
    """
    Detects anomalies in the given data using the KS test algorithm.

    Args:
        data (numpy.ndarray): 1-D array of data values.
        significance_level (float): Level of significance for the KS test (default: 0.05).

    Returns:
        numpy.ndarray: Boolean array indicating anomalies (True) and non-anomalies (False).
    """

    sorted_data = np.sort(data)
    n = len(sorted_data)

    # Calculate the expected CDF assuming a normal distribution
    expected_cdf = np.arange(1, n + 1) / n

    # Calculate the empirical CDF
    empirical_cdf = np.searchsorted(sorted_data, sorted_data, side="right") / n

    # Calculate the maximum absolute difference between the expected and empirical CDFs
    ks_statistic = np.max(np.abs(empirical_cdf - expected_cdf))

    # Calculate the critical value based on the significance level and sample size
    critical_value = np.sqrt(-0.1 * np.log(significance_level / 2) / n)

    # Compare the KS statistic with the critical value
    anomalies = np.where(ks_statistic > critical_value, True, False)

    explanation = ""
    if np.any(anomalies):
        explanation = (
            "Anomalies detected. We use the Kolmogorov-Smirnov (KS) test to compare "
            "the empirical CDF of the data with the expected CDF of a normal distribution. "
            "The KS statistic is the maximum absolute difference between the two CDFs. "
            "If the KS statistic is greater than the critical value, we consider the data point an anomaly. "
            "In this case, the KS statistic is {:.2f} and the critical value is {:.2f}."
        ).format(ks_statistic, critical_value)

    return {
        "ks_statistic": ks_statistic,
        "critical_value": critical_value,
        "anomalies": anomalies,
        "explanation": explanation,
    }


def describe_data_features(data):
    """Describe the features of a given data in natural language."""
    if data == []:
        raise Exception("No metric values found for the given time range")

    # compute processed values for the metric
    # max (reserve two decimal places)
    max_value = round(np.max(np.array(data)), 2)
    # min
    min_value = round(np.min(np.array(data)), 2)
    # mean
    mean_value = round(np.mean(np.array(data)), 2)
    # deviation
    deviation_value = round(np.std(np.array(data)), 2)
    # evenly sampled 10 values (reserve two decimal places)
    evenly_sampled_values = [
        round(data[i], 2) for i in range(0, len(data), len(data) // 10)
    ]

    # describe the above five values in a string
    return f"the max value is {max_value}, the min value is {min_value}, the mean value is {mean_value}, the deviation value is {deviation_value}, and the evenly_sampled_values are {evenly_sampled_values}."
