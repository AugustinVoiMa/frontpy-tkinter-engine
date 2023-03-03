import re
import tkinter as tk
from frontpy_core.core.views import LinearLayout
from frontpy_core.core.views.view import View
from frontpy_tkinter_engine.windows.tkinter_state_store import TkinterStateStore


def linear_layout_start(layout: LinearLayout, state_store: TkinterStateStore):
    state_store['layout_spec'] = {
        'mode': 'linear',
        'direction': layout.direction,
        'rtl': layout.rtl
    }


def apply_linear_layout(widget: tk.Widget, view: View):
    layout_spec = view.parent.engine_state_store["layout_spec"]
    height = view.layout_height
    width = view.layout_width

    pack_kw = {}

    # pxvalue = lambda s: re.match(r"^\s*(\d+)\s*(?:px)?\s*$", s)
    if height == "match_parent" and width == "match_parent":
        pack_kw["fill"] = tk.BOTH
    elif height == "match_parent":
        pack_kw["fill"] = tk.Y
    elif width == "match_parent":
        pack_kw["fill"] = tk.X

    # if "fill" in pack_kw:
    #     pack_kw["expand"] = True

    if layout_spec['direction'] == "vertical":
        pack_kw['side'] = "top"
    elif layout_spec['rtl']:
        pack_kw['side'] = "right"
    else:
        pack_kw['side'] = "left"


    if "layout_align" in view._kw_attrs:
        if view._kw_attrs.get("layout_align") == "center":
            s = "center"
        else:
            align = list(map(str.strip, view._kw_attrs["layout_align"].split('|')))
            s = ""
            if "top" in align:
                s += "n"
            if "bottom" in align:
                s += "s"
            if "left" in align:
                s += "w"
            if "right" in align:
                s += "e"
        pack_kw["anchor"] = s
    print(pack_kw)
    widget.pack(**pack_kw)
