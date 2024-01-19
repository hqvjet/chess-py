import math
import time

import client.parameters as para
from client.api import find_opponent
from client.component.button import Button
from client.component.figure import init_figure_images
from client.tools import load_image, terminate, get_text_rendered
from client.ui.game import main_game
from client.ui.onlineMode import menu_screen


def finding_opponent_screen(pygame, screen, clock):
    earth = load_image(pygame, 'earth.jpg')
    lupa = load_image(pygame, 'lupa.png')
    x = 0
    lupa_circle = 0
    R = 150
    act = 0
    search_indicator_text = 'Searching for Opponent:'
    cancel_button = Button(440, 720, 10, 7, 120, 40, 'Cancel', 40)
    search_time_text = '60'
    start_time = time.time()
    pygame.time.set_timer(para.GET_ACT_TIMER, 1000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(pygame, para.player_key)
            if event.type == para.GET_ACT_TIMER:
                ok = find_opponent(para.player_key)
                if ok:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                key = event.button
                pos = event.pos
                cancel_search = cancel_button.check_coords(pos)
                if cancel_search:
                    return False
        if time.time() - start_time > 59:
            return False
        screen.fill((0, 0, 0))
        rel_x = x % earth.get_rect().width
        screen.blit(earth, (rel_x - earth.get_rect().width, 0))
        if rel_x < para.WIDTH:
            screen.blit(earth, (rel_x, 0))
        x -= 2
        lupa_x = int(R * math.cos(math.radians(lupa_circle)) + 250)
        lupa_y = int(R * math.sin(math.radians(lupa_circle)) + 250)
        lupa_circle += 2
        search_time_text = str(int(60 - (time.time() - start_time)))
        screen.blit(lupa, (lupa_x, lupa_y))
        screen.blit(*get_text_rendered(pygame, search_indicator_text, (20, 20), 49))
        screen.blit(*get_text_rendered(pygame, search_time_text, (550, 20), 49))
        cancel_button.render(screen)
        pygame.display.flip()
        clock.tick(para.FPS)


def start_finding_opponent(pygame, screen, clock):
    init_figure_images(pygame)
    while True:
        if not para.first_in:
            pygame.mixer.music.play(-1)
        while True:
            menu_screen(pygame, screen, clock)
            ok = finding_opponent_screen(pygame, screen, clock)
            if ok:
                break
        pygame.mixer.music.stop()
        main_game(pygame, screen, clock)
        para.first_in = False


