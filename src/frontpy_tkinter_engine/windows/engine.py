import importlib
from tkinter import mainloop
from typing import Type

from frontpy_core.core.views.frame_controller.frame_controller import FrameController
from frontpy_core.engine_base.abstract_engine import AbstractEngine
from . import views
from . import frame_controller


class Engine(AbstractEngine):
    views = views

    frame_controller = frame_controller

    def launch_frames(self):
        frames = []

        # Get master window
        for win_manifest in self.manifest["windows"]:
            if win_manifest.get("main", False):
                controller_pkg, controller_name = win_manifest["frame_controller"].split(':')
                controller_class: Type[FrameController] = getattr(
                    importlib.import_module(
                        self.manifest["application_package"] + controller_pkg),
                    controller_name)

                frame = controller_class()
                frames.append(frame)
                break

        # Get additional start windows
        for win_manifest in self.manifest["windows"]:
            if win_manifest.get("open_on_launch", False) and not win_manifest.get("main", False):
                controller_pkg, controller_name = win_manifest["frame_controller"].split(':')
                controller_class: Type[FrameController] = getattr(
                    importlib.import_module(
                        self.manifest["application_package"] + controller_pkg),
                    controller_name)

                frame = controller_class()
                frames.append(frame)
        return frames

    def run(self):
        mainloop()
