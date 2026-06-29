# `tum_esm_utils.plotting` API Reference


Better defaults for matplotlib plots and utilities for creating and saving figures.

Implements: `apply_better_defaults`, `create_figure`, `add_subplot`

This requires you to install this utils library with the optional `plotting` dependencies:

```bash
pip install "tum_esm_utils[plotting]"
## `or`
uv add "tum_esm_utils[plotting]"
```


##### `apply_better_defaults`

```python
def apply_better_defaults(font_family: Optional[str] = "Roboto",
                          load_system_fonts: bool = False) -> None
```

Apply better defaults to matplotlib plots.

**Arguments**:

- `font_family` - The font family to use for the plots. If None, the default
  settings are not changed.
- `load_system_fonts` - If True, the system fonts are manually added to the
  font manager. Normally, this is not necessary.


##### `create_figure`

```python
@contextlib.contextmanager
def create_figure(path: str,
                  title: Optional[str] = None,
                  width: float = 10,
                  height: float = 10,
                  suptitle_y: float = 0.97,
                  padding: float = 2,
                  dpi: int = 250) -> Generator[plt.Figure, None, None]
```

Create a figure for plotting.

Usage:

```python
with create_figure("path/to/figure.png", title="Title") as fig:
    ...
```

**Arguments**:

- `path` - The path to save the figure to.
- `title` - The title of the figure.
- `width` - The width of the figure.
- `height` - The height of the figure.
- `suptitle_y` - The y-coordinate of the figure title.
- `padding` - The padding of the figure.
- `dpi` - The DPI of the figure.


##### `add_subplot`

```python
def add_subplot(fig: plt.Figure,
                position: tuple[int, int, int]
                | matplotlib.gridspec.SubplotSpec,
                title: Optional[str] = None,
                xlabel: Optional[str] = None,
                ylabel: Optional[str] = None,
                **kwargs: Any) -> plt.Axes
```

Add a subplot to a figure.

Use a gridspec for more control:


```python
gs = matplotlib.gridspec.GridSpec(4, 1, height_ratios=[1, 2, 2, 2])
add_subplot(fig, gs[0], ...)
```

**Arguments**:

- `fig` - The figure to add the subplot to.
- `position` - The position of the subplot. The tuple should contain three
  integers (rows, columns, index). You can also pass a gridspec
  subplot spec.
- `title` - The title of the subplot.
- `xlabel` - The x-axis label of the subplot.
- `ylabel` - The y-axis label of the subplot.
- `**kwargs` - Additional keyword arguments for the subplot.
  

**Returns**:

  An axis object for the new subplot.
  

**Raises**:

- `ValueError` - If the index of the subplot is invalid.


##### `add_colorpatch_legend`

```python
def add_colorpatch_legend(fig: plt.Figure | matplotlib.axes.Axes,
                          handles: list[tuple[
                              str,
                              Union[
                                  str,
                                  tuple[float, float, float],
                                  tuple[float, float, float, float],
                              ],
                          ]],
                          ncols: Optional[int] = None,
                          location: str = "upper left",
                          **kwargs: Any) -> None
```

Add a color patch legend to a figure.

**Arguments**:

- `fig` - The figure to add the legend to.
- `handles` - A list of tuples containing the label and color of each patch
  (e.g. `[("Label 1", "red"), ("Label 2", "blue")]`). You can pass any color
  that is accepted by matplotlib.
- `ncols` - The number of columns in the legend.
- `location` - The location of the legend.

