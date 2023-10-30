from typing import Union

from matplotlib.figure import FigureBase
from matplotlib.legend import Legend
from typing_extensions import Literal

import mpl_utils.monkeypatch as monkeypatch


def deduped_figure_legend(fig: FigureBase, **legend_kwargs) -> Legend:
    dedupped = dict()
    for ax in fig.axes:
        for h, l in zip(*ax.get_legend_handles_labels()):
            if l not in dedupped:
                dedupped[l] = h
    labels, handles = zip(*dedupped.items())
    return fig.legend(handles, labels, **legend_kwargs)


def move_legend_outside(lgd: Legend, outside: Union[bool, Literal["upper"], Literal["lower"]] = True):
    import warnings

    warnings.warn(
        "Setting legend loc with `outside ...` has been upstreamed & prefered over moving it outside after creation, which can only be done using unstable internel methods",
        category=DeprecationWarning,
    )

    if not outside:
        return
    loc = lgd._loc_real
    if not isinstance(loc, str):
        raise NotImplementedError("Can only move legends that were defined with an inital `str` loc")
    if outside:
        loc = f"outside {loc}"
    else:
        loc = f"outside {outside} {loc}"
    lgd.set_loc(loc)
