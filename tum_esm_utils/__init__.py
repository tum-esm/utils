"""Python utilities by the Professorship of Environmental
Sensing and Modeling at the Technical University of Munich.

GitHub Repository https://github.com/tum-esm/utils
Documentation: https://tum-esm-utils.netlify.app
PyPI: https://pypi.org/project/tum-esm-utils

(Optional) Explicit Imports:

By setting the environment variable `TUM_ESM_UTILS_EXPLICIT_IMPORTS=1`, the
package disables automatic submodule imports. This means you cannot import the
whole package and access submodules directly (e.g., `tum_esm_utils.code` will
not be available after `import tum_esm_utils`). Instead, you must explicitly
import each submodule, e.g. `from tum_esm_utils import code` or
`import tum_esm_utils.code`.

This reduces the import time of the package by up to 60 times
"""

import os

if os.getenv("TUM_ESM_UTILS_EXPLICIT_IMPORTS") != "1":
    from . import (
        code as code,
        datastructures as datastructures,
        decorators as decorators,
        files as files,
        mathematics as mathematics,
        processes as processes,
        rebinning as rebinning,
        shell as shell,
        sqlitelock as sqlitelock,
        system as system,
        text as text,
        timing as timing,
        validators as validators,
    )

    # ignore import errors from the following submodules
    # because they requires extras to be installed

    # requires extra "em27"
    try:
        from . import em27 as em27
    except ImportError:
        pass

    # requires extra "plotting"
    try:
        from . import plotting as plotting
    except ImportError:
        pass

    # requires extra "opus"
    try:
        from . import opus as opus
    except ImportError:
        pass

    # requires extra "modeling"
    try:
        from . import column as column
    except ImportError:
        pass

    # requires extra "modeling"
    try:
        from . import rebinning as rebinning
    except ImportError:
        pass

    # requires extra "netcdf"
    try:
        from . import netcdf as netcdf
    except ImportError:
        pass
