from drift.metrics import psi


def test_psi_zero_for_identical_distributions() -> None:
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert psi(values, values) == 0.0


def test_psi_positive_for_shifted_distributions() -> None:
    expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    actual = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert psi(expected, actual) > 0.0
