"""A thin wrapper over the netCDF4 library to make working with NetCDF files easier.

Implements: `NetCDFFile`

This requires you to install this utils library with the optional `netcdf` dependencies:

```bash
pip install "tum_esm_utils[netcdf]"
# or
pdm add "tum_esm_utils[netcdf]"
```"""

from typing import Any, Literal, Optional
import os
import netCDF4 as nc


class NetCDFFile:
    def __init__(
        self,
        filepath: str,
        parallel: bool = False,
        diskless: bool = True,
        mode: Literal["w", "a", "r"] = "w",
    ) -> None:
        """A simple wrapper around netCDF4.Dataset to make the interaction with NetCDF files easier.

        If writing to a new file, it will first write to the filepath+ ".tmp" and  rename it to the final
        filepath when closing the file. This ensures that the final filepath will only exist if the file
        was written completely. In append mode, the filepath is not changes."""

        assert filepath.endswith(".nc"), "Only the .nc file extension is supported"
        self.tmp_filepath = filepath[:-3] + ".tmp.nc"
        self.filepath = filepath
        self.mode = mode

        if mode == "w" and os.path.isfile(self.tmp_filepath):
            os.remove(self.tmp_filepath)

        self.ds = nc.Dataset(
            self.tmp_filepath if mode == "w" else self.filepath,
            mode=mode,
            format="NETCDF4",
            parallel=parallel,
            diskless=diskless,
            persist=True,
        )
        self.dimensions: dict[str, nc.Dimension] = {}
        self.variables: dict[str, nc.Variable[Any]] = {}
        self.attributes: dict[str, str] = {}

        if mode in ["a", "r"]:
            for dim_name, dim in self.ds.dimensions.items():
                self.dimensions[dim_name] = dim
            for var_name, var in self.ds.variables.items():
                self.variables[var_name] = var
            for attr_name in self.ds.ncattrs():
                self.attributes[attr_name] = self.ds.getncattr(attr_name)

    def create_dimension(self, name: str, size: int) -> None:
        """Create a new dimension in the NetCDF file.

        Raises:
            ValueError: If the dimension already exists
            RuntimeError: If the NetCDF file is not opened in write mode."""

        if self.mode == "r":
            raise RuntimeError("Cannot create dimension in read-only mode")

        if name in self.dimensions:
            raise ValueError(f"Dimension {name} already exists in the NetCDF file")

        d = self.ds.createDimension(name, size)
        assert isinstance(d, nc.Dimension)
        self.dimensions[name] = d

    def create_variable(
        self,
        name: str,
        dimensions: tuple[nc.Dimension | str, ...],
        units: str,
        long_name: Optional[str] = None,
        description: Optional[str] = None,
        fill_value: Optional[float | int] = None,
        chunk_dimensions: list[str] = [],
        datatype: Literal["f4", "f8", "i4", "i8"] = "f4",
        zlib: bool = True,
        compression_level: int = 2,
    ) -> None:
        """Create a new variable in the NetCDF file.

        Raises:
            ValueError: If the variable already exists or if a dimension is not found.
            RuntimeError: If the NetCDF file is not opened in write mode."""

        if self.mode == "r":
            raise RuntimeError("Cannot create dimension in read-only mode")

        if name in self.variables:
            raise ValueError(f"Variable {name} already exists in the NetCDF file")

        object_dimensions: list[nc.Dimension] = []
        for dimension in dimensions:
            if isinstance(dimension, str):
                if dimension not in self.dimensions:
                    raise ValueError(f"Dimension {dimension} not found in the NetCDF file")
                object_dimensions.append(self.dimensions[dimension])
            else:
                if dimension.name not in self.dimensions:
                    raise ValueError(f"Dimension {dimension.name} not found in the NetCDF file")
                object_dimensions.append(dimension)

        chunk_sizes = [dimension.size for dimension in object_dimensions]
        for i, dimension in enumerate(object_dimensions):
            if dimension.name in chunk_dimensions:
                chunk_sizes[i] = 1

        var: Any = self.ds.createVariable(  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
            name,
            datatype=datatype,
            dimensions=object_dimensions,
            zlib=zlib and ((len(dimensions) > 1) or (name != object_dimensions[0].name)),
            complevel=compression_level,  # type: ignore
            fill_value=fill_value,
            chunksizes=chunk_sizes if len(chunk_dimensions) > 0 else None,
        )
        var.units = units
        if long_name is not None:
            var.long_name = long_name
        if description is not None:
            var.description = description
        self.variables[name] = var

    def import_dimension(
        self,
        dimension: nc.Dimension,
        new_name: Optional[str] = None,
    ) -> None:
        """Import a dimension from another NetCDF file.

        Raises:
            ValueError: If the dimension already exists.
            RuntimeError: If the NetCDF file is not opened in write mode."""

        if self.mode == "r":
            raise RuntimeError("Cannot import dimension in read-only mode")

        if dimension.name in self.dimensions:
            raise ValueError(f"Dimension {dimension.name} already exists in the NetCDF file")
        self.create_dimension(dimension.name if new_name is None else new_name, dimension.size)

    def import_variable(
        self,
        variable: "nc.Variable[Any]",
        new_name: Optional[str] = None,
        zlib: bool = True,
        compression_level: int = 2,
    ) -> None:
        """Import a variable from another NetCDF file.

        Raises:
            ValueError: If the variable already exists.
            RuntimeError: If the NetCDF file is not opened in write mode."""

        if self.mode == "r":
            raise RuntimeError("Cannot import variable in read-only mode")

        if variable.name in self.variables:
            raise ValueError(f"Variable {variable.name} already exists in the NetCDF file")
        name = variable.name if new_name is None else new_name
        self.create_variable(
            name=name,
            dimensions=variable.dimensions,
            units=str(variable.units),
            long_name=variable.long_name if hasattr(variable, "long_name") else None,  # pyright: ignore[reportUnknownArgumentType]
            description=variable.description if hasattr(variable, "description") else None,  # pyright: ignore[reportUnknownArgumentType]
            fill_value=float(variable.get_fill_value()),
            zlib=zlib,
            compression_level=compression_level,
        )
        self.variables[name][:] = variable[:]

    def add_attribute(self, key: str, value: str) -> None:
        """Add a global attribute to the NetCDF file.

        Raises:
            ValueError: If the attribute already exists.
            RuntimeError: If the NetCDF file is not opened in write mode."""

        if self.mode == "r":
            raise RuntimeError("Cannot add attribute in read-only mode")

        if key in self.attributes:
            raise ValueError(f"Attribute {key} already exists in the NetCDF file")
        self.attributes[key] = value
        self.ds.setncattr(key, value)

    def close(self) -> None:
        """Close the NetCDF file, possibly renaming the temporary file to the final filepath."""

        self.ds.close()
        if self.mode == "w":
            if os.path.isfile(self.filepath):
                os.remove(self.filepath)
            os.rename(self.tmp_filepath, self.filepath)

        del self

    def __getitem__(self, key: str) -> "nc.Variable[Any]":
        """Get a variable from the NetCDF file."""
        return self.variables[key]
