import pygame
import pygame_gui
from pygame_gui.core import ObjectID
pygame.init()

from network import Network

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

network = Network("ws://localhost:8765")

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "theme.json")
manager.set_visual_debug_mode(True)

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Say Hello',
                                             manager=manager)
game_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, -30, 200, 100),
                                         text="Test Game", manager=manager,
                                         anchors={'centerx': 'centerx',
                                         'bottom': 'bottom'}, object_id=ObjectID("#game_title", "@title"))

run = True
dt = 0
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            break

        manager.process_events(event)
                
    manager.update(dt)

    manager.draw_ui(screen)
    pygame.display.flip()

    
    dt = clock.tick(60)/1000
    









pygame.quit()