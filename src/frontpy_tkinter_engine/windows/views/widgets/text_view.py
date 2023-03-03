from tkinter import Label, TOP

from frontpy_core.core.views import TextView
from frontpy_tkinter_engine.windows.meta import TkinterEngineError
from frontpy_tkinter_engine.windows.tkinter_state_store import TkinterStateStore
from frontpy_tkinter_engine.windows.views.layouts.layout import apply_layout
from frontpy_tkinter_engine.windows.views.utils import get_font


def create_state_store() -> TkinterStateStore:
    return TkinterStateStore()


def start_text_view(view: TextView, state_store: TkinterStateStore):
    if "frame" not in view.parent.engine_state_store:
        raise TkinterEngineError("The parent component of a text view does not store a 'frame' object.")

    parent_frame = view.parent.engine_state_store["frame"]  # get the frame in which to put this label

    font = get_font(view._kw_attrs)

    # widet specific kwargs
    specific_kw = {}
    if "width" in view._kw_attrs:
        specific_kw["width"] = int(view._kw_attrs["width"])
    if "height" in view._kw_attrs:
        specific_kw["height"] = int(view._kw_attrs["height"]) // font.metrics("linespace")
    if "justify" in view._kw_attrs:
        j = view._kw_attrs["justify"]
        if j not in ["left", "center", "right"]:
            raise TkinterEngineError(f"Unrecognized justify value: {j}. Expected 'left', 'center' or 'right'")
        specific_kw["justify"] = j

    if "foreground_color" in view._kw_attrs:
        specific_kw["foreground"] = view._kw_attrs["foreground_color"]
    if "background_color" in view._kw_attrs:
        specific_kw["background"] = view._kw_attrs["background_color"]

    if "align" in view._kw_attrs:
        if view._kw_attrs["align"] == "center":
            s = "center"
        else:
            align = list(map(str.strip, view._kw_attrs["align"].split('|')))
            s = ""
            if "top" in align:
                s += "n"
            if "bottom" in align:
                s += "s"
            if "left" in align:
                s += "w"
            if "right" in align:
                s += "e"
        specific_kw["anchor"] = s

    specific_kw["state"] = "disabled" if view.disabled else "normal"

    print(specific_kw)
    lbl = Label(parent_frame, text=view.text, font=font, **specific_kw)

    apply_layout(lbl, view)

    state_store['label'] = lbl
