def better_default_datetime_formatter():
    """Make ConciseDateFormatter the default

    "This formatter is a candidate to become the default date tick formatter in future versions of Matplotlib"
    https://matplotlib.org/stable/gallery/ticks/date_concise_formatter.html
    """
    import numpy as np
    import datetime
    import matplotlib.dates as mdates
    import matplotlib.units as munits

    converter = mdates.ConciseDateConverter()
    munits.registry[np.datetime64] = converter
    munits.registry[datetime.date] = converter
    munits.registry[datetime.datetime] = converter


_mokeypatched_matplotlib_constrained_layout = False


def mokeypatch_matplotlib_constrained_layout():
    """Monkeypatch `ENH: allow fig.legend outside axes... #19743` to fix Figure.legend in constrained layouts
    https://github.com/matplotlib/matplotlib/pull/19743"""
    from functools import wraps
    import matplotlib._constrained_layout as constrained_layout

    global _mokeypatched_matplotlib_constrained_layout
    if _mokeypatched_matplotlib_constrained_layout:
        return

    make_layout_margins = constrained_layout.make_layout_margins

    @wraps(make_layout_margins)
    def wrapped_make_layout_margins(
        layoutgrids,
        fig,
        renderer,
        *args,
        w_pad=0,
        h_pad=0,
        hspace=0,
        wspace=0,
        **kwargs
    ):
        ret = make_layout_margins(
            layoutgrids,
            fig,
            renderer,
            *args,
            w_pad=w_pad,
            h_pad=h_pad,
            hspace=hspace,
            wspace=wspace,
            **kwargs,
        )
        # make margins for figure-level legends:
        for leg in fig.legends:
            inv_trans_fig = None
            if getattr(leg, "_outside", None) and leg._bbox_to_anchor is None:
                if inv_trans_fig is None:
                    inv_trans_fig = fig.transFigure.inverted().transform_bbox
                bbox = inv_trans_fig(leg.get_tightbbox(renderer))
                w = bbox.width + 2 * w_pad
                h = bbox.height + 2 * h_pad
                if (leg._loc in (3, 4) and leg._outside == "lower") or (leg._loc == 8):
                    layoutgrids[fig].edit_margin_min("bottom", h)
                elif (leg._loc in (1, 2) and leg._outside == "upper") or (
                    leg._loc == 9
                ):
                    layoutgrids[fig].edit_margin_min("top", h)
                elif leg._loc in (1, 4, 5, 7):
                    layoutgrids[fig].edit_margin_min("right", w)
                elif leg._loc in (2, 3, 6):
                    layoutgrids[fig].edit_margin_min("left", w)
        return ret

    constrained_layout.make_layout_margins = wrapped_make_layout_margins
    _mokeypatched_matplotlib_constrained_layout = True
