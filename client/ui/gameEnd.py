import random
import client.parameters as para

from client.tools import load_image, terminate, get_text_rendered
from client.component.button import Button
from client.component.particle import Particle


def game_end_screen(pygame, screen, mode, clock):
    star = False
    is_first = True
    fon = pygame.transform.scale(load_image(pygame, 'game_end.jpg'), (para.WIDTH, para.HEIGHT))
    partion_end_text = 'RESULT!'
    exit_menu_button = Button(375, 700, 5, 5, 250, 43, 'Exit', 49)
    if mode == 3:
        para.game_end_text = 'DRAW!'
    elif mode == 1:
        para.game_end_text = 'WIN!'
        star = True
    elif mode == 2:
        para.game_end_text = 'LOSE!'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(pygame, para.player_key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                exit_menu = exit_menu_button.check_coords(event.pos)
                if exit_menu:
                    return
        if star and is_first:
            is_first = False
            create_particles(pygame, (500, 400))

        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        screen.blit(*get_text_rendered(pygame, partion_end_text, (30, 30), 49, True))
        screen.blit(*get_text_rendered(pygame, para.game_end_text, (270, 100), 49, True))
        exit_menu_button.render(screen)
        para.sprites_star.update()
        para.sprites_star.draw(screen)
        pygame.display.flip()
        clock.tick(para.FPS)


def create_particles(pygame, position):
    particle_count = 600
    numbers = range(-50, 50)
    for _ in range(particle_count):
        Particle(pygame, position, random.choice(numbers), random.choice(numbers))
