from tkinter import Button

from frontpy_core.core.views import ButtonView
from frontpy_tkinter_engine.windows.meta import TkinterEngineError
from frontpy_tkinter_engine.windows.tkinter_state_store import TkinterStateStore
from frontpy_tkinter_engine.windows.views.layouts.layout import apply_layout
from frontpy_tkinter_engine.windows.views.utils import get_font


def create_state_store() -> TkinterStateStore:
    return TkinterStateStore()


def start_button_view(view: ButtonView, state_store: TkinterStateStore):
    if "widget" not in view.parent.engine_state_store:
        raise TkinterEngineError("The parent component of a text view does not store a 'frame' object.")

    parent_frame = view.parent.engine_state_store["widget"]  # get the frame in which to put this label

    font = get_font(view._kw_attrs)

    # widget specific kwargs
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

    if view.on_click_listener is not None:
        specific_kw["command"] = view.on_click_listener

    print(specific_kw)
    btn = Button(parent_frame, text=view.text, font=font, **specific_kw)

    apply_layout(btn, view)

    state_store['widget'] = btn

    set_disabled(view, state_store)


def set_disabled(view: ButtonView, state_store):
    btn: Button = state_store['widget']
    btn["state"] = "disabled" if view.disabled else "normal"
