"""Better defaults for matplotlib plots and utilities for creating and saving figures.

Implements: `apply_better_defaults`, `create_figure`, `add_subplot`

This requires you to install this utils library with the optional `plotting` dependencies:

```bash
pip install "tum_esm_utils[plotting]"
# or
pdm add "tum_esm_utils[plotting]"
```"""

from typing import Generator, Optional, Any, Union
import contextlib

import matplotlib.pyplot as plt
import matplotlib.font_manager
import matplotlib.patches
from tailwind_colors import TAILWIND_COLORS_HEX


def apply_better_defaults(font_family: Optional[str] = "Roboto") -> None:
    """Apply better defaults to matplotlib plots.

    Args:
        font_family: The font family to use for the plots. If None, the default
                        settings are not changed.
    """

    if font_family is not None:
        system_fonts = matplotlib.font_manager.findSystemFonts()
        matching_fonts = [font for font in system_fonts if font_family in font]
        if len(matching_fonts) == 0:
            raise ValueError(
                f"Font family '{font_family}' not found. System fonts: {system_fonts}"
            )
        for font in matching_fonts:
            matplotlib.font_manager.fontManager.addfont(font)
        plt.rcParams['font.sans-serif'] = [
            font_family, *plt.rcParams['font.sans-serif']
        ]

    plt.rcParams['figure.titleweight'] = 'bold'
    plt.rcParams['axes.titleweight'] = 'semibold'
    plt.rcParams['axes.labelweight'] = 'semibold'
    plt.rcParams['axes.facecolor'] = TAILWIND_COLORS_HEX.SLATE_050
    plt.rcParams['axes.edgecolor'] = TAILWIND_COLORS_HEX.SLATE_600
    plt.rcParams['grid.color'] = TAILWIND_COLORS_HEX.SLATE_300
    plt.rcParams['axes.axisbelow'] = True
    plt.rcParams['xtick.color'] = TAILWIND_COLORS_HEX.SLATE_600
    plt.rcParams['ytick.color'] = TAILWIND_COLORS_HEX.SLATE_600
    plt.rcParams['xtick.labelcolor'] = "black"
    plt.rcParams['ytick.labelcolor'] = "black"
    plt.rcParams['scatter.edgecolors'] = "none"
    matplotlib.style.use('fast')


@contextlib.contextmanager
def create_figure(
    path: str,
    title: Optional[str] = None,
    width: float = 10,
    height: float = 10,
    suptitle_y: float = 0.97,
    padding: float = 2,
    dpi: int = 250,
) -> Generator[plt.Figure, None, None]:
    """Create a figure for plotting.
    
    Usage:

    ```python
    with create_figure("path/to/figure.png", title="Title") as fig:
        ...
    ```
    Args:
        path: The path to save the figure to.
        title: The title of the figure.
        width: The width of the figure.
        height: The height of the figure.
        suptitle_y: The y-coordinate of the figure title.
        padding: The padding of the figure.
        dpi: The DPI of the figure.
    """

    fig = plt.figure()
    fig.set_size_inches(width, height)
    yield fig
    if title is not None:
        fig.suptitle(title)
        fig.suptitle(fig._suptitle.get_text(), y=suptitle_y)  # type: ignore
    fig.tight_layout(pad=padding)
    fig.savefig(path, dpi=dpi)
    plt.close(fig)


def add_subplot(
    fig: plt.Figure,
    position: tuple[int, int, int],
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    **kwargs: dict[str, Any],
) -> plt.Axes:
    """Add a subplot to a figure.
    
    Args:
        fig: The figure to add the subplot to.
        position: The position of the subplot. The tuple should contain three integers: the number of rows, the number of columns, and the index of the subplot.
        title: The title of the subplot.
        xlabel: The x-axis label of the subplot.
        ylabel: The y-axis label of the subplot.
        **kwargs: Additional keyword arguments for the subplot.
    
    Returns:
        An axis object for the new subplot.
        
    Raises:
        ValueError: If the index of the subplot is invalid."""

    if (position[2] < 1) or (position[2] > (position[0] * position[1])):
        raise ValueError(
            "Invalid subplot index. The index must be between 1 and the number of rows times the number of columns."
        )

    axis = fig.add_subplot(position[0], position[1], position[2], **kwargs)
    if title is not None:
        axis.set_title(title)
    if xlabel is not None:
        axis.set_xlabel(xlabel)
    if ylabel is not None:
        axis.set_ylabel(ylabel)
    axis.grid(visible=None, which="minor", axis="both", linewidth=0.25)
    axis.grid(visible=None, which="major", axis="both", linewidth=0.75)
    return axis


def add_colorpatch_legend(
    fig: plt.Figure,
    handles: list[tuple[str, Union[
        str,
        tuple[float, float, float],
        tuple[float, float, float, float],
    ]]],
    ncols: Optional[int] = None,
    location: str = "upper left",
) -> None:
    """Add a color patch legend to a figure.
    
    Args:
        fig: The figure to add the legend to.
        handles: A list of tuples containing the label and color of each patch 
            (e.g. `[("Label 1", "red"), ("Label 2", "blue")]`). You can pass any color
            that is accepted by matplotlib.
        ncols: The number of columns in the legend.
        location: The location of the legend.
    """

    fig.legend(
        handles=[
            matplotlib.patches.Patch(color=color, label=label)
            for label, color in handles
        ],
        ncol=len(handles) if ncols is None else ncols,
        loc=location,
    )
