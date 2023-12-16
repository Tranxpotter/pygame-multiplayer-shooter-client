import pygame
pygame.init()

from network import Network
from pygame_input import ButtonRect, ButtonCircle, TextInput, RadioInput, RadioSelection, ToggleButtonRect, ToggleButtonCircle

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


def on_button_press(btn:ButtonRect):
    print(btn.value)
def on_button_hover(btn:ButtonRect):
    btn.display_dy = -10
    btn.display_dheight = 10
def on_not_button_hover(btn:ButtonRect):
    btn.display_dy = 0
    btn.display_dheight = 0
test_button = ButtonRect(700, 400, 50, 50, 2, outline_width=3, outline_color=(255, 0, 0))
test_button.set_on_click(on_button_press)
test_button.set_label("Hello world", pygame.font.Font(None, 30), (0, 255, 0))
test_button.value = "Hello World!"
test_button.set_hover(on_button_hover, on_not_button_hover)

circle_button = ButtonCircle(800, 500, 30)
circle_button.outline_width = 5
circle_button.outline_color = (255,0,0)
circle_button.set_on_click(lambda x:print("bruh"))

test_radio = RadioInput(700, 100, 200, 200, "hello", ["Hello"])
test_radio.set_all_text_color((255,255,255))



text_inputs = [username_input, password_input]
buttons = [test_button, circle_button]
radios = [test_radio]

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
    for button in buttons:
        button.handle_events(events, dt)
    for radio in radios:
        radio.handle_events(events, dt)

    
    screen.fill((30, 30, 30))
    for text_input in text_inputs:
        text_input.draw(screen)
    for button in buttons:
        button.draw(screen)
    for radio in radios:
        radio.draw(screen)

    pygame.display.flip()

    
    dt = clock.tick(60)/1000
    









pygame.quit()