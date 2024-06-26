import pygame
from pygame.surface import Surface as Surface


class ButtonRect:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            border_radius: int = 0,
            background_image: pygame.Surface | None = None,
            color: tuple = (
                255,
                255,
                255),
            padding: int = 0,
            outline_color: tuple = (
                0,
                0,
                0),
        outline_width: int = 1,
        value=None,
            active: bool = True) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.display_dx = 0
        self.display_dy = 0
        self.display_dwidth = 0
        self.display_dheight = 0

        self.border_radius = border_radius
        self.border_top_left_radius = border_radius
        self.border_top_right_radius = border_radius
        self.border_bottom_left_radius = border_radius
        self.border_bottom_right_radius = border_radius
        self.background_image = pygame.transform.scale(
            background_image, (width, height)) if background_image else None
        self.color = color
        self.padding = padding
        self.outline_color = outline_color
        self.outline_width = outline_width

        self.label_text = None
        self.label_font = None
        self.label_color = (0, 0, 0)

        self.value = value
        self.active = active
        self._on_active_action = None
        self._on_inactive_action = None

        self._on_hover_action = None
        self._on_not_hover_action = None
        self._hovering = False

        self._on_click_action = None
        self._activate_mouse_button = None

        if width <= padding * 2 or height <= padding * 2:
            raise ValueError(
                "Height and Width must be bigger than 2 times of padding")

    @property
    def rect(self): return pygame.Rect(self.x, self.y, self.width, self.height)

    @property
    def display_rect(self): return pygame.Rect(
        self.x + self.display_dx,
        self.y + self.display_dy,
        self.width + self.display_dwidth,
        self.height + self.display_dheight)

    @display_rect.setter
    def display_rect(self, x, y, width, height):
        self.display_rect = pygame.Rect(x, y, width, height)

    def set_advanced_border_radius(
            self,
            border_top_left_radius: int,
            border_top_right_radius: int,
            border_bottom_left_radius: int,
            border_bottom_right_radius: int):
        self.border_top_left_radius = border_top_left_radius
        self.border_top_right_radius = border_top_right_radius
        self.border_bottom_left_radius = border_bottom_left_radius
        self.border_bottom_right_radius = border_bottom_right_radius

    def set_background_image(self, image: pygame.Surface):
        self.background_image = pygame.transform.scale(
            image, (self.width, self.height))

    def set_label(
        self, text: str, font: pygame.font.Font = pygame.font.Font(
            None, 10), color: tuple = (
            0, 0, 0)):
        '''Set the text, font and text color of the text on the button'''
        self.label_text = text
        self.label_font = font
        self.label_color = color

    def set_activate_action(self, on_active, on_inactive):
        self._on_active_action = on_active
        self._on_inactive_action = on_inactive

    def set_on_active_action(self, func):
        self._on_active_action = func

    def set_on_inactive_action(self, func):
        self._on_inactive_action = func

    def activate(self):
        if not self.active and self._on_active_action:
            self._on_active_action()
        self.active = True

    def deactivate(self):
        if self.active and self._on_inactive_action:
            self._on_inactive_action()
        self.active = False

    def set_hover(self, on_hover, on_not_hover):
        '''Fast set action when the button is hovered on and off

        Parameters
        ----------
        on_hover
            Function to be called when hover on, take in 1 argument: self
        on_not_hover
            Function to be called when hover off, take in 1 argument: self
        '''
        self._on_hover_action = on_hover
        self._on_not_hover_action = on_not_hover

    def set_on_hover(self, func):
        '''Set action when the button is hovered on

        Parameters
        ----------
        func
            Function to be called, take in 1 argument: self
        '''
        self._on_hover_action = func

    def set_on_not_hover(self, func):
        '''Set action when the button is hovered off

        Parameters
        ----------
        func
            Function to be called, take in 1 argument: self
        '''
        self._on_not_hover_action = func

    def set_on_click(self, func):
        '''Set action when the button is clicked

        Parameters
        ----------
        func
            Function to be called, take in 1 argument: self
        '''
        self._on_click_action = func

    def set_mouse_button(self, button: int):
        '''Set clicked mouse button on the button to activate, or else any mouse button can activate it

        Parameters
        ----------
        button : pygame mouse button, left-1, middle-2, right-3'''
        self._activate_mouse_button = button

    def handle_events(self, events: list, dt: float):
        '''Called at the start of every game loop

        Parameters
        ----------
        events: `list`
            Pass in the result from pygame.event.get(), be aware to only call this function once
        dt: `float`
            Time difference from last frame
        '''

        for event in events:
            # Hover handling
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if self._on_hover_action and not self._hovering:
                        self._on_hover_action(self)
                    self._hovering = True
                else:
                    if self._on_not_hover_action and self._hovering:
                        self._on_not_hover_action(self)
                    self._hovering = False
            # Click handling
            if self.active:
                if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                        event.pos):
                    if self._activate_mouse_button and event.button != self._activate_mouse_button:
                        continue
                    if self._on_click_action:
                        self._on_click_action(self)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            self.outline_color,
            (self.display_rect.x - self.outline_width,
             self.display_rect.y - self.outline_width,
             self.display_rect.width + self.outline_width * 2,
             self.display_rect.height + self.outline_width * 2),
            border_radius=self.border_radius,
            border_top_left_radius=self.border_top_left_radius,
            border_top_right_radius=self.border_top_right_radius,
            border_bottom_left_radius=self.border_bottom_left_radius,
            border_bottom_right_radius=self.border_bottom_right_radius)
        if self.background_image:
            match_width = self.background_image.get_width() == self.display_rect.width
            match_height = self.background_image.get_height() == self.display_rect.height
            if not match_width or not match_height:
                self.background_image = pygame.transform.scale(
                    self.background_image,
                    (self.width + self.display_dwidth,
                     self.height + self.display_dheight))
            screen.blit(self.background_image, self.display_rect)
        else:
            pygame.draw.rect(
                screen,
                self.color,
                self.display_rect,
                0,
                self.border_radius,
                self.border_top_left_radius,
                self.border_top_right_radius,
                self.border_bottom_left_radius,
                self.border_bottom_right_radius)

        if self.label_font:
            label_surface = self.label_font.render(
                self.label_text, True, self.label_color)
            screen.blit(
                label_surface,
                (self.display_rect.x + self.padding,
                 self.display_rect.y + self.padding))


class ButtonCircle(ButtonRect):
    def __init__(
            self,
            x: int,
            y: int,
            radius: int,
            border_radius: int = 0,
            background_image: Surface | None = None,
            color: tuple = (
                255,
                255,
                255),
            padding: int = 0,
            outline_color: tuple = (
                0,
                0,
                0),
        outline_width: int = 1,
        value=None,
            active: bool = True) -> None:
        super().__init__(
            x,
            y,
            radius * 2,
            radius * 2,
            border_radius,
            background_image,
            color,
            padding,
            outline_color,
            outline_width,
            value,
            active)
