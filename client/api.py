import requests
import client.parameters as para


def register(login, passwd):
    try:
        ok = requests.get(para.SERVER_ADDRESS +
                          'register_user/{}\n{}'.format(login, passwd)).text
        if ok == 'error':
            return False, 'errorName'
        return True, ok
    except Exception:
        return False, 'errorConnect'


def login_user(login, passwd):
    try:
        key = requests.get(para.SERVER_ADDRESS +
                           'login_user/{}\n{}'.format(login, passwd)).text
        if key == 'error':
            return False, 'errorData'
        return True, key
    except Exception:
        return False, 'errorConnect'


def get_rating(player_key):
    rating = requests.get(para.SERVER_ADDRESS +
                          'get_rating/{}'.format(player_key)).text
    if rating == 'error':
        print("Ошибка получения рейтинга!")
        return ''
    return rating


def find_opponent(player_key):

    try:
        board_is = requests.get(para.SERVER_ADDRESS +
                                'check_board_is/{}'.format(player_key)).text
        if board_is == 'OK':
            para.COLOR = int(requests.get(para.SERVER_ADDRESS +
                                     'get_color/{}'.format(player_key)).text)
            return True

        create = requests.get(para.SERVER_ADDRESS +
                              'create_board/{}'.format(player_key)).text
        if create == 'OK':
            para.COLOR = int(requests.get(para.SERVER_ADDRESS +
                                     'get_color/{}'.format(player_key)).text)
            return True
    except Exception:
        pass
    return False


def check_result(player_key):
    result = requests.get(para.SERVER_ADDRESS +
                          'check_result/{}'.format(player_key)).text
    print(result)
    if result not in ['False', 'error']:
        if result == 'WIN':
            return 1
        elif result == 'LOSS':
            return 2
        elif result == 'None':
            return 3
    else:
        return False
