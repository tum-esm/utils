"""Types for interacting with OPUS files.

Credits to Friedrich Klappenbach (ge79wul@mytum.de) for decoding the OPUS file format."""

from __future__ import annotations
from typing import Any, Literal, Optional
import math
import datetime
import pydantic
import tum_esm_utils


class OpusHeader(pydantic.BaseModel):
    """Object that contains all the information in the OPUS file header block."""

    version: int = pydantic.Field(..., ge=0, description="File version")
    dir_pointer: int = pydantic.Field(
        ..., ge=0, description="File pointer to start of OPUS directory"
    )
    max_dir_size: int = pydantic.Field(..., ge=0, description="Maximum number of directory entries")
    dir_size: int = pydantic.Field(..., ge=0, description="Used number of OPUS directory entries")


class OpusParameterBlock(pydantic.BaseModel):
    data: dict[str, Optional[str | float | int]]
    data_types: dict[str, int]
    parameter_order: list[str]
    raw_data: bytes


class OpusDataBlock(pydantic.BaseModel):
    raw_data: bytes


class OpusDirectoryEntry(pydantic.BaseModel):
    """Object that contains all the information in an OPUS directory entry."""

    block_type: int = pydantic.Field(..., description="encoded block type (32 bit mask)")
    block_length: int = pydantic.Field(..., description="block length (32-bit words)")
    block_pointer: int = pydantic.Field(
        ..., description="file pointer to beginning of data/parameter block (bytes)"
    )
    block_category: str = pydantic.Field(
        ..., description="decoded parameter type flag (values from DBSPARM)"
    )


class OpusChannelParameters(pydantic.BaseModel):
    spectrum: dict[str, Any] = pydantic.Field(..., validation_alias="DBTDSTAT")
    instrument: dict[str, Any] = pydantic.Field(..., validation_alias="DBTINSTR")
    acquisition: dict[str, Any] = pydantic.Field(..., validation_alias="DBTAQPAR")
    optics: dict[str, Any] = pydantic.Field(..., validation_alias="DBTPRCPAR")
    sample: dict[str, Any] = pydantic.Field(..., validation_alias="DBTORGPAR")
    fourier_transform: dict[str, Any] = pydantic.Field(..., validation_alias="DBTFTPAR")

    def parse_measurement_datetime(
        self,
        measurement_timestamp_mode: Literal["start", "end"] = "start",
    ) -> datetime.datetime:
        DAT, TIM, DUR = self.spectrum["DAT"], self.spectrum["TIM"], self.instrument["DUR"]
        seconds = float(TIM.split(":")[2].split(" ")[0])
        utc_offset = tum_esm_utils.timing.parse_timezone_string(TIM.split(" ")[-1].strip("()"))
        dt = datetime.datetime(
            year=int(DAT.split("/")[2]),
            month=int(DAT.split("/")[1]),
            day=int(DAT.split("/")[0]),
            hour=int(TIM.split(":")[0]),
            minute=int(TIM.split(":")[1]),
            second=math.floor(seconds),
            microsecond=round((seconds % 1) * 1_000_000),
            tzinfo=datetime.timezone.utc,
        ) - datetime.timedelta(hours=utc_offset)
        if measurement_timestamp_mode == "start":
            dt = dt + datetime.timedelta(seconds=DUR / 2)
        else:
            dt = dt - datetime.timedelta(seconds=DUR / 2)
        return dt
