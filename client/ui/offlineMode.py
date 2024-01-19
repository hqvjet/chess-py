import client.parameters as para
from client.component.figure import init_figure_images
from client.tools import load_image, get_text_rendered, terminate
from client.api import get_rating
from client.component.button import Button
from client.ui.game import main_game


def select_diff(pygame, screen, clock):
    init_figure_images(pygame)
    mode_indicator_text = 'Choose Difficult'
    easy_diff_button = Button(395, 300, 65, 5, 210, 43, 'Easy!', 49)
    medium_diff_button = Button(395, 360, 45, 5, 210, 43, 'Medium!', 49)
    hard_diff_button = Button(395, 420, 65, 5, 210, 43, 'Hard!', 49)
    back_button = Button(395, 480, 65, 5, 210, 43, 'Back', 49)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(pygame, para.player_key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                key = event.button
                pos = event.pos
                if key == 1:
                    easy = easy_diff_button.check_coords(pos)
                    medium = medium_diff_button.check_coords(pos)
                    hard = hard_diff_button.check_coords(pos)
                    back = back_button.check_coords(pos)

                    if easy:
                        main_game(pygame, screen, clock)
                    if medium:
                        main_game(pygame, screen, clock)
                    if hard:
                        main_game(pygame, screen, clock)
                    if back:
                        para.BACK_TO = 'start_screen'
                        para.GAMEMODE = None
                        return
        screen.fill((0, 0, 0))
        fon = pygame.transform.scale(load_image(pygame, 'fon.jpg'), (para.WIDTH, para.HEIGHT))
        screen.blit(fon, (0, 0))
        screen.blit(*get_text_rendered(pygame, mode_indicator_text, (230, 160), 100))
        easy_diff_button.render(screen)
        medium_diff_button.render(screen)
        hard_diff_button.render(screen)
        back_button.render(screen)
        pygame.display.flip()
        clock.tick(para.FPS)
