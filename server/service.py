from Chess import *
from random import randint
from turnlogger import TurnLogger
from controller import change_rating
import time
import server.parameters as para


def game_end(key):
    try:
        del para.turn_players[para.turn_players.index(key)]
    except Exception:
        pass
    try:
        del para.boards[key]
    except Exception:
        pass
    try:
        del para.last_online[key]
    except Exception:
        pass
    try:
        del para.player_won_exgmop[para.player_won_exgmop.index(key)]
    except Exception:
        pass


def create_board(key):
    try:
        my_index = para.turn_players.index(key)
        if len(para.turn_players) > 1:
            del para.turn_players[my_index]
            temp_board = Board()
            color_temp = randint(0, 1)
            logger_temp = TurnLogger()
            opponent_key = para.turn_players.pop(0)
            para.boards[key] = (temp_board, str(color_temp + 1), logger_temp,
                                opponent_key)
            para.boards[opponent_key] = (temp_board, str((not color_temp) + 1),
                                         logger_temp, key)
            try:
                del para.turn_players[para.turn_players.index(opponent_key)]
            except Exception:
                pass

            return 'OK'
        return 'waiting'
    except Exception:
        return 'error'


def get_color(key):
    try:
        print(para.boards[key][1])
        return para.boards[key][1]
    except Exception:
        return 'error'


def close_session(key):
    try:
        opponent_key = para.boards[key][3]
        para.player_won_exgmop.append(opponent_key)
    except Exception:
        pass
    try:
        del para.turn_players[para.turn_players.index(key)]
    except Exception:
        pass
    try:
        del para.boards[key]
    except Exception:
        pass
    try:
        del para.last_online[key]
    except Exception:
        pass
    try:
        del para.player_won_exgmop[para.player_won_exgmop.index(key)]
    except Exception:
        pass

    return ''


def check_board_is(key):
    if key in para.boards:
        try:
            del para.turn_players[para.turn_players.index(key)]
        except Exception:
            pass
        return 'OK'
    if key not in para.turn_players:
        para.turn_players.append(key)
    return 'waiting'


def can_move(paramsAndKey):
    try:
        params, key = paramsAndKey.split('***')
        para.board = para.boards[key][0]
        params = params.split(':')
        x1, y1, x2, y2 = map(int, params[:4])
        act = [7 - x1, 7 - y1, 7 - x2, 7 - y2]
        player = params[4]
        if player == 'w':
            act_player = 'b'
            x1, y1, x2, y2 = 7 - x1, y1, 7 - x2, y2
        else:
            x1, y1, x2, y2 = x1, 7 - y1, x2, 7 - y2
            act_player = 'b'
        result = para.board.move_piece(x1, y1, x2, y2)
        if result[0]:
            para.boards[key][2].register_turn(player, result[1])
        return '1' if result[0] else '0'
    except Exception:
        return 'error'


def load_board(colorAndKey):
    try:
        color, key = colorAndKey.split('***')
        para.board = para.boards[key][0]
        board_full = [['' for _ in range(8)] for __ in range(8)]
        if color == 'w':
            for i in range(8):
                for j in range(8):
                    board_full[i][j] = para.board.cell(i, 7 - j).replace('  ', '.')
                board_full[i] = '-'.join(board_full[i])
        elif color == 'b':
            for i in range(8):
                for j in range(8):
                    board_full[i][j] = para.board.cell(7 - i, j).replace('  ', '.')
                board_full[i] = '-'.join(board_full[i])
        board_full = '\n'.join(board_full)
        return board_full
    except Exception:
        return 'error'


def check_result(key):
    try:
        if key in para.player_won_exgmop:
            change_rating(key, 10)
            game_end(key)
            return 'WIN'
        para.board = para.boards[key][0]
        result = para.board.result()
        print(result)
        if result == '*':
            return 'False'
        if result == '1/2-1/2':
            game_end(key)
            return 'None'

        if result == '1-0':
            if para.boards[key][1] == '1':
                change_rating(key, 10)
                game_end(key)
                return 'WIN'
            else:
                change_rating(key, -10)
                game_end(key)
                return 'LOSS'
        if result == '0-1':
            if para.boards[key][1] == '2':
                change_rating(key, 10)
                game_end(key)
                return 'WIN'
            else:
                change_rating(key, -10)
                game_end(key)
                return 'LOSS'
    except Exception:
        pass
        return 'error'


def get_current_color(key):
    try:
        color = para.boards[key][0].turn
        if color:
            return 'w'
        return 'b'
    except Exception:
        return 'error'


def get_turns(key):
    try:
        para.last_online[key] = time.time()
        turns = para.boards[key][2].get_turns()
        return '*'.join(turns)
    except Exception:
        return 'error'


def check_online_player():
    try:
        for key, i in para.last_online.items():
            if time.time() - i > 10:
                try:
                    opponent_key = para.boards[key][3]
                    para.player_won_exgmop.append(opponent_key)
                except Exception:
                    pass
                try:
                    del para.turn_players[para.turn_players.index(key)]
                except Exception:
                    pass
                try:
                    del para.boards[key]
                except Exception:
                    pass
                try:
                    del para.last_online[key]
                except Exception:
                    pass
                try:
                    del para.player_won_exgmop[key]
                except Exception:
                    pass
    except Exception:
        pass
    return ''
