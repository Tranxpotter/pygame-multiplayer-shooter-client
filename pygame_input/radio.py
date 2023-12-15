import pygame
from typing import Literal

class RadioInput:
    def __init__(self, x:int|float, y:int|float, width:int|float, height:int|float, options:list = []) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.options = []

        for option in options:
            if not isinstance(option, RadioSelection):
                self.options.append(RadioSelection(option))
            else:
                self.options.append(option)
        
    
    
    def handle_events(self, events:list, dt:float):
        '''Called at the start of every game loop

        Parameters
        ----------
        events: `list`
            Pass in the result from pygame.event.get(), be aware to only call this function once
        dt: `float`
            Time difference from last frame
        '''









class RadioSelection:
    def __init__(self, value, text:str = None, selected = False) -> None:
        self.value = value
        self.text = text if text else str(value)
        self.selected = selected
        self.x = None
        self.y = None
    
    def set_position(self, x:int, y:int):
        self.x = x
        self.y = y

    def style(self):
        pass
    