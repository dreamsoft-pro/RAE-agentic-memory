"""Extended unit tests for importance decay utilities."""

import math
from datetime import timedelta
import pytest
from rae_core.scoring.decay import time_to_threshold

class TestTimeToThresholdExtended:
    """Test suite for time_to_threshold function."""

    def test_standard_decay_calculation(self):
        """Standard calculation: from 1.0 to 0.5 with rate 0.1."""
        # 0.5 = 1.0 * e^(-0.1 * t)
        # t = ln(2) / 0.1
        expected_days = math.log(2) / 0.1
        tt = time_to_threshold(1.0, 0.5, 0.1)
        assert tt.total_seconds() / (24 * 3600) == pytest.approx(expected_days)

    def test_slow_decay_calculation(self):
        """Standard calculation: from 1.0 to 0.1 with rate 0.05."""
        # 0.1 = 1.0 * e^(-0.05 * t)
        # t = ln(10) / 0.05
        expected_days = math.log(10) / 0.05
        tt = time_to_threshold(1.0, 0.1, 0.05)
        assert tt.total_seconds() / (24 * 3600) == pytest.approx(expected_days)

    def test_already_below_threshold(self):
        """Edge case: initial importance is already below threshold."""
        assert time_to_threshold(0.4, 0.5, 0.1) == timedelta(0)

    def test_exactly_at_threshold(self):
        """Edge case: initial importance is exactly at threshold."""
        assert time_to_threshold(0.5, 0.5, 0.1) == timedelta(0)

    def test_zero_decay_rate(self):
        """Edge case: decay rate is zero (importance never changes)."""
        assert time_to_threshold(1.0, 0.5, 0.0) == timedelta(0)

    def test_negative_decay_rate(self):
        """Edge case: decay rate is negative (importance increases)."""
        assert time_to_threshold(1.0, 0.5, -0.1) == timedelta(0)

    @pytest.mark.parametrize("initial, threshold, rate, expected_days", [
        (0.8, 0.2, 0.2, math.log(4) / 0.2),
        (0.9, 0.3, 0.1, math.log(3) / 0.1),
    ])
    def test_parametrized_cases(self, initial, threshold, rate, expected_days):
        """Test various parameter combinations."""
        tt = time_to_threshold(initial, threshold, rate)
        assert tt.total_seconds() / (24 * 3600) == pytest.approx(expected_days)
