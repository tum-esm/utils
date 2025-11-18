import time
import numpy as np
import pytest
import tum_esm_utils.rebinning


@pytest.mark.order(3)
@pytest.mark.quick
def test_rebin_1d() -> None:
    a = np.array([1, 2, 3, 4])

    b1 = tum_esm_utils.rebinning.rebin_1d(a, 1)
    b1_expected = np.array([10])
    assert np.allclose(b1, b1_expected), f"Expected {b1_expected}, got {b1}"
    assert np.isclose(np.sum(a), np.sum(b1)), f"Sum mismatch: {np.sum(a)} vs {np.sum(b1)}"

    b2 = tum_esm_utils.rebinning.rebin_1d(a, 2)
    b2_expected = np.array([3, 7])
    assert np.allclose(b2, b2_expected), f"Expected {b2_expected}, got {b2}"
    assert np.isclose(np.sum(a), np.sum(b2)), f"Sum mismatch: {np.sum(a)} vs {np.sum(b2)}"

    b3 = tum_esm_utils.rebinning.rebin_1d(a, 3)
    b3_expected = np.array([1.6666, 3.3333, 5])
    assert np.allclose(b3, b3_expected, atol=0.001), f"Expected {b3_expected}, got {b3}"
    assert np.isclose(np.sum(a), np.sum(b3)), f"Sum mismatch: {np.sum(a)} vs {np.sum(b3)}"

    b4 = tum_esm_utils.rebinning.rebin_1d(a, 4)
    b4_expected = np.array([1, 2, 3, 4])
    assert np.allclose(b4, b4_expected), f"Expected {b4_expected}, got {b4}"
    assert np.isclose(np.sum(a), np.sum(b4)), f"Sum mismatch: {np.sum(a)} vs {np.sum(b4)}"

    b5 = tum_esm_utils.rebinning.rebin_1d(a, 5)
    b5_expected = np.array([0.8, 1.4, 2, 2.6, 3.2])
    assert np.allclose(b5, b5_expected), f"Expected {b5_expected}, got {b5}"
    assert np.isclose(np.sum(a), np.sum(b5)), f"Sum mismatch: {np.sum(a)} vs {np.sum(b5)}"

    b6 = tum_esm_utils.rebinning.rebin_1d(a, 6)
    b6_expected = np.array([0.6666, 1, 1.3333, 2, 2.3333, 2.6666])
    assert np.allclose(b6, b6_expected, atol=0.001), f"Expected {b6_expected}, got {b6}"
    assert np.isclose(np.sum(a), np.sum(b6)), f"Sum mismatch: {np.sum(a)} vs {np.sum(b6)}"


@pytest.mark.order(3)
@pytest.mark.quick
def test_rebin_2d() -> None:
    a = np.array(
        [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
            [17, 18, 19, 20],
            [21, 22, 23, 24],
        ]
    )

    b23 = tum_esm_utils.rebinning.rebin_2d(a, new_x_bins=2, new_y_bins=3)
    b23_expected = np.array(
        [
            [1 + 2 + 5 + 6, 3 + 4 + 7 + 8],
            [9 + 10 + 13 + 14, 11 + 12 + 15 + 16],
            [17 + 18 + 21 + 22, 19 + 20 + 23 + 24],
        ]
    )
    assert np.allclose(b23, b23_expected), f"Expected {b23_expected}, got {b23}"

    b13 = tum_esm_utils.rebinning.rebin_2d(a, new_x_bins=1, new_y_bins=3)
    b13_expected = np.array(
        [
            [1 + 2 + 5 + 6 + 3 + 4 + 7 + 8],
            [9 + 10 + 13 + 14 + 11 + 12 + 15 + 16],
            [17 + 18 + 21 + 22 + 19 + 20 + 23 + 24],
        ]
    )
    assert np.allclose(b13, b13_expected), f"Expected {b13_expected}, got {b13}"

    b22 = tum_esm_utils.rebinning.rebin_2d(a, new_x_bins=2, new_y_bins=2)
    b22_expected = np.array(
        [
            [1 + 2 + 5 + 6 + 9 + 10, 3 + 4 + 7 + 8 + 11 + 12],
            [13 + 14 + 17 + 18 + 21 + 22, 15 + 16 + 19 + 20 + 23 + 24],
        ]
    )
    assert np.allclose(b22, b22_expected), f"Expected {b22_expected}, got {b22}"

    b12 = tum_esm_utils.rebinning.rebin_2d(a, new_x_bins=1, new_y_bins=2)
    b12_expected = np.array(
        [
            [1 + 2 + 5 + 6 + 9 + 10 + 3 + 4 + 7 + 8 + 11 + 12],
            [13 + 14 + 17 + 18 + 21 + 22 + 15 + 16 + 19 + 20 + 23 + 24],
        ]
    )
    assert np.allclose(b12, b12_expected), f"Expected {b12_expected}, got {b12}"

    b11 = tum_esm_utils.rebinning.rebin_2d(a, new_x_bins=1, new_y_bins=1)
    b11_expected = np.array([[np.sum(a)]])
    assert np.allclose(b11, b11_expected), f"Expected {b11_expected}, got {b11}"

    # test rebinning performance

    large_a = np.random.rand(1000, 1000)
    t1 = time.time()
    tum_esm_utils.rebinning.rebin_2d(large_a, new_x_bins=100, new_y_bins=100)
    t2 = time.time()
    print(f"Rebinning 1000x1000 to 100x100 took {t2 - t1:.4f} seconds.")
    # Rebinning 1000x1000 to 100x100 took 0.0032 seconds (on an M4 Pro Chip)

    large_a = np.random.rand(100, 100)
    t1 = time.time()
    tum_esm_utils.rebinning.rebin_2d(large_a, new_x_bins=1000, new_y_bins=1000)
    t2 = time.time()
    print(f"Rebinning 100x100 to 1000x1000 took {t2 - t1:.4f} seconds.")
    # Rebinning 100x100 to 1000x1000 took 0.0062 seconds (on an M4 Pro Chip)

    # assert False comment out to see the performance prints
