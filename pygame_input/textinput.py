import pygame


class TextInput:
    '''
        Text box input for pygame

        Usage
        ------------
        `handle_event` and `draw` must be called every frame, `set_on_submit` can be used to do different actions
    '''

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 border_radius: int = 0,
                 text: str = "",
                 placeholder: str = "",
                 font: pygame.font.Font = pygame.font.Font(None, 10),
                 background_image: pygame.Surface | None = None,
                 background_color: tuple = (255, 255, 255),
                 outline_color: tuple = (0, 0, 0),
                 outline_width: int = 0,
                 padding: int = 5,
                 text_color: tuple = (0, 0, 0)
                 ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.border_top_left_radius = border_radius
        self.border_top_right_radius = border_radius
        self.border_bottom_left_radius = border_radius
        self.border_bottom_right_radius = border_radius
        self.text = text
        self.pointer = 0
        self._position_shift = 0
        self.placeholder = placeholder
        self.font = font
        self.background_image = pygame.transform.scale(
            background_image, (width, height)) if background_image else None
        self.background_color = background_color
        self.active_background_color = background_color
        self.inactive_background_color = background_color
        self.hover_background_color = background_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.padding = padding
        self.text_color = text_color

        self.text_surface = font.render(self.text, True, text_color)

        self.active = False
        self._activate_mouse_button = None
        self._activate_key = None

        self._submit_action = None
        self._submit_do_default = True
        self._on_active_action = None
        self._on_inactive_action = None
        self._on_hover_action = None
        self._on_not_hover_action = None
        self._hovering = False

        self._pressing_down = None
        self._pressing_down_time = 0
        self._pointer_animation_clock = 0
        self._pointer_animation_showing = True

        if height <= padding * 2 or width <= padding * 2:
            raise ValueError(
                "Height and Width must be bigger than 2 times of padding")

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_events(self, events: list, dt: float) -> bool:
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
                    self.background_color = self.hover_background_color
                    if self._on_hover_action and not self._hovering:
                        self._on_hover_action(self)
                    self._hovering = True
                else:
                    self.background_color = self.active_background_color if self.active else self.inactive_background_color
                    if self._on_not_hover_action and self._hovering:
                        self._on_not_hover_action(self)
                    self._hovering = False
            # Clicked handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._activate_mouse_button:
                    if event.button != self._activate_mouse_button:
                        continue
                if self.rect.collidepoint(event.pos):
                    self.activate()
                else:
                    self.deactivate()
            # Check activate key
            if self._activate_key and not self.active:
                if event.type == pygame.KEYDOWN and event.key == self._activate_key:
                    self.activate()
                    continue
            if self.active:
                # Check key presses
                if event.type == pygame.KEYDOWN:
                    self._pointer_animation_showing = True
                    self._pointer_animation_clock = 0
                    if event.key == pygame.K_RETURN:
                        self.on_submit()
                        continue
                    elif event.key == pygame.K_BACKSPACE:
                        if self.pointer == 0:
                            continue
                        self.text = self.text[0:self.pointer -
                                              1] + self.text[self.pointer:]
                        self.pointer -= 1
                    elif event.key == pygame.K_LEFT:
                        if self.pointer > 0:
                            self.pointer -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.pointer < len(self.text):
                            self.pointer += 1
                    else:
                        self.text = self.text[0:self.pointer] + \
                            event.unicode + self.text[self.pointer:]
                        self.pointer += 1

                    self._pressing_down = event
                    self._pressing_down_time = 0

                if event.type == pygame.KEYUP:
                    if self._pressing_down and event.key == self._pressing_down.key:
                        self._pressing_down = None
                        self.pressing_down_time = 0

        # Key hold down actions
        if self._pressing_down_time > 0.5 and self._pressing_down:
            if self._pressing_down.key == pygame.K_BACKSPACE:
                if self.pointer > 0:
                    self.text = self.text[0:self.pointer -
                                          1] + self.text[self.pointer:]
                    self.pointer -= 1
            elif self._pressing_down.key == pygame.K_LEFT:
                if self.pointer > 0:
                    self.pointer -= 1
            elif self._pressing_down.key == pygame.K_RIGHT:
                if self.pointer < len(self.text):
                    self.pointer += 1
            else:
                self.text += self._pressing_down.unicode
                self.pointer += 1
            self._pressing_down_time -= 0.05
            self._pointer_animation_clock = 0
            self._pointer_animation_showing = True

        if self._pressing_down:
            self._pressing_down_time += dt

        # display surface creating
        if self.active:
            text_render = self.font.render(self.text, True, self.text_color)

            text_surface_width = text_render.get_width()
            text_width_right_of_pointer = self.font.render(
                self.text[self.pointer:], True, self.text_color).get_width()
            pointer_loc = text_surface_width - text_width_right_of_pointer
            pointer_surface = pygame.Surface(
                (self.font.get_height() // 10, self.font.get_height()))
            if self._pointer_animation_showing:
                pointer_surface.fill(self.text_color)
            else:
                pointer_surface.fill(self.background_color)

            pointer_display_pos_right = pointer_loc - \
                self._position_shift + pointer_surface.get_width()
            text_display_width = self.width - self.padding * 2      # (*****)|
            # |(*****)
            pointer_is_right_of_display = pointer_display_pos_right > text_display_width
            pointer_is_left_of_display = pointer_loc < self._position_shift and text_width_right_of_pointer > self.width
            text_width_is_shorter_than_display = pointer_display_pos_right + \
                text_width_right_of_pointer < text_display_width  # *(****|)

            if pointer_is_right_of_display:
                self._position_shift = pointer_loc + pointer_surface.get_width() - self.width + \
                    self.padding * 2

            elif pointer_is_left_of_display:
                self._position_shift = pointer_loc

            elif text_width_is_shorter_than_display:
                pointer_abs_pos_right = pointer_loc + pointer_surface.get_width()
                new_pos_shift = pointer_abs_pos_right + \
                    text_width_right_of_pointer - text_display_width
                self._position_shift = 0 if new_pos_shift < 0 else new_pos_shift

            self.text_surface = pygame.Surface(
                (text_render.get_width() +
                 pointer_surface.get_width(),
                 text_render.get_height()),
                pygame.SRCALPHA,
                32)
            self.text_surface.convert_alpha()
            self.text_surface.blit(
                pointer_surface, (pointer_loc - pointer_surface.get_width() * 0.5, 0))
            self.text_surface.blit(text_render, (0, 0))

        elif self.text:
            self.text_surface = self.font.render(
                self.text, True, self.text_color)

        else:
            self.text_surface = self.font.render(
                self.placeholder, True, (100, 100, 100, 100))

        self._pointer_animation_clock += dt
        if self._pointer_animation_clock >= 0.5:
            self._pointer_animation_clock -= 0.5
            self._pointer_animation_showing = not self._pointer_animation_showing

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

    def set_active_background_color(self, color: tuple):
        self.active_background_color = color

    def set_inactive_background_color(self, color: tuple):
        self.inactive_background_color = color

    def set_hover_background_color(self, color: tuple):
        self.hover_background_color = color

    def set_on_hover(self, func):
        '''Set action when the text box is hovered on

        Parameters
        ----------
        func
            Function to be called, take in 1 argument: self
        '''
        self._on_hover_action = func

    def set_on_not_hover(self, func):
        '''Set action when the text box is hovered off

        Parameters
        ----------
        func
            Function to be called, take in 1 argument: self
        '''
        self._on_not_hover_action = func

    def set_mouse_button(self, button: int):
        '''Set clicked mouse button on the text box to activate, or else any mouse button can activate it

        Parameters
        ----------
        button : pygame mouse button, left-1, middle-2, right-3'''
        self._activate_mouse_button = button

    def set_activate_key(self, key: int):
        '''Set pressed key to activate text box

        Parameters
        ----------
        button : pygame keyboard key'''
        self._activate_key = key

    def activate(self):
        '''Set text box to active'''
        self.background_color = self.active_background_color
        if self._on_active_action and not self.active:
            self._on_active_action(self)
        self.active = True

    def deactivate(self):
        '''Set text box to inactive'''
        self.background_color = self.inactive_background_color
        if self._on_inactive_action and self.active:
            self._on_inactive_action(self)
        self.active = False

    def set_on_active(self, func):
        '''Set action when the text box is clicked and set from not active to active

        Parameters
        ----------
        func
            Function to be called, take in 1 argument: self
        '''
        self._on_active_action = func

    def set_on_inactive(self, func):
        '''Set action when the text box is set from active to not active

        Parameters
        ----------
        func
            Function to be called, take in 1 argument: self
        '''
        self._on_active_action = func

    def set_on_submit(self, func, do_default: bool = True):
        '''Set action when return is pressed

        Parameters
        ----------
        func
            Function to be called, take in 1 argument: self
        do_default
            Whether to clear text and set inactive or not
            If you wish to clear text on your own, be sure to call the clear_text method
        '''
        self._submit_action = func
        self._submit_do_default = do_default

    def clear_text(self):
        self.text = ""
        self.pointer = 0

    def on_submit(self):
        if self._submit_action:
            self._submit_action(self)
        if not self._submit_do_default:
            return

        self.pointer = 0
        self.text = ""
        self.background_color = self.inactive_background_color
        if self._on_inactive_action:
            self._on_inactive_action(self)
        self.active = False

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            self.outline_color,
            (self.x - self.outline_width,
             self.y - self.outline_width,
             self.width + self.outline_width * 2,
             self.height + self.outline_width * 2),
            border_radius=self.border_radius,
            border_top_left_radius=self.border_top_left_radius,
            border_top_right_radius=self.border_top_right_radius,
            border_bottom_left_radius=self.border_bottom_left_radius,
            border_bottom_right_radius=self.border_bottom_right_radius)
        if self.background_image:
            screen.blit(self.background_image, (self.x, self.y))
            display_surface = pygame.Surface(
                (self.width - self.padding * 2,
                 self.height - self.padding * 2), pygame.SRCALPHA, 32)
            display_surface = display_surface.convert_alpha()
        else:
            pygame.draw.rect(
                screen,
                self.background_color,
                self.rect,
                border_radius=self.border_radius,
                border_top_left_radius=self.border_top_left_radius,
                border_top_right_radius=self.border_top_right_radius,
                border_bottom_left_radius=self.border_bottom_left_radius,
                border_bottom_right_radius=self.border_bottom_right_radius)
            display_surface = pygame.Surface(
                (self.width - self.padding * 2,
                 self.height - self.padding * 2))
            display_surface.fill(self.background_color)
        display_surface.blit(self.text_surface, (-self._position_shift, 0))
        screen.blit(
            display_surface,
            (self.x +
             self.padding,
             self.y +
             self.padding))
