import client.parameters as para
from client.component.button import Button
from client.tools import load_image, get_text_rendered, terminate


def start_screen(pygame, screen, clock):
    hello_text = 'WELCOME TO THE WORLD OF CHESS!'
    name_developer_text = 'Viethq'
    nickname_developer_text = 'Github nickname: viethq'
    offline_mode_button = Button(395, 300, 20, 5, 260, 43, 'Offline Mode!', 49)
    online_mode_button = Button(395, 400, 20, 5, 260, 43, 'Online Mode!', 49)
    exit_button = Button(395, 500, 90, 5, 260, 43, 'Exit!', 49)
    fon = pygame.transform.scale(load_image(pygame, 'fon.jpg'), (para.WIDTH, para.HEIGHT))
    screen.blit(fon, (0, 0))
    screen.blit(*get_text_rendered(pygame, hello_text, (0, 30), 60, True))
    screen.blit(*get_text_rendered(pygame, name_developer_text,
                                   (10, 700), 50, italic=True))
    screen.blit(*get_text_rendered(pygame, nickname_developer_text,
                                   (10, 750), 50, italic=True))
    offline_mode_button.render(screen)
    online_mode_button.render(screen)
    exit_button.render(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(pygame, para.player_key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                key = event.button
                pos = event.pos
                if key == 1:
                    online = online_mode_button.check_coords(pos)
                    offline = offline_mode_button.check_coords(pos)
                    exit_game = exit_button.check_coords(pos)
                    if offline:
                        para.GAMEMODE = 0
                    if online:
                        para.GAMEMODE = 1
                    if exit_game:
                        terminate(pygame, para.player_key)
        pygame.display.flip()
        clock.tick(para.FPS)
