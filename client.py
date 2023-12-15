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


username_input = TextInput(100, 100, 400, 50, placeholder="username", font=pygame.font.Font(None, 50), outline_width=2, outline_color=(255,0,0), padding=10)
username_input.set_advanced_border_radius(30,30,30,30)
username_input.set_mouse_button(1)
username_input.set_activate_key(pygame.K_RETURN)

password_input = TextInput(100, 200, 400, 50, placeholder="password", font=pygame.font.Font(None, 50), outline_width=2, outline_color=(255,0,0))
def on_login(_):
    username = username_input.text
    password = password_input.text
    if not username or not password:
        draw_text("Both username and password are needed", pygame.font.Font(None, 30), (255,255,255), 100, 270)
        return
    network.send()



text_inputs = [username_input, password_input]

run = True
dt = 0
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            break
        
        
    
    
    for text_input in text_inputs:
        text_input.handle_events(events, dt)

    
    screen.fill((30, 30, 30))
    for text_input in text_inputs:
        text_input.draw(screen)

    pygame.display.flip()

    
    dt = clock.tick(60)/1000
    









pygame.quit()