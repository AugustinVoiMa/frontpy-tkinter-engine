from tkinter import Label, TOP, StringVar, Text, Scrollbar

from frontpy_core.core.views import TextView
from frontpy_tkinter_engine.windows.meta import TkinterEngineError
from frontpy_tkinter_engine.windows.tkinter_state_store import TkinterStateStore
from frontpy_tkinter_engine.windows.views.layouts.layout import apply_layout
from frontpy_tkinter_engine.windows.views.utils import get_font
import tkinter as tk


def create_state_store() -> TkinterStateStore:
    return TkinterStateStore()


def start_edit_text_view(view: TextView, state_store: TkinterStateStore):
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

    if "foreground_color" in view._kw_attrs:
        specific_kw["foreground"] = view._kw_attrs["foreground_color"]
    if "background_color" in view._kw_attrs:
        specific_kw["background"] = view._kw_attrs["background_color"]

    local_frame = False
    if view._kw_attrs.get('overflow-y') == "scroll":
        # we need to wrap text & scrollbar in a single frame
        frame = tk.Frame(parent_frame)
        apply_layout(frame, view)
        parent_frame = frame
        local_frame = True

    scrollbar_y = None
    if 'overflow-y' in view._kw_attrs:
        if view._kw_attrs['overflow-y'] == "scroll":
            scrollbar_y = Scrollbar(parent_frame)
            specific_kw["yscrollcommand"] = scrollbar_y.set

    specific_kw["state"] = "disabled" if view.disabled else "normal"

    print(specific_kw)
    text_var = StringVar()
    text_var.set(view.text)

    lbl = Text(parent_frame,
               font=font,
               **specific_kw)

    if scrollbar_y is not None:
        scrollbar_y.configure(command=lbl.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    if local_frame:
        # local frame implies EditText has it's own frame, so we can expand inside
        lbl.pack(fill=tk.BOTH, expand=True)
    else:
        # otherwise we apply layout config
        apply_layout(lbl, view)

    state_store['label'] = lbl
    state_store['variables'] = dict(
        text=text_var
    )


def update_text(view: TextView, state_store: TkinterStateStore):
    text_var: StringVar = state_store['variables']['text']
    text_var.set(view.text)
