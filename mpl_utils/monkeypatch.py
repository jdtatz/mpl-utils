def better_default_datetime_formatter():
    """Make ConciseDateFormatter the default

    "This formatter is a candidate to become the default date tick formatter in future versions of Matplotlib"
    https://matplotlib.org/stable/gallery/ticks/date_concise_formatter.html
    """
    import datetime

    import matplotlib.dates as mdates
    import matplotlib.units as munits
    import numpy as np

    converter = mdates.ConciseDateConverter()
    munits.registry[np.datetime64] = converter
    munits.registry[datetime.date] = converter
    munits.registry[datetime.datetime] = converter


def mokeypatch_matplotlib_constrained_layout():
    """Monkeypatch `ENH: allow fig.legend outside axes... #19743` to fix Figure.legend in constrained layouts
    https://github.com/matplotlib/matplotlib/pull/19743
    """
    import warnings

    warnings.warn(
        "No need to mokeypatch matplotlib anymore, the patch has already been upstreamed", category=DeprecationWarning
    )
