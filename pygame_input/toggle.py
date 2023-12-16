import pygame
from pygame.surface import Surface, Surface as Surface
from .button import ButtonRect as _ButtonRect, ButtonCircle as _ButtonCircle


class ToggleButtonRect(_ButtonRect):
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            border_radius: int = 0,
            background_image: Surface | None = None,
            color: tuple = ...,
            padding: int = 0,
            outline_color: tuple = ...,
            outline_width: int = 1,
            value=None,
            active: bool = True,
            state: bool = False) -> None:
        super().__init__(
            x,
            y,
            width,
            height,
            border_radius,
            background_image,
            color,
            padding,
            outline_color,
            outline_width,
            value,
            active)
        self.state = state
        self._on_toggle_on = None
        self._on_toggle_off = None
        self.set_on_click(self.toggle)

    @staticmethod
    def toggle(self):
        if self.state and self._on_toggle_off:
            self.state = not self.state
            self._on_toggle_off(self)
        elif not self.state and self._on_toggle_on:
            self.state = not self.state
            self._on_toggle_on(self)

    def set_on_toggle(self, on, off):
        self._on_toggle_on = on
        self._on_toggle_off = off

    def set_on_toggle_on(self, func):
        self._on_toggle_on = func

    def set_on_toggle_off(self, func):
        self._on_toggle_off = func


class ToggleButtonCircle(_ButtonCircle):
    def __init__(
            self,
            x: int,
            y: int,
            radius: int,
            border_radius: int = 0,
            background_image: Surface | None = None,
            color: tuple = ...,
            padding: int = 0,
            outline_color: tuple = ...,
            outline_width: int = 1,
            value=None,
            active: bool = True,
            state: bool = False) -> None:
        super().__init__(
            x,
            y,
            radius,
            border_radius,
            background_image,
            color,
            padding,
            outline_color,
            outline_width,
            value,
            active)
        self.state = state
        self._on_toggle_on = None
        self._on_toggle_off = None
        self.set_on_click(self.toggle)

    @staticmethod
    def toggle(self):
        if self.state and self._on_toggle_off:
            self._on_toggle_off(self)
        elif not self.state and self._on_toggle_on:
            self._on_toggle_on(self)

    def set_on_toggle(self, on, off):
        self._on_toggle_on = on
        self._on_toggle_off = off

    def set_on_toggle_on(self, func):
        self._on_toggle_on = func

    def set_on_toggle_off(self, func):
        self._on_toggle_off = func
