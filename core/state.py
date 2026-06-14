"""
==========================================================

System States

==========================================================
"""

from enum import Enum


class CandidateState(str, Enum):

    CREATED = "CREATED"

    DATA_READY = "DATA_READY"

    FEATURES_READY = "FEATURES_READY"

    FILTERED = "FILTERED"

    RANKED = "RANKED"

    READY = "READY"

    REJECTED = "REJECTED"

    EXECUTED = "EXECUTED"

    MONITORING = "MONITORING"

    EXITED = "EXITED"

    ARCHIVED = "ARCHIVED"


class PositionState(str, Enum):

    OPEN = "OPEN"

    PROTECTED = "PROTECTED"

    TRAILING = "TRAILING"

    SCALE_OUT = "SCALE_OUT"

    CLOSED = "CLOSED"