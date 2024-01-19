from controller import *
from service import *


def api(app):
    @app.route('/get_rating/<key>')
    def api_get_rating(key):
        return get_rating(key)

    @app.route('/get_color/<key>')
    def api_get_color(key):
        return get_color(key)

    @app.route('/close_session/<key>')
    def api_close_session(key):
        return close_session(key)

    @app.route('/create_board/<key>')
    def api_create_board(key):
        return create_board(key)

    @app.route('/check_board_is/<key>')
    def api_check_board_is(key):
        return check_board_is(key)

    @app.route('/register_user/<params>')
    def api_register_user(params):
        return register_user(params)

    @app.route('/login_user/<params>')
    def api_login_user(params):
        return login_user(params)

    @app.route('/check_move/<paramsAndKey>')
    def api_can_move(paramsAndKey):
        return can_move(paramsAndKey)

    @app.route('/get_board/<colorAndKey>')
    def api_load_board(colorAndKey):
        return load_board(colorAndKey)

    @app.route('/check_result/<key>')
    def api_check_result(key):
        return check_result(key)

    @app.route('/get_current_color/<key>')
    def api_get_current_color(key):
        return get_current_color(key)

    @app.route('/get_turns/<key>')
    def api_get_turns(key):
        return get_turns(key)

    @app.route('/tick')
    def api_check_online_player():
        return check_online_player()
