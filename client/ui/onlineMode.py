import client.parameters as para
from client.tools import load_image, get_text_rendered, terminate
from client.api import get_rating
from client.component.button import Button


def menu_screen(pygame, screen, clock):
    get_rating(para.player_key)
    rating_indicator_text = 'Point: '
    rating_text = get_rating(para.player_key)
    start_game_button = Button(370, 300, 65, 5, 210, 43, 'Start!', 49)
    exit_prog_button = Button(370, 400, 65, 5, 210, 43, 'Exit!', 49)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(pygame, para.player_key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                key = event.button
                pos = event.pos
                if key == 1:
                    exit_game = exit_prog_button.check_coords(pos)
                    start_game = start_game_button.check_coords(pos)
                    if exit_game:
                        terminate(pygame, para.player_key)
                    if start_game:
                        return
        screen.fill((0, 0, 0))
        fon = pygame.transform.scale(load_image(pygame, 'fon.jpg'), (para.WIDTH, para.HEIGHT))
        screen.blit(fon, (0, 0))
        screen.blit(*get_text_rendered(pygame, rating_indicator_text, (30, 30), 49))
        screen.blit(*get_text_rendered(pygame, rating_text, (270, 30), 49))
        start_game_button.render(screen)
        exit_prog_button.render(screen)
        pygame.display.flip()
        clock.tick(para.FPS)
