import json
import os
import asyncio

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
network.start_connection()


manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), "theme.json")
manager.set_visual_debug_mode(True)

ANCHOR_CENTER = {"centerx":"centerx", "centery":"centery"}
game_title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, 0, 1280, 100),
                                         text="Multiplayer Shooter Test Game", manager=manager,
                                         anchors={'centerx': 'centerx',
                                         'top': 'top'}, object_id=ObjectID("#game_title", "@title"))

username_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(0, -50, 300, 50), 
                                                     manager=manager, 
                                                     object_id=ObjectID("#username_input", "@login_input"), 
                                                     placeholder_text="username", 
                                                     anchors=ANCHOR_CENTER)

password_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(0, 50, 300, 50), 
                                                     manager=manager, 
                                                     object_id=ObjectID("#password_input", "@login_input"), 
                                                     placeholder_text="password", 
                                                     anchors=ANCHOR_CENTER)
password_input.set_text_hidden()

error_display = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, 150, 200, 50),
                                            manager=manager,
                                            object_id=ObjectID("#error_display", "@error_display"), 
                                            text="", 
                                            anchors=ANCHOR_CENTER)
error_display.visible = 0

signin_options = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0, -100, 100, 50), 
                                            manager=manager,
                                            object_id=ObjectID("#signin_options", "@signin_options"),
                                            text="login", 
                                            anchors = ANCHOR_CENTER)

submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(180, 50, 50, 50), 
                                             manager=manager,
                                             object_id=ObjectID("#submit_button", "@submit_button"),
                                             text="->",
                                             anchors=ANCHOR_CENTER)


async def on_signin():
    print(1)
    if not username_input.text:
        error_display.visible = 1
        error_display.set_text("username is required")
        return
    elif not password_input.text:
        error_display.visible = 1
        error_display.set_text("password is required")
        return
    
    
    
    signin_info = {"mode":signin_options.text, 
                   "username":username_input.text, 
                   "password":password_input.text}
    
    password_input.clear()
    
    try:
        await network.send(json.dumps(signin_info))
    except:
        return
    
    try:
        result = await network.recv()
    except asyncio.TimeoutError as e:
        error_display.set_text("Connection Timeout")
        return
    except:
        return
    
    print(f"{result=}")
    result = json.loads(result)

    if result["failed"]:
        error_display.visible = 1
        error_display.set_text(result["error_message"])
        return
    
    error_display.visible = 0
    submit_button.disable()


def on_connection_error():
    error_display.visible = 1
    error_display.set_text("Not connected to server")
network.set_on_connection_error(on_connection_error)
    
    

async def main():
    run = True
    dt = 0
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                await network.websocket.close()
                run = False
                break

            elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_object_id == "#username_input":
                    username_input.unfocus()
                    password_input.focus()
                elif event.ui_object_id == "#password_input":
                    password_input.unfocus()
                    await on_signin()
            
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_object_id == "#signin_options":
                    if signin_options.text == "login":
                        signin_options.set_text("signup")
                    else:
                        signin_options.set_text("login")
                elif event.ui_object_id == "#submit_button":
                    await on_signin()
                

            manager.process_events(event)
        
                    
        manager.update(dt)

        manager.draw_ui(screen)
        pygame.display.flip()

        
        dt = clock.tick(60)/1000
    






if __name__ == "__main__":
    asyncio.run(main())
    pygame.quit()