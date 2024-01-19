import chess

import client.parameters as para
from client.board import Board, convert_to_fen
from client.component.figure import Figure
from client.tools import terminate
from client.ui.gameEnd import game_end_screen
from client.api import check_result as server_check_result


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
                result = check_result(para.board) if para.GAMEMODE == 0 else server_check_result(para.player_key)
                print(result)
                if result:
                    game_end_screen(pygame, screen, result, clock)
                    return
                if para.GAMEMODE == 1:
                    para.board.update_board()
                    para.board.get_current_turn()
                    para.board.get_turns()
                    update_board(pygame)
                else:
                    file_update_board()
                    get_current_turn()
                    # para.board.get_turns()
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
    if para.GAMEMODE == 0:
        para.COLOR = 1
    para.board = Board(8, 8, para.COLOR)
    para.board.set_view(1, 1, 100)


def load_level(filename):
    filename = "res/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip().split('-') for line in mapFile]
    max_width = max(map(len, level_map))
    return level_map


def get_board_from_file(filename):
    result_string = ''
    filename = "res/" + filename
    # Read the file and process each line
    with open(filename, 'r') as file:
        for line in file:
            result_string += line.strip() + '\n'

    return result_string


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


def check_result(board_state):
    fen_board = convert_to_fen(get_board_from_file('board_temp.txt'))
    final = chess.Board(fen=fen_board)
    result = final.result()
    print(result)
    if result == '1/2-1/2':
        return 'Draw!'
    elif result == '1-0':
        return 'Win!'
    elif result == '0-1':
        return 'Loss!'
    else:
        return 'None'


def get_current_turn():
    fen_board = convert_to_fen(get_board_from_file('board_temp.txt'))
    final = chess.Board(fen=fen_board)
    para.board.turns = 'w' if final.turn == chess.WHITE else 'b'


def file_update_board():
    if len(para.board.board):
        with open('res/board_temp.txt', 'w') as data:
            data.write(para.board.board)
