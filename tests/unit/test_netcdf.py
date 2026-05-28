import pytest
import tempfile
import os
import numpy as np
import netCDF4 as nc
import scipy.ndimage
import tum_esm_utils.files
from tum_esm_utils.netcdf import NetCDFFile

PROJECT_DIR = tum_esm_utils.files.get_parent_dir_path(__file__, current_depth=2)


@pytest.mark.order(3)
@pytest.mark.quick
def test_netcdffile_create_and_read() -> None:
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create a NetCDF file in a temporary directory
        filepath = os.path.join(tmpdirname, "test.nc")
        ncfile = NetCDFFile(str(filepath), mode="w")

        assert not os.path.exists(filepath)
        assert os.path.exists(filepath[:-3] + ".tmp.nc")

        # Create dimensions
        ncfile.create_dimension("time", 10)
        ncfile.create_dimension("lat", 5)
        ncfile.create_dimension("lon", 5)

        # Create variable
        ncfile.create_variable(
            name="temperature",
            dimensions=("time", "lat", "lon"),
            units="K",
            long_name="Air temperature",
            description="Synthetic temperature data",
            fill_value=-9999.0,
            datatype="f4",
        )

        # Write data
        data = np.random.rand(10, 5, 5).astype(np.float32)
        ncfile.variables["temperature"][:] = data

        # Add attribute
        ncfile.add_attribute("title", "Test NetCDF File")

        # Close file
        ncfile.close()

        # Reopen and check contents
        ncfile2 = nc.Dataset(str(filepath), mode="a")
        assert "temperature" in ncfile2.variables
        assert ncfile2.variables["temperature"].shape == (10, 5, 5)
        np.testing.assert_array_almost_equal(ncfile2.variables["temperature"][:], data)
        assert ncfile2.getncattr("title") == "Test NetCDF File"
        ncfile2.close()


@pytest.mark.order(3)
@pytest.mark.quick
def test_netcdffile_import_dimension_and_variable() -> None:
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create source NetCDF file
        src_filepath = os.path.join(tmpdirname, "src.nc")
        src_nc = NetCDFFile(str(src_filepath), mode="w")
        src_nc.create_dimension("x", 4)
        src_nc.create_variable(
            name="foo", dimensions=("x",), units="1", fill_value=0, datatype="i4"
        )
        src_nc.variables["foo"][:] = np.arange(4)
        src_nc.close()

        # Open source and target files
        src_nc = NetCDFFile(str(src_filepath), mode="r")
        tgt_filepath = os.path.join(tmpdirname, "tgt.nc")
        tgt_nc = NetCDFFile(str(tgt_filepath), mode="w")

        # Import dimension and variable
        tgt_nc.import_dimension(src_nc.dimensions["x"])
        tgt_nc.import_variable(src_nc.variables["foo"])
        tgt_nc.close()
        src_nc.close()

        # Check imported data
        tgt_nc = NetCDFFile(str(tgt_filepath), mode="r")
        assert "x" in tgt_nc.dimensions
        assert "foo" in tgt_nc.variables
        np.testing.assert_array_equal(tgt_nc.variables["foo"][:], np.arange(4))
        tgt_nc.close()


@pytest.mark.order(3)
@pytest.mark.quick
def test_netcdffile_append() -> None:
    with tempfile.TemporaryDirectory() as tmpdirname:
        fp = os.path.join(tmpdirname, "file.nc")

        ds1 = tum_esm_utils.netcdf.NetCDFFile(fp, mode="w")
        ds1.create_dimension("time", 5)
        ds1.create_variable("temperature", dimensions=("time",), units="K", datatype="f8")
        ds1["temperature"][:] = np.random.rand(5) * 300  # Random temperatures in Kelvin
        ds1.close()

        ds2 = tum_esm_utils.netcdf.NetCDFFile(fp, mode="a")
        ds2.create_variable("pressure", dimensions=("time",), units="hPa", datatype="f8")
        ds2["pressure"][:] = np.random.rand(5) * 1000  # Random pressures in hPa
        ds2.close()

        ds3 = tum_esm_utils.netcdf.NetCDFFile(fp, mode="r")
        assert "temperature" in ds3.variables
        assert "pressure" in ds3.variables
        assert np.nansum(ds3["temperature"][:]) > 1
        assert np.nansum(ds3["pressure"][:]) > 1
        ds3.close()


@pytest.mark.order(3)
@pytest.mark.slow
@pytest.mark.skipif(os.name != "posix", reason="Not fully supported on Windows")
def test_netcdffile_compression() -> None:
    with tempfile.TemporaryDirectory() as tmpdirname:
        random_temp = np.random.normal(loc=300, scale=10, size=(10, 50, 50))
        random_temp = scipy.ndimage.gaussian_filter(random_temp, sigma=5)
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
            for compression_level in [1, 5, 9]:
                a = NetCDFFile(
                    os.path.join(tmpdirname, f"test-{compression_type}-{compression_level:02d}.nc"),
                    mode="w",
                )
                a.create_dimension("time", 10)
                a.create_dimension("lat", 50)
                a.create_dimension("lon", 50)
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
