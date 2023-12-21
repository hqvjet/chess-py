from Chess import *
from random import randint
from turnlogger import TurnLogger
from controller import change_rating
import time


def game_end(key, turn_players, boards, last_online, player_won_exgmop):
    try:
        del turn_players[turn_players.index(key)]
    except Exception:
        pass
    try:
        del boards[key]
    except Exception:
        pass
    try:
        del last_online[key]
    except Exception:
        pass
    try:
        del player_won_exgmop[player_won_exgmop.index(key)]
    except Exception:
        pass


def create_board(key):
    try:
        global turn_players
        global boards
        my_index = turn_players.index(key)
        if len(turn_players) > 1:
            del turn_players[my_index]
            temp_board = Board()
            color_temp = randint(0, 1)
            logger_temp = TurnLogger()
            opponent_key = turn_players.pop(0)
            boards[key] = (temp_board, str(color_temp + 1), logger_temp,
                           opponent_key)
            boards[opponent_key] = (temp_board, str((not color_temp) + 1),
                                    logger_temp, key)
            try:
                del turn_players[turn_players.index(opponent_key)]
            except Exception:
                pass

            return 'OK'
        return 'waiting'
    except Exception:
        return 'error'


def get_color(key):
    try:
        return boards[key][1]
    except Exception:
        return 'error'


def close_session(key, player_won_exgmop, last_online):
    try:
        opponent_key = boards[key][3]
        player_won_exgmop.append(opponent_key)
    except Exception:
        pass
    try:
        del turn_players[turn_players.index(key)]
    except Exception:
        pass
    try:
        del boards[key]
    except Exception:
        pass
    try:
        del last_online[key]
    except Exception:
        pass
    try:
        del player_won_exgmop[player_won_exgmop.index(key)]
    except Exception:
        pass

    return ''


def check_board_is(key, boards, ):
    if key in boards:
        try:
            del turn_players[turn_players.index(key)]
        except Exception:
            pass
        return 'OK'
    if key not in turn_players:
        turn_players.append(key)
    return 'waiting'


def can_move(paramsAndKey):
    try:
        params, key = paramsAndKey.split('***')
        board = boards[key][0]
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
        result = board.move_piece(x1, y1, x2, y2)
        if result[0]:
            boards[key][2].register_turn(player, result[1])
        return '1' if result[0] else '0'
    except Exception:
        return 'error'


def load_board(colorAndKey):
    try:
        color, key = colorAndKey.split('***')
        board = boards[key][0]
        board_full = [['' for _ in range(8)] for __ in range(8)]
        if color == 'w':
            for i in range(8):
                for j in range(8):
                    board_full[i][j] = board.cell(i, 7 - j).replace('  ', '.')
                board_full[i] = '-'.join(board_full[i])
        elif color == 'b':
            for i in range(8):
                for j in range(8):
                    board_full[i][j] = board.cell(7 - i, j).replace('  ', '.')
                board_full[i] = '-'.join(board_full[i])
        board_full = '\n'.join(board_full)
        return board_full
    except Exception:
        return 'error'


def check_result(key, player_won_exgmop):
    try:
        if key in player_won_exgmop:
            change_rating(key, 10)
            game_end(key)
            return 'WIN'
        board = boards[key][0]
        result = board.result()
        if result == '*':
            return 'False'
        if result == '1/2-1/2':
            game_end(key)
            return 'None'

        if result == '1-0':
            if boards[key][1] == '1':
                change_rating(key, 10)
                game_end(key)
                return 'WIN'
            else:
                change_rating(key, -10)
                game_end(key)
                return 'LOSS'
        if result == '0-1':
            if boards[key][1] == '2':
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
        color = boards[key][0].turn
        if color:
            return 'w'
        return 'b'
    except Exception:
        return 'error'


def get_turns(key, last_online):
    try:
        last_online[key] = time.time()
        turns = boards[key][2].get_turns()
        return '*'.join(turns)
    except Exception:
        return 'error'


def check_online_player(last_online, player_won_exgmop):
    try:
        for key, i in last_online.items():
            if time.time() - i > 10:
                try:
                    opponent_key = boards[key][3]
                    player_won_exgmop.append(opponent_key)
                except Exception:
                    pass
                try:
                    del turn_players[turn_players.index(key)]
                except Exception:
                    pass
                try:
                    del boards[key]
                except Exception:
                    pass
                try:
                    del last_online[key]
                except Exception:
                    pass
                try:
                    del player_won_exgmop[key]
                except Exception:
                    pass
    except Exception:
        pass
    return ''
