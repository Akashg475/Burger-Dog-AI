import os
import sys
import pygame
from game_env import BurgerDogEnvironment

pygame.init()

# Set Display Surface
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

burger_dog = BurgerDogEnvironment(WINDOW_WIDTH, WINDOW_HEIGHT)

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Colors
ORANGE = (246, 170, 54)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font
assets_path = os.path.dirname(__file__)
font = pygame.font.Font(os.path.join(assets_path, "assets", "WashYourHand.ttf"), 32)


class HUD:
    def __init__(self, prefix, variable, suffix, color, **kwargs):

        self.prefix = prefix
        self.suffix = suffix
        self.color = color

        self.surface = font.render(f"{prefix}{str(variable)}{suffix}", True, color)
        self.rect = self.surface.get_rect()

        if kwargs.get("top_left", None):
            self.rect.topleft = kwargs["top_left"]
        if kwargs.get('centerx', None):
            self.rect.centerx = kwargs["centerx"]
        if kwargs.get('y', None):
            self.rect.y = kwargs['y']
        if kwargs.get("top_right"):
            self.rect.topright = kwargs["top_right"]

    def update_variable(self, variable):
        self.surface = font.render(f"{self.prefix}{str(variable)}{self.suffix}", True, self.color)


HUD_ITEMS = {
    'burger_points_hud': HUD("Burger Points: ", burger_dog.burger_points, '', ORANGE, top_left=(10, 10)),
    'score_hud': HUD("Score: ", burger_dog.score, '', ORANGE, top_left=(10, 50)),
    'title_hud': HUD("Burger Dog", '', '', ORANGE, centerx=WINDOW_WIDTH // 2, y=10),
    'burger_eaten_hud': HUD("Burger Eaten: ", burger_dog.burger_eaten, '', ORANGE, centerx=WINDOW_WIDTH // 2, y=50),
    'player_lives_hud': HUD("Lives: ", burger_dog.player_lives, '', ORANGE, top_right=(WINDOW_WIDTH - 10, 10)),
    'boost_hud': HUD("Boost: ", burger_dog.boost_level, '', ORANGE, top_right=(WINDOW_WIDTH - 10, 50)),
}

# Set sounds and music
bark_sound = pygame.mixer.Sound(os.path.join(assets_path, "assets", "bark_sound.wav"))
miss_sound = pygame.mixer.Sound(os.path.join(assets_path, "assets", "miss_sound.wav"))
bg_music = pygame.mixer.Sound(os.path.join(assets_path, "assets", "bd_background_music.wav"))

# Set images
player_image_right = pygame.image.load(os.path.join(assets_path, "assets", "dog_right.png"))
player_image_left = pygame.image.load(os.path.join(assets_path, "assets", "dog_left.png"))
player_image = player_image_right
burger_dog.player_rect = player_image.get_rect()

burger_image = pygame.image.load(os.path.join(assets_path, "assets", "burger.png"))
burger_dog.burger_rect = burger_image.get_rect()


def update_display():
    display_surface.fill(BLACK)

    for item in HUD_ITEMS.values():
        display_surface.blit(item.surface, item.rect)

    HUD_ITEMS['burger_points_hud'].update_variable(burger_dog.burger_points)

    pygame.draw.line(display_surface, WHITE, (0, 100), (WINDOW_WIDTH, 100), 3)

    display_surface.blit(player_image, burger_dog.player_rect)
    display_surface.blit(burger_image, burger_dog.burger_rect)

    pygame.display.update()

    clock.tick(FPS)


def step(action):
    global player_image
    if action[0] == 1:
        player_image = player_image_left
    elif action[0] == 2:
        player_image = player_image_right

    if action[2]:
        HUD_ITEMS['boost_hud'].update_variable(burger_dog.boost_level)

    obs, reward, done, info = burger_dog.step(burger_dog.action_array_to_int(action))

    if info.get('Burger Miss', None):
        miss_sound.play()
        HUD_ITEMS['player_lives_hud'].update_variable(burger_dog.player_lives)
        HUD_ITEMS['boost_hud'].update_variable(burger_dog.boost_level)

    if info.get("Burger Eaten", None):
        bark_sound.play()

        HUD_ITEMS['score_hud'].update_variable(burger_dog.score)
        HUD_ITEMS['burger_eaten_hud'].update_variable(burger_dog.burger_eaten)
        HUD_ITEMS['boost_hud'].update_variable(burger_dog.boost_level)

    return obs, reward, done, info


def game_over():
    game_over_text = font.render("Final Score: " + str(burger_dog.score), True, ORANGE)
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    continue_text = font.render("Press any key to play again", True, ORANGE)
    continue_rect = continue_text.get_rect()
    continue_rect.centerx = WINDOW_WIDTH // 2
    continue_rect.y = game_over_rect.bottom + 10

    bg_music.stop()

    is_paused = True
    while is_paused:

        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                is_paused = False
                burger_dog.reset()

                update_HUD()

                bg_music.play(-1)

        pygame.display.update()


def update_HUD():
    HUD_ITEMS['boost_hud'].update_variable(burger_dog.boost_level)
    HUD_ITEMS['player_lives_hud'].update_variable(burger_dog.player_lives)
    HUD_ITEMS['score_hud'].update_variable(burger_dog.score)
    HUD_ITEMS['burger_eaten_hud'].update_variable(burger_dog.burger_eaten)
    HUD_ITEMS['burger_points_hud'].update_variable(burger_dog.burger_points)


if __name__ == "__main__":
    bg_music.play(-1)
    import human
