from client.api import register, login_user
from client.tools import terminate, load_image, get_text_rendered
from client.component.button import Button
from client.component.textInput import TextInput
import client.parameters as para


def login_screen(pygame, screen, clock):
    error_type = 0
    main_text = 'Enlist your name here in the hall of fame:'
    login_indicator_text = 'Username:'
    pass_indicator_text = 'Password:'
    register_login_error = 'Oops! There is a register error occurs, try again'
    login_data_error = 'Oops! Wrong Password, try again'
    server_connect_error = 'Oops! There is a connect error occurs, try again'
    login_button = Button(400, 600, 35, 7, 200, 50, 'Login Now!', 35)
    register_button = Button(375, 670, 23, 15, 250, 50,
                             'Register Now!', 45)
    login_input = TextInput(400, 450, 200, 30, 40, 13)
    pass_input = TextInput(400, 550, 200, 30, 40, 13, True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(pygame, para.player_key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                key = event.button
                pos = event.pos
                if key == 1:
                    login = login_button.check_coords(pos)
                    reg = register_button.check_coords(pos)
                    login_input.check_coords(pos)
                    pass_input.check_coords(pos)
                    if reg:
                        if login_input.get_text() and pass_input.get_text():
                            ok = register(login_input.get_text(),
                                          pass_input.get_text())
                            if ok[0]:
                                para.player_key = ok[1]
                                return
                            else:
                                if ok[1] == 'errorName':
                                    error_type = 1
                                elif ok[1] == 'errorConnect':
                                    error_type = 10
                                login_input.clear()
                                pass_input.clear()
                    elif login:
                        if login_input.get_text() and pass_input.get_text():
                            ok = login_user(login_input.get_text(),
                                            pass_input.get_text())
                            if ok[0]:
                                para.player_key = ok[1]
                                return
                            else:
                                if ok[1] == 'errorData':
                                    error_type = 2
                                elif ok[1] == 'errorConnect':
                                    error_type = 10
                                login_input.clear()
                                pass_input.clear()

            elif event.type == pygame.KEYDOWN:
                login_input.update(event)
                pass_input.update(event)

        screen.fill((0, 0, 0))
        fon = pygame.transform.scale(load_image(pygame, 'fon.jpg'), (para.WIDTH, para.HEIGHT))
        screen.blit(fon, (0, 0))
        screen.blit(*get_text_rendered(pygame, main_text, (0, 30), 49, True))
        screen.blit(*get_text_rendered(pygame, login_indicator_text, (0, 400),
                                       49, True))
        screen.blit(*get_text_rendered(pygame, pass_indicator_text, (0, 500),
                                       49, True))
        login_button.render(screen)
        register_button.render(screen)
        login_input.render(screen)
        pass_input.render(screen)
        if error_type == 1:
            screen.blit(*get_text_rendered(pygame, register_login_error, (0, 730),
                                           49, True))
        elif error_type == 2:
            screen.blit(*get_text_rendered(pygame, login_data_error, (0, 730),
                                           40, True))
        elif error_type == 10:
            screen.blit(*get_text_rendered(pygame, server_connect_error, (0, 730),
                                           40, True))
        pygame.display.flip()
        clock.tick(para.FPS)
