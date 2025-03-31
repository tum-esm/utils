"""Functions to read NCEP profiles."""

import polars as pl


# fmt: off
map_columns = [
    "Height", "Temp", "Pressure", "Density", "h2o", "hdo", "co2", "n2o", "co", "ch4", "hf", "o2",
    "gravity",
]
mod_columns = [
    "Pressure", "Temperature", "Height", "MMW", "H2O", "RH", "EPV", "PT", "EqL", "O3", "CO",
]
vmr_columns = [
    "Altitude", "H2O", "CO2", "O3", "N2O", "CO", "CH4", "O2", "NO", "SO2", "NO2", "NH3", "HNO3",
    "OH", "HF", "HCl", "HBr", "HI", "ClO", "OCS", "H2CO", "HOCl", "HO2", "H2O2", "HONO", "HO2NO2",
    "N2O5", "ClNO3", "HCN", "CH3F", "CH3Cl", "CF4", "CCl2F2", "CCl3F", "CH3CCl3", "CCl4", "COF2",
    "COFCl", "C2H6", "C2H4", "C2H2", "N2", "CHClF2", "COCl2", "CH3Br", "CH3I", "HCOOH", "H2S",
    "CHCl2F", "HDO", "SF6", "F113", "ClCN", "F142b", "dust_m", "PH3", "CH3OH", "CH3SH", "CH3CHO",
    "CH3CN", "PAN", "NF3", "ClOOCl", "ClClO2", "ClOClO", "CHF3", "f141b", "CH3COOH", "cirrus6",
    "cirrus15", "C3H8", "D2O", "sa_venus", "C6H6", "C3H6", "CH3COCH3", "CFH2CF3", "n-C4H10",
    "C5H8", "LUFT",
]
# fmt: on

mod_column_widths = [10, 14, 11, 11, 14, 10, 14, 12, 11, 13, 13]
mod_column_offsets = [0, *([sum(mod_column_widths[:i]) for i in range(1, len(mod_columns))])]
vmr_column_widths = [9, *([11] * (len(vmr_columns) - 2)), 10]
vmr_column_offsets = [0, *([sum(vmr_column_widths[:i]) for i in range(1, len(vmr_columns))])]


def load_ggg2020_map(filepath: str) -> pl.DataFrame:
    """Load the Atmospheric profile from a GGG2020 map file."""
    return (
        pl.read_csv(
            filepath,
            has_header=False,
            skip_rows=12,
            infer_schema=False,
            separator="v",
            schema={"full_str": pl.Utf8},
            n_threads=1,
        )
        .lazy()
        .with_columns(pl.col("full_str").str.split(",").alias("column_list"))
        .drop("full_str")
        .with_columns(
            *[
                pl.col("column_list")
                .list.get(i)
                .str.strip_chars(" ")
                .cast(pl.Float64)
                .alias(column)
                for i, column in enumerate(map_columns)
            ]
        )
        .drop("column_list")
        .collect()
    )


def load_ggg2020_mod(filepath: str) -> pl.DataFrame:
    """Load the Atmospheric profile from a GGG2020 mod file."""

    return (
        pl.read_csv(
            filepath,
            has_header=False,
            skip_rows=7,
            infer_schema=False,
            schema={"full_str": pl.Utf8},
            n_threads=1,
        )
        .lazy()
        .with_columns(
            [
                pl.col("full_str")
                .str.slice(offset, width)
                .str.strip_chars()
                .cast(pl.Float64)
                .alias(column)
                for column, offset, width in zip(mod_columns, mod_column_offsets, mod_column_widths)
            ]
        )
        .drop("full_str")
        .collect()
    )


def load_ggg2020_vmr(filepath: str) -> pl.DataFrame:
    """Load the Atmospheric profile from a GGG2020 vmr file."""
    return (
        pl.read_csv(
            filepath,
            has_header=False,
            skip_rows=8,
            infer_schema=False,
            schema={"full_str": pl.Utf8},
            n_threads=1,
        )
        .lazy()
        .with_columns(
            [
                pl.col("full_str")
                .str.slice(offset, width)
                .str.strip_chars()
                .cast(pl.Float64)
                .alias(column)
                for column, offset, width in zip(vmr_columns, vmr_column_offsets, vmr_column_widths)
            ]
        )
        .drop("full_str")
        .collect()
    )
