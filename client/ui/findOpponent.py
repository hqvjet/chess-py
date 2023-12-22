import math
import time
import client.parameters as para

from client.board import Board
from client.api import find_opponent, check_result
from client.tools import load_image, terminate, get_text_rendered
from client.ui.gameEnd import game_end_screen
from client.ui.onlineMode import menu_screen
from client.component.button import Button
from client.component.figure import Figure, init_figure_images


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


def main_game(pygame, screen, clock):
    board_init()
    para.board.set_key(para.player_key)
    make_board()
    running = True

    pygame.time.set_timer(para.GET_ACT_TIMER, 1000)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(pygame, para.player_key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                para.board.get_click(event.pos, event.button)
            if event.type == para.GET_ACT_TIMER:
                result = check_result(para.player_key)
                # print(result)
                if result:
                    print('end game')
                    game_end_screen(pygame, screen, result, clock)
                    return
                para.board.update_board()
                para.board.get_current_turn()
                para.board.get_turns()
                update_board(pygame)

        if para.board.get_update_status():
            coords = para.board.get_update_coords()
            if coords is not None:
                sprites = para.figures_sprites.sprites()
                for i in range(len(sprites)):
                    if sprites[i].get_coords() == coords[1]:
                        para.figures_sprites.remove(sprites[i])
                        para.board.updated()
                for i in range(len(sprites)):
                    if sprites[i].get_coords() == coords[0]:
                        sprites[i].update_coords(coords[1])
                        para.board.updated()
            para.board.need_update = None

        screen.fill((0, 0, 0))
        para.board.render(screen)
        para.figures_sprites.draw(screen)
        pygame.display.flip()


def board_init():
    para.board = Board(8, 8, para.COLOR)
    para.board.set_view(1, 1, 100)


def load_level(filename):
    filename = "res/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip().split('-') for line in mapFile]
    max_width = max(map(len, level_map))
    return level_map


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] != '.':
                Figure(level[y][x], x, y, para.figures_sprites)
                para.board.change_figure(x, y, level[y][x])


def make_board():
    print(para.COLOR)
    if para.COLOR == 1:
        generate_level(load_level('map_white.txt'))
    elif para.COLOR == 2:
        generate_level(load_level('map_black.txt'))


def update_board(pygame):
    try:
        bord = load_level('board_temp.txt')
        para.figures_sprites = pygame.sprite.Group()
        generate_level(bord)
    except Exception:
        pass
