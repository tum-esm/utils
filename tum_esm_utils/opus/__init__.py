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

from .file_interface import OpusFile as OpusFile
