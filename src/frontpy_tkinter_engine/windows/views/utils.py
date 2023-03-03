import re
from tkinter.font import Font

from frontpy_tkinter_engine.windows.meta import TkinterEngineError


def get_font(kw_attrs):
    font_kwargs = {}
    if "font_family" in kw_attrs:
        font_kwargs["family"] = kw_attrs["font_family"]
    if "font_size" in kw_attrs:
        font_size_str = kw_attrs["font_size"]
        mo = re.match(r"^\s*(\d+)\s*pt\s*$", font_size_str)
        if mo:
            font_kwargs["size"] = int(mo.group(1))
        else:
            mo = re.match(r"^\s*(\d+)\s*(?:px)?\s*$", font_size_str)
            if not mo:
                raise TkinterEngineError(f"unrecognized font size: {font_size_str}. "
                                         f"Expected an integer valut for point (pt) or px (optional px)")
            font_kwargs["size"] = -int(mo.group(1))  # px unit is specified to tk with negative int

    if "font_weight" in kw_attrs:
        w = kw_attrs["font_weight"]
        if w not in ["bold", "normal"]:
            raise TkinterEngineError(f"Unrecognized font_weight: {w}.Expected either 'bold' or 'normal'")
        font_kwargs["weight"] = w

    return Font(**font_kwargs)
