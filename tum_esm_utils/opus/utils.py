"""Credits to Friedrich Klappenbach (ge79wul@mytum.de) for decoding the OPUS file format."""

from __future__ import annotations
from typing import Optional, TypeVar
import numpy as np
import numpy.typing as npt
import io
import struct
from . import types

# Define constants

FILE_MAGIC = b"\n\n\xfe\xfe"  # magic sequence at beginning of Opus file
# Definitions for directory block type bit patterns

# Parameter type flag
DBSPARM = 4  # bit shift
DBMPARM = 63  # bit mask
DBFPARM: list[str] = [
    "",  # undefined
    "DBTDSTAT",  # data status parameter (DataParameters )
    "DBTINSTR",  # instrument status parameters
    "DBTAQPAR",  # standard acquisition parameters
    "DBTFTPAR",  # FT-Parameters
    "DBTPLTPAR",  # plot- and display parameters
    "DBTPRCPAR",  # processing parameters (Optic parameters)
    "DBTGCPAR",  # GC-parameters
    "DBTLIBPAR",  # library search parameters
    "DBTCOMPAR",  # communication parameters
    "DBTORGPAR",  # sample origin parameter (Sample Parameters)
] + [f"DBTPARM{i}" for i in range(11, DBMPARM + 1)]
assert len(DBFPARM) == DBMPARM + 1


def read_opus_header(f: io.BufferedReader) -> types.OpusHeader:
    """Read OPUS file header from a file."""

    magic_sequence = f.read(4)
    if magic_sequence != FILE_MAGIC:
        raise RuntimeError(f'Magic sequence not found, found {magic_sequence.decode()}" instead')
    x = struct.unpack("<dIII", f.read(struct.calcsize("<dIII")))
    assert len(x) >= 4
    return types.OpusHeader(
        version=x[0],
        dir_pointer=x[1],
        max_dir_size=x[2],
        dir_size=x[3],
    )


def read_opus_dir_entry(f: io.BufferedReader) -> types.OpusDirectoryEntry:
    """Read a single OPUS directory entry object from file at current position."""

    fmt = "<III"
    x = struct.unpack(fmt, f.read(struct.calcsize(fmt)))
    assert len(x) == 3
    block_type = x[0]
    block_length = x[1]
    block_pointer = x[2]
    assert isinstance(block_type, int)
    assert isinstance(block_length, int)
    assert isinstance(block_pointer, int)

    return types.OpusDirectoryEntry(
        block_type=block_type,
        block_length=block_length,
        block_pointer=block_pointer,
        block_category=DBFPARM[(block_type >> DBSPARM) & DBMPARM],
    )


T = TypeVar("T", types.OpusParameterBlock, types.OpusDataBlock)


def read_opus_block(
    f: io.BufferedReader,
    opus_directory_entry: types.OpusDirectoryEntry,
    expected_block_type: type[T],
) -> T:
    f.seek(opus_directory_entry.block_pointer)
    raw_data = f.read(4 * opus_directory_entry.block_length)

    block: types.OpusParameterBlock | types.OpusDataBlock
    if opus_directory_entry.block_category == "":
        block = types.OpusDataBlock(raw_data=raw_data)
        if not isinstance(block, expected_block_type):
            raise RuntimeError(f"Expected a {expected_block_type}, but got a {type(block)}")
        return block

    data: dict[str, Optional[int | float | str]] = {}
    data_types: dict[str, int] = {}
    parameter_order: list[str] = []

    offset = 0  # Byte offset from beginning of block
    fmt1 = "<4shh"  # Initial format string: 4-byte string, 2 short int (little endian)
    while offset <= (len(raw_data) - struct.calcsize(fmt1)):
        # rs: seserved space in 16 bit units
        (pname, ptype, rs) = struct.unpack_from(fmt1, raw_data, offset)
        assert isinstance(pname, bytes)
        assert isinstance(ptype, int)
        assert isinstance(rs, int)

        parameter_name = pname[:-1].decode("utf-8")  # Remove '\0' terminator
        offset += struct.calcsize(fmt1)
        value: Optional[int | float | str] = None

        # Try to read the following values
        if rs > 0:
            # INT32 (little endian)
            if ptype == 0:
                fmt2 = "<i"
                raw_value = struct.unpack_from("<i", raw_data, offset)
                assert isinstance(raw_value[0], int)
                value = raw_value[0]

            # REAL64 (little endian)
            elif ptype == 1:
                fmt2 = "<d"
                raw_value = struct.unpack_from(fmt2, raw_data, offset)
                assert isinstance(raw_value[0], float)
                value = raw_value[0]

            # STRING, ENUM or SENUM
            else:
                fmt2 = ("<%ds") % (2 * rs)
                raw_value = struct.unpack_from(fmt2, raw_data, offset)
                assert isinstance(raw_value[0], bytes)
                value = raw_value[0][:-1].decode("utf-8").replace("\x00", "")

            offset += struct.calcsize(fmt2)

        # Store decoded parameter value
        data[parameter_name] = value
        data_types[parameter_name] = ptype
        parameter_order.append(parameter_name)

    block = types.OpusParameterBlock(
        data=data,
        data_types=data_types,
        parameter_order=parameter_order,
        raw_data=raw_data,
    )
    if not isinstance(block, expected_block_type):
        raise RuntimeError(f"Expected a {expected_block_type}, but got a {type(block)}")
    return block


def read_interferogram(
    f: io.BufferedReader,
    channel_parameters: list[types.OpusChannelParameters],
    ifg_opus_dirs: list[types.OpusDirectoryEntry],
    read_all_channels: bool = True,
) -> npt.NDArray[np.float64]:
    if len(channel_parameters) != len(ifg_opus_dirs):
        raise RuntimeError("Number of channel parameters and interferogram blocks do not match!")

    if len(channel_parameters) == 0:
        raise RuntimeError("No channel parameters found!")

    if not read_all_channels:
        channel_parameters = channel_parameters[:1]
        ifg_opus_dirs = ifg_opus_dirs[:1]

    spectrum_length = channel_parameters[0].spectrum["NPT"]
    for channel_parameter in channel_parameters[1:]:
        if channel_parameter.spectrum["NPT"] != spectrum_length:
            raise RuntimeError("The interferograms don't have the same length!")

    if len(ifg_opus_dirs) not in [1, 2]:
        raise RuntimeError(f"Invalid number of interferogram blocks found: {len(ifg_opus_dirs)}")

    for ifg_opus_dir in ifg_opus_dirs:
        if ifg_opus_dir.block_length != spectrum_length:
            raise RuntimeError(
                f"Interferogram block has length {ifg_opus_dir.block_length}, "
                f"but expected {spectrum_length}"
            )

    full_ifg = np.zeros(
        shape=(len(ifg_opus_dirs), spectrum_length),
        dtype=np.float64,
    )
    for channel_index in range(len(ifg_opus_dirs)):
        channel_ifg = np.multiply(
            np.array(
                struct.unpack_from(
                    f"<{spectrum_length}f",
                    read_opus_block(f, ifg_opus_dirs[0], types.OpusDataBlock).raw_data,
                    offset=0,
                )
            ),
            channel_parameters[channel_index].spectrum["CSF"],
        )
        full_ifg[channel_index, :] = channel_ifg.copy()

    return full_ifg
