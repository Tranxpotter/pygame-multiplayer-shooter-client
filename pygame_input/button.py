import pygame


class ButtonRect:
    def __init__(self, x:int|float, y:int|float, width:int|float, height:int|float, border_radius:int|float = 0, color:tuple = (255, 255, 255), padding:int = 0, outline_color:tuple = (0,0,0), outline_width:int = 1, value = None, active:bool = True) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height)
        self.border_radius = border_radius
        self.color = color
        self.padding = padding
        self.outline_color = outline_color
        self.outline_width = outline_width
        
        self.label_text = None
        self.label_font = None
        self.label_color = None

        self.value = value
        self.active = active

        self.on_hover_action = None
        self.on_not_hover_action = None
        self.hovering = False

        self.on_click_action = None
        


        if width <= padding*2 or height <= padding*2:
            raise ValueError(
                "Height and Width must be bigger than 2 times of padding")
    
    def set_label(self, text:str, font:pygame.font.Font = pygame.font.Font(None, 10), color:tuple = (0,0,0)):
        '''Set the text, font and text color of the text on the button'''
        self.label_text = text
        self.label_font = font
        self.label_color = color
    
    def set_on_hover(self, func):
        '''Set action when the button is hovered on

        Parameters
        ----------
        func
            Function to be called, take in 1 argument: self
        '''
        self.on_hover_action = func
    def set_on_not_hover(self, func):
        '''Set action when the button is hovered off

        Parameters
        ----------
        func
            Function to be called, take in 1 argument: self
        '''
        self.on_not_hover_action = func
    
    def set_on_click(self, func):
        '''Set action when the button is clicked

        Parameters
        ----------
        func
            Function to be called, take in 1 argument: self
        '''
        self.on_click_action = func
    
    def handle_events(self, events:list, dt:float):
        '''Called at the start of every game loop

        Parameters
        ----------
        events: `list`
            Pass in the result from pygame.event.get(), be aware to only call this function once
        dt: `float`
            Time difference from last frame
        '''

        for event in events:
            #Hover handling
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if self.on_hover_action and not self.hovering:
                        self.on_hover_action(self)
                    self.hovering = True
                else:
                    if self.on_not_hover_action and self.hovering:
                        self.on_not_hover_action(self)
                    self.hovering = False
            #Click handling
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.on_click_action:
                    
    
                    







