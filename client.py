import pygame
pygame.init()

from network import Network
from pygame_textinput import TextInput

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

network = Network("ws://localhost:8765")

def draw_text(text, font:pygame.font.Font, text_color, x, y):
    img = font.render(text, color = text_color)
    screen.blit(img, (x, y))

font = pygame.font.get_default_font()
text_input = TextInput(100, 100, 400, 50, placeholder="input...", font=pygame.font.Font(None, 50), outline_width=2, outline_color=(255,0,0))

run = True
dt = 0
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            break
    if not run:
        break
    text_input.handle_event(events, dt)
    

    
    
    screen.fill((30, 30, 30))
    text_input.draw(screen)

    pygame.display.flip()

    
    dt = clock.tick(60)/1000
    









pygame.quit()