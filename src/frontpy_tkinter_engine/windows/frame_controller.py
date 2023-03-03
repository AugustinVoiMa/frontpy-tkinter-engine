from tkinter import Tk

from frontpy_core.core.views.frame_controller.frame_controller import FrameController
from frontpy_tkinter_engine.windows.tkinter_state_store import TkinterStateStore


def create_state_store() -> TkinterStateStore:
    return TkinterStateStore()


def start_frame_controller(fc: FrameController, state_store: TkinterStateStore):
    root = Tk()
    root.geometry(f"{fc.width}x{fc.height}")
    if fc.title is not None:
        root.title(fc.title)
    state_store['root'] = root
