"""
==========================================================

QuantEdge AI

Math Utilities

Common mathematical functions used across the project.

==========================================================
"""

import math


def clamp(value, minimum, maximum):
    """
    Restrict value between minimum and maximum.
    """
    return max(minimum, min(value, maximum))


def safe_divide(numerator, denominator, default=0.0):
    """
    Safe division avoiding ZeroDivisionError.
    """
    if denominator == 0:
        return default
    return numerator / denominator


def percentage_change(old_value, new_value):
    """
    Calculate percentage change.
    """
    if old_value == 0:
        return 0.0

    return ((new_value - old_value) / old_value) * 100


def annualize_time(days):
    """
    Convert days to fraction of a year.
    """
    return days / 365.0


def round_price(price, decimals=2):
    """
    Round price.
    """
    return round(price, decimals)


def sigmoid(x):
    """
    Logistic sigmoid.
    """
    try:
        return 1.0 / (1.0 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0


def normalize(value, minimum, maximum):
    """
    Normalize to [0,1].
    """
    if maximum <= minimum:
        return 0.0

    value = clamp(value, minimum, maximum)

    return (value - minimum) / (maximum - minimum)


def standardize(value, mean, std):
    """
    Z-score standardization.
    """
    if std == 0:
        return 0.0

    return (value - mean) / std


def risk_reward(entry, target, stop):
    """
    Calculate Risk:Reward ratio.
    """
    reward = target - entry
    risk = entry - stop

    if risk <= 0:
        return 0.0

    return reward / risk


def expected_value(probability, reward, risk):
    """
    Expected value.

    probability should be between 0 and 1.
    """

    probability = clamp(probability, 0.0, 1.0)

    return (
        probability * reward
        -
        (1 - probability) * risk
    )


def midpoint(bid, ask):
    """
    Mid price.
    """

    if bid <= 0 or ask <= 0:
        return 0.0

    return (bid + ask) / 2


def spread_percent(bid, ask):
    """
    Bid-ask spread percentage.
    """

    mid = midpoint(bid, ask)

    if mid == 0:
        return 100.0

    return ((ask - bid) / mid) * 100


def annualized_volatility(std, periods_per_year):
    """
    Annualize volatility.
    """

    return std * math.sqrt(periods_per_year)