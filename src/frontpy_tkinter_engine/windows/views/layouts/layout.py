from tkinter import Frame, Widget

from frontpy_core.core.views.layouts.layout import Layout
from frontpy_core.core.views.view import View
from frontpy_tkinter_engine.windows.meta import TkinterEngineError
from frontpy_tkinter_engine.windows.tkinter_state_store import TkinterStateStore
from frontpy_tkinter_engine.windows.views.layouts.linear_layout import apply_linear_layout


def create_state_store() -> TkinterStateStore:
    return TkinterStateStore()


def layout_start(layout: Layout, state_store: TkinterStateStore):
    kwargs = {}
    attrs = layout._kw_attrs
    if "background_color" in attrs:
        kwargs["background"] = attrs["background_color"]

    if "border_width" in attrs:
        kwargs["borderwidth"] = attrs["border_width"]

    if "padding_width" in attrs:
        kwargs["padx"] = int(attrs["padding_width"])
    if "padding_height" in attrs:
        kwargs["pady"] = int(attrs["padding_height"])

    if layout.parent is None:
        # case of the root layout
        assert layout.root is not None
        parent_frame: Frame = layout.root.engine_state_store.get('root')
        if parent_frame is None:
            raise TkinterEngineError("The root parent of a layout does ot store a 'root' object")
        # no need to draw a supplementary frame as the Tk() already define the root frame
        state_store["frame"] = parent_frame
        parent_frame.configure(**kwargs)

    else:
        parent_frame = layout.parent.engine_state_store.get('frame')
        if parent_frame is None:
            raise TkinterEngineError("The parent component of a text view does not store a 'frame' object.")

        frame = Frame(parent_frame, **kwargs)
        apply_layout(frame, layout)
        state_store["frame"] = frame


def apply_layout(widget: Widget, view: View):
    """Returns the pack kwargs for any widget of the layout that stored the layout_specs to the state store"""
    layout_mode = view.parent.engine_state_store["layout_spec"]["mode"]
    if layout_mode == "linear":
        return apply_linear_layout(widget, view)
    else:
        raise TkinterEngineError(f"Layout mode unknown: {layout_mode}")
