from tkinter import Widget

from frontpy_core.core.event import Event, KeyEvent
from frontpy_core.core.views.view import View
from frontpy_tkinter_engine.windows.tkinter_state_store import TkinterStateStore


def event2tkinter_sequence(event: Event):
    ev_modifiers = []
    ev_type = []
    ev_detail = []
    if isinstance(event, KeyEvent):
        ev_type.append("KeyPress")
        for key in event.keys:
            if key == "Ctrl":
                key = "Control"
            # if len(key) == 1:
            #     key = key.lower()
            if key in ["Control", "Shift", "Alt"]:
                ev_modifiers.append(key)
            else:
                ev_detail.append(key)
    assert len(ev_modifiers) <= 2
    assert len(ev_type) <= 1
    assert len(ev_detail) <= 1
    assert len(ev_type) > 0 or len(ev_detail) > 0

    seq = ev_modifiers + ev_type + ev_detail
    print("build sequence", seq)
    return "<" + '-'.join(seq) + ">"


def build_callback(fun):
    def callback(event):
        print("called event", event)
        fun()

    return callback


def set_event_listeners(view: View, store: TkinterStateStore):
    main_widget: Widget = store['widget']
    for event, listeners in view._events.items():
        event_sequence = event2tkinter_sequence(event)
        print("set bindings for event", event, "with sequence", event_sequence)
        main_widget.unbind(event_sequence)
        for listener in listeners:
            main_widget.bind(event_sequence, build_callback(listener), add=True)
