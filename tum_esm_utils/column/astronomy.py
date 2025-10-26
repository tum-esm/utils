from typing import Any
import datetime
import tum_esm_utils.files


class Astronomy:
    """Astronomy utilities."""

    def __init__(self) -> None:
        """Initializes the Astronomy class, downloads the latest `de421.bsp` dataset."""

        import skyfield.api # pyright: ignore[reportMissingTypeStubs]

        self.planets: Any = skyfield.api.Loader(tum_esm_utils.files.rel_to_abs_path("."))(
            "de421.bsp"
        )
        self.timescale = skyfield.api.load.timescale() # pyright: ignore[reportUnknownMemberType]
        self.earth: Any = self.planets["Earth"] # pyright: ignore[reportUnknownMemberType]
        self.sun: Any = self.planets["Sun"] # pyright: ignore[reportUnknownMemberType]

    def get_sun_position(
        self,
        lat: float,
        lon: float,
        alt_asl: float,
        dt: datetime.datetime,
    ) -> tuple[float, float]:
        """Computes current sun elevation and azimuth in degrees."""

        import skyfield.api # pyright: ignore[reportMissingTypeStubs]

        skyfield_dt = self.timescale.from_datetime(dt) # pyright: ignore[reportUnknownMemberType]
        skyfield_location = self.earth + skyfield.api.wgs84.latlon( # pyright: ignore[reportUnknownMemberType]
            latitude_degrees=lat,
            longitude_degrees=lon,
            elevation_m=alt_asl,
        )
        altitude, azimuth, _ = (
            skyfield_location.at(skyfield_dt).observe(self.sun).apparent().altaz()
        )
        return float(altitude.degrees), float(azimuth.degrees)
