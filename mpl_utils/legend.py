from typing import Union
from typing_extensions import Literal
import mpl_utils.monkeypatch as monkeypatch
from matplotlib.figure import FigureBase
from matplotlib.legend import Legend


def deduped_figure_legend(fig: FigureBase, **legend_kwargs) -> Legend:
    dedupped = dict()
    for ax in fig.axes:
        for h, l in zip(*ax.get_legend_handles_labels()):
            if l not in dedupped:
                dedupped[l] = h
    labels, handles = zip(*dedupped.items())
    return fig.legend(handles, labels, **legend_kwargs)


def move_legend_outside(
    lgd: Legend, outside: Union[bool, Literal["upper"], Literal["lower"]] = True
):
    if not outside:
        return
    # Either the patch has been upstreamed or the monkeypatch has been applied
    if hasattr(lgd, "_outside") or monkeypatch._mokeypatched_matplotlib_constrained_layout:
        lgd._outside = outside
    elif lgd._loc == 1 and outside == True:
        lgd.set_bbox_to_anchor((1, 1))
    else:
        raise NotImplementedError(
            "When not monkeypatched the only backup path implmented is `outside=True` with `loc='upper right'`"
        )
