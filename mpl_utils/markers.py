from typing import Optional

import matplotlib.font_manager as font_manager
import matplotlib.markers as markers
import matplotlib.path as path
import matplotlib.textpath as textpath
import matplotlib.transforms as transforms

__all__ = ["centered_text_as_path", "marker_with_text"]


def centered_text_as_path(
    s: str,
    font_props: Optional[font_manager.FontProperties] = None,
    ismath: bool = False,
) -> path.Path:
    if font_props is None:
        # fp = font_manager.FontProperties(size=1, family='monospace')
        fp = font_manager.FontProperties(size=1)
    else:
        fp = font_props
    # dx, _, _ = textpath.text_to_path.get_text_width_height_descent("q", fp, ismath=ismath)
    # dy = font.get_size()
    w, h, _d = textpath.text_to_path.get_text_width_height_descent(s, fp, ismath=ismath)
    trans = transforms.Affine2D().scale(fp.get_size() / textpath.text_to_path.FONT_SCALE).translate(-w / 2, -h / 2)
    verts, codes = textpath.text_to_path.get_text_path(fp, s)
    return path.Path(verts, codes, closed=False).transformed(trans)


def marker_with_text(base_marker, text: str) -> markers.MarkerStyle:
    if not isinstance(base_marker, markers.MarkerStyle):
        assert hasattr(base_marker, "__hash__") and base_marker in markers.MarkerStyle.markers
        base_marker = markers.MarkerStyle(base_marker)
    # ignoring alternate path for now
    base_path = base_marker.get_path().transformed(base_marker.get_transform())
    text_path = centered_text_as_path(text).transformed(transforms.Affine2D().scale(3 / 4))
    marker_path = path.Path.make_compound_path(base_path, text_path)
    return markers.MarkerStyle(marker_path)
