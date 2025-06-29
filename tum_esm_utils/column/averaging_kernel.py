"""Functions to store, load and apply a column averaging kernel."""

from __future__ import annotations
from typing import Any, Optional
import numpy as np
import tum_esm_utils


class ColumnAveragingKernel:
    """A class to store, load and apply a column averaging kernel."""

    def __init__(
        self,
        szas: np.ndarray[Any, Any],
        pressures: np.ndarray[Any, Any],
        aks: Optional[np.ndarray[Any, Any]] = None,
    ) -> None:
        """Initialize the ColumnAveragingKernel.
        Args:
            szas: The solar zenith angles (SZAs) in degrees.
            pressures: The pressures in hPa.
            aks: The averaging kernels. If None, a zero array is created.
        """

        import scipy.interpolate

        self.szas = szas
        self.pressures = pressures
        self.aks: np.ndarray[Any, Any]
        if aks is not None:
            self.aks = aks
        else:
            self.aks = np.zeros((len(szas), len(pressures)), dtype=np.float64)
        self.spline: Optional[scipy.interpolate.RectBivariateSpline] = None

    def apply(
        self,
        szas: np.ndarray[Any, Any],
        pressures: np.ndarray[Any, Any],
    ) -> np.ndarray[Any, Any]:
        """Compute the averaging kernel for a given set of szas and pressures.

        ```python
        ak.apply(
            szas=np.array([0, 10, 20]),
            pressures=np.array([900, 800, 700])
        )
        ```

        Returns:

        ```
        [
           AK @  0° SZA and 900 hPa,
           AK @ 10° SZA and 800 hPa,
           AK @ 20° SZA and 700 hPa
        ]
        ```
        """

        import scipy.interpolate

        if self.spline is None:
            self.spline = scipy.interpolate.RectBivariateSpline(
                self.szas,
                self.pressures,
                self.aks,
                s=0,
            )
        return self.spline(szas, pressures, grid=False)

    def dump(self, filepath: str) -> None:
        """Dump the ColumnAveragingKernel to a JSON file."""

        assert filepath.endswith(".json"), "Filepath must end with .json"
        tum_esm_utils.files.dump_json_file(
            filepath,
            {
                "pressures": self.pressures.tolist(),
                "szas": self.szas.tolist(),
                "aks": self.aks.tolist(),
            },
            indent=None,
        )

    @staticmethod
    def load(filepath: str) -> ColumnAveragingKernel:
        """Load the ColumnAveragingKernel from a JSON file."""

        assert filepath.endswith(".json"), "Filepath must end with .json"
        d = tum_esm_utils.files.load_json_file(filepath)
        cak = ColumnAveragingKernel(
            pressures=np.array(d["pressures"], dtype=np.float64),
            szas=np.array(d["szas"], dtype=np.float64),
            aks=np.array(d["aks"], dtype=np.float64),
        )
        cak.apply(np.array([]), np.array([]))
        return cak
