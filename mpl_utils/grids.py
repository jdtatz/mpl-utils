from typing import Union

from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpecBase, SubplotSpec


def add_inner_gridspec(
    fig_spec: Union[Figure, SubplotSpec],
    nrows=1,
    ncols=1,
    **gridspec_kwargs,
) -> GridSpecBase:
    if isinstance(fig_spec, Figure):
        return fig_spec.add_gridspec(nrows, ncols, **gridspec_kwargs)
    elif isinstance(fig_spec, SubplotSpec):
        return fig_spec.subgridspec(nrows, ncols, **gridspec_kwargs)
    else:
        raise TypeError(f"Expected `fig_spec` to be either a `Figure` or a `SubplotSpec`, not a {type(fig_spec)}")
