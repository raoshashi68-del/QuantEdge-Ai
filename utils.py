# Utility functions
"""
==========================================================
Utility Functions
==========================================================
"""

from datetime import datetime


def now():

    return datetime.now()


def timestamp():

    return now().strftime("%Y-%m-%d %H:%M:%S")


def today():

    return now().date()


def clamp(value, minimum, maximum):

    return max(minimum, min(value, maximum))


def safe_div(a, b):

    if b == 0:

        return 0

    return a / b


def percentage_change(current, previous):

    if previous == 0:

        return 0

    return ((current - previous) / previous) * 100