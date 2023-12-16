import pygame
from typing import Literal
import copy
from .toggle import ToggleButtonRect, ToggleButtonCircle

BASIC_RADIO_SELECTION_BUTTON = ToggleButtonCircle(0, 0, 7, (255,255,255), outline_color=(100,100,100), outline_width=1)
def _on_toggle_on(btn:ToggleButtonCircle):
    btn.color = (0, 100, 255)
def _on_toggle_off(btn:ToggleButtonCircle):
    btn.color = (255, 255, 255)
BASIC_RADIO_SELECTION_BUTTON.set_on_toggle(_on_toggle_on, _on_toggle_off)

class RadioInput:
    def __init__(self, x:int|float, y:int|float, width:int|float, height:int|float, title:str = "", options:list = [], arrangement:Literal["horizontal", "vertical"] = "vertical", active:bool = True) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.rect = pygame.Rect(x, y, width, height)
        self.options:list[RadioSelection] = []
        self.selected = None
        self.arrangement = arrangement
        self.active = active

        for option in options:
            if not isinstance(option, RadioSelection):
                option = RadioSelection(option, str(option))
            option.container = self
            self.options.append(option)
    

    def set_all_buttons(self, button:ToggleButtonRect|ToggleButtonCircle):
        for option in self.options:
            option.set_button(button)
    
    def set_all_font(self, font:pygame.font.Font):
        for option in self.options:
            option.font = font
    
    def set_all_text_position(self, text_position:Literal["top", "bottom", "left", "right"]):
        for option in self.options:
            option.text_position = text_position

    def set_all_text_color(self, color:tuple):
        for option in self.options:
            option.text_color = color
    

    
    def on_select(self, option):
        self.options[self.selected].unselect()
        self.selected = self.options.index(option)
    
    def handle_events(self, events:list, dt:float):
        '''Called at the start of every game loop

        Parameters
        ----------
        events: `list`
            Pass in the result from pygame.event.get(), be aware to only call this function once
        dt: `float`
            Time difference from last frame
        '''
        if self.active:
            for option in self.options:
                option.handle_events(events, dt)


    def draw(self, screen:pygame.Surface):
        for option in self.options:
            option.draw(screen)







class RadioSelection:
    def __init__(self, value, text:str = None, text_position:Literal["top", "bottom", "left", "right"] = "right", text_color:tuple = (0,0,0), font:pygame.font.Font = pygame.font.Font(None, 25), selected:bool = False, button:ToggleButtonRect|ToggleButtonCircle = BASIC_RADIO_SELECTION_BUTTON, active:bool = True, container:RadioInput|None = None, x:int=0, y:int=0) -> None:
        
        self.value = value
        self.text = text if text else str(value)
        self.text_position = text_position
        self.text_color = text_color
        self.font = font
        self.selected = selected
        self.x = x
        self.y = y
        self.text_x = x
        self.text_y = y

        self.button = button
        self.active = active
        self.container = container
    
    def set_position(self, x:int, y:int):
        self.x, self.y = x, y
        if self.text_position == "right":
            self.button.x, self.button.y = x, y
            self.text_x, self.text_y = self.x + self.button.width + self.button.outline_width
    
    
    def button_callback(self, button:ToggleButtonRect|ToggleButtonCircle):
        self.container.on_select(self)
        button.deactivate()
    
    def unselect(self):
        self.button.toggle(self.button)

    def set_button(self, button:ToggleButtonRect|ToggleButtonCircle):
        self.button = copy.deepcopy(button)
        self.button.value = self.value      
    
                

    def handle_events(self, events:list, dt:float):
        '''Called at the start of every game loop

        Parameters
        ----------
        events: `list`
            Pass in the result from pygame.event.get(), be aware to only call this function once
        dt: `float`
            Time difference from last frame
        '''
        if self.active:
            if not self.button:
                raise ValueError("Radio Selection Button Missing")
            self.button.handle_events(events, dt)
    
    
    def draw(self, screen:pygame.Surface):
        if not self.button:
            raise ValueError("Radio Selection Button Missing")
        text_surface = self.font.render(self.text, True, self.text_color)
        if self.text_position == "right":
            self.button.draw(screen)
            screen.blit(text_surface, (self.x+self.button.width, self.y))
        elif self.text_position == "left":
            screen.blit(text_surface, (self.x, self.y))

        







    