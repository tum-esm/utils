import os
import numpy as np
import tum_esm_utils

if __name__ == "__main__":
    # add gaussian blur on top of array to make it more realistic
    from scipy.ndimage import gaussian_filter

    random_temp = np.random.normal(loc=300, scale=10, size=(10, 50, 50))
    random_temp = gaussian_filter(random_temp, sigma=5)

    for compression_type in [
        "zlib",
        "szip",
        "zstd",
        "bzip2",
        "blosc_lz",
        "blosc_lz4",
        "blosc_lz4hc",
        "blosc_zlib",
        "blosc_zstd",
    ]:
        last_good_compression_level: int = 1
        for compression_level in range(1, 30):
            a = tum_esm_utils.netcdf.NetCDFFile(
                tum_esm_utils.files.rel_to_abs_path(
                    f"./test-{compression_type}-{compression_level:02d}.nc"
                ),
                mode="w",
            )
            a.create_dimension("time", 10)
            a.create_dimension("lat", 50)
            a.create_dimension("lon", 50)
            try:
                a.create_variable(
                    "temperature",
                    dimensions=("time", "lat", "lon"),
                    units="K",
                    datatype="f8",
                    compression=compression_type,  # type: ignore
                    compression_level=compression_level,
                    zlib=True,  # type: ignore
                )
                a.variables["temperature"][:] = random_temp
                a.close()
                last_good_compression_level = compression_level
            except Exception:
                a.discard()

        for i in range(1, last_good_compression_level):
            os.remove(f"test-{compression_type}-{i:02d}.nc")
