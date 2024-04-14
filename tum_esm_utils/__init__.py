"""Python utilities by the Professorship of Environmental
Sensing and Modeling at the Technical University of Munich.

GitHub Repository https://github.com/tum-esm/utils
Documentation: https://tum-esm-utils.netlify.app
PyPI: https://pypi.org/project/tum-esm-utils"""

from . import (
    code,
    datastructures,
    decorators,
    files,
    mathematics,
    processes,
    shell,
    system,
    text,
    timing,
    validators,
)

try:
    from . import em27
except ImportError:
    pass

try:
    from . import plotting
except ImportError:
    pass
