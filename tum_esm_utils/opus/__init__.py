"""Functions for interacting with OPUS files.

Implements: `OpusFile`.

Read https://tccon-wiki.caltech.edu/Main/I2SAndOPUSHeaders for more information
about the file parameters. This requires you to install this utils library with
the optional `opus` dependency:

```bash
pip install "tum_esm_utils[opus]"
# or
pdm add "tum_esm_utils[opus]"
```

Credits to Friedrich Klappenbach (ge79wul@mytum.de) for decoding the OPUS file
format."""

from __future__ import annotations
from typing import Optional, Literal
import numpy as np
import numpy.typing as npt
import datetime
import pydantic

from . import types, utils


class OpusFile(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    header: types.OpusHeader
    channel_parameters: list[types.OpusChannelParameters]
    measurement_times: list[datetime.datetime]
    interferogram: Optional[npt.NDArray[np.float64]] = pydantic.Field(default=None, exclude=True)

    # serialization of measurement times
    @pydantic.field_serializer("measurement_times")
    def serialize_measurement_times(self, measurement_times: list[datetime.datetime]) -> list[str]:
        return [t.isoformat() for t in measurement_times]

    @staticmethod
    def read(
        filepath: str,
        measurement_timestamp_mode: Literal["start", "end"] = "start",
        interferogram_mode: Literal["skip", "validate", "read"] = "read",
        read_all_channels: bool = True,
    ) -> OpusFile:
        """Read an interferogram file.

        Args:
            filepath:                   Path to the OPUS file.
            measurement_timestamp_mode: Whether the timestamps in the interferograms
                                        indicate the start or end of the measurement
            interferogram_mode:         How to handle the interferogram data. "skip"
                                        will not read the interferogram data, "validate"
                                        will read the first and last block to check
                                        for errors during writing, "read" will read
                                        the entire interferogram. "read" takes about
                                        11-12 times longer than "skip", "validate" is
                                        about 20% slower than "skip".
            read_all_channels:          Whether to read all channels in the file or
                                        only the first one.

        Returns:
            An OpusFile object, optionally containing the interferogram data (in read mode)
        """

        # what to copy when only manipulating the interferogram
        # 4 (MAGIC) + struct.calcsize('<dIII') + len(opus_dirs) * struct.calcsize('<III')
        # for each opus dirs:
        # f.seek(opus_directory_entry.block_pointer)
        # f.read(4 * opus_directory_entry.block_length)

        with open(filepath, "rb") as f:
            opus_header = utils.read_opus_header(f)
            f.seek(opus_header.dir_pointer)
            opus_dirs = [utils.read_opus_dir_entry(f) for _ in range(opus_header.dir_size)]

            block_indices: dict[
                str,
                list[int],
            ] = {
                "": [],
                "DBTDSTAT": [],
                "DBTINSTR": [],
                "DBTAQPAR": [],
                "DBTPRCPAR": [],
                "DBTFTPAR": [],
                "DBTORGPAR": [],
            }
            for i, ode in enumerate(opus_dirs):
                for key in block_indices.keys():
                    if ode.block_category == key:
                        block_indices[key].append(i)

            # write all blocks with empty category that are close to the expected length
            # to the interferogram block. ignore all other blocks
            block_indices["interferogram"] = [
                i for i in block_indices[""] if abs(opus_dirs[i].block_length - 228512) < 200
            ]
            del block_indices[""]

            for key in block_indices:
                if len(block_indices[key]) == 0:
                    raise RuntimeError(f"Could not find a {key} block!")

            # check number of blocks
            assert (
                len(block_indices["DBTDSTAT"]) >= 1
            ), f"found {len(block_indices['DBTDSTAT'])} DBTDSTAT blocks"
            for b in ["DBTINSTR", "DBTAQPAR", "DBTPRCPAR", "DBTFTPAR", "DBTORGPAR"]:
                assert len(block_indices[b]) == 1, f"found {len(block_indices[b])} {b} blocks"

            parameters_ch1 = types.OpusChannelParameters.model_validate(
                {
                    k: utils.read_opus_block(
                        f, opus_dirs[block_indices[k][0]], types.OpusParameterBlock
                    ).data
                    for k in [
                        "DBTAQPAR",
                        "DBTORGPAR",
                        "DBTDSTAT",
                        "DBTINSTR",
                        "DBTPRCPAR",
                        "DBTFTPAR",
                    ]
                }
            )

            channel_count = len(block_indices["DBTDSTAT"])
            assert (
                len(block_indices["interferogram"]) == channel_count
            ), f"found {len(block_indices['interferogram'])} interferogram blocks, but {channel_count} DBTDSTAT blocks"
            read_channel_count = channel_count if read_all_channels else 1

            # all channels share the same parameters, except for the spectrum
            channel_parameters = [parameters_ch1]
            for i in range(1, read_channel_count):
                p = parameters_ch1.model_copy(deep=True)
                p.spectrum = utils.read_opus_block(
                    f,
                    opus_dirs[block_indices["DBTDSTAT"][i]],
                    types.OpusParameterBlock,
                ).data
                channel_parameters.append(p)

            interferogram: Optional[npt.NDArray[np.float64]] = None

            # validate = only check if the block is fully present
            if interferogram_mode == "validate":
                for block_index in block_indices["interferogram"]:
                    utils.read_opus_block(f, opus_dirs[block_index], types.OpusDataBlock)

            # read = read the entire interferogram
            if interferogram_mode == "read":
                interferogram = utils.read_interferogram(
                    f,
                    channel_parameters=channel_parameters,
                    ifg_opus_dirs=[opus_dirs[i] for i in block_indices["interferogram"]][
                        :read_channel_count
                    ],
                    read_all_channels=read_all_channels,
                )

        return OpusFile(
            header=opus_header,
            channel_parameters=channel_parameters,
            measurement_times=[
                p.parse_measurement_datetime(measurement_timestamp_mode) for p in channel_parameters
            ],
            interferogram=interferogram,
        )
