from random import randint
from gym import Env, spaces
import numpy as np


class BurgerDogEnvironment(Env):

    def render(self, mode="human"):
        pass

    def __init__(self, game_width, game_height):

        self.GAME_WIDTH = game_width
        self.GAME_HEIGHT = game_height

        self.PLAYER_STARTING_LIVES = 3
        self.PLAYER_NORMAL_VELOCITY = 5
        self.PLAYER_BOOST_VELOCITY = 10
        self.STARTING_BOOST_LEVEL = 100
        self.STARTING_BURGER_VELOCITY = 3
        self.BURGER_ACCELARATION = 0.5
        self.BUFFER_DISTANCE = 100

        self.score = 0
        self.burger_points = 0
        self.burger_eaten = 0
        self.burger_rect = None

        self.player_lives = self.PLAYER_STARTING_LIVES
        self.player_velocity = self.PLAYER_NORMAL_VELOCITY
        self.player_rect = None

        self.boost_level = self.STARTING_BOOST_LEVEL
        self.burger_velocity = self.STARTING_BURGER_VELOCITY

        self.action_space = spaces.Discrete(18)

        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, -self.BUFFER_DISTANCE, 0]),
            high=np.array([self.GAME_WIDTH, self.GAME_HEIGHT, 100, self.GAME_WIDTH, self.GAME_HEIGHT, 20]))

    def reset_game_variables(self):
        self.player_rect.centerx = self.GAME_WIDTH // 2
        self.player_rect.bottom = self.GAME_HEIGHT - 10

        self.burger_rect.topleft = (
            randint(0, self.GAME_WIDTH - self.burger_rect.width), -self.BUFFER_DISTANCE)
        self.burger_velocity = self.STARTING_BURGER_VELOCITY

        self.boost_level = self.STARTING_BOOST_LEVEL
        self.burger_points = 0

    def get_observation(self):
        return np.array(
            [*self.player_rect.center, self.boost_level, *self.burger_rect.center, self.burger_velocity]).astype(
            np.float32)

    def reset(self):
        self.reset_game_variables()
        self.player_lives = self.PLAYER_STARTING_LIVES
        self.score = 0
        self.burger_eaten = 0

        return self.get_observation()

    def step(self, action: int):
        converted_action_space = self.action_int_to_array(action)
        # print(action, converted_action_space)
        info = {}
        reward = 0

        if converted_action_space[2] and self.boost_level > 0:
            self.player_velocity = self.PLAYER_BOOST_VELOCITY
            self.boost_level -= 1
        else:
            self.player_velocity = self.PLAYER_NORMAL_VELOCITY

        if converted_action_space[0] == 1:  # Move Left
            self.player_rect.left = max(
                0, self.player_rect.left - self.player_velocity)
        elif converted_action_space[0] == 2:  # Move Right
            self.player_rect.right = min(
                self.GAME_WIDTH, self.player_rect.right + self.player_velocity)

        if converted_action_space[1] == 1:  # Move up
            self.player_rect.top = max(
                100, self.player_rect.top - self.player_velocity)
        elif converted_action_space[1] == 2:  # Move Down
            self.player_rect.bottom = min(
                self.GAME_HEIGHT, self.player_rect.bottom + self.player_velocity)

        # Move the Burger
        self.burger_rect.y += self.burger_velocity
        self.burger_points = int((self.GAME_HEIGHT - self.burger_rect.y + 100) /
                                 10 * self.burger_velocity / self.STARTING_BURGER_VELOCITY)

        # If Player Missed Burger
        if self.burger_rect.y >= self.GAME_HEIGHT:
            self.player_lives -= 1
            info['Burger Miss'] = True
            reward -= 30
            self.reset_game_variables()

        # Check for Collision
        if self.player_rect.colliderect(self.burger_rect):
            self.score += self.burger_points
            reward += self.burger_points
            self.burger_eaten += 1

            info['Burger Eaten'] = True

            self.boost_level = min(self.boost_level + 25, 100)
            self.burger_rect.topleft = (
                randint(0, self.GAME_HEIGHT - self.burger_rect.width), -self.BUFFER_DISTANCE)

            self.burger_velocity += self.BURGER_ACCELARATION

        # Check for Game over
        if self.player_lives == 0:
            reward -= 50
            done = True

        else:
            done = False

        return self.get_observation(), reward, done, info

    def action_int_to_array(self, action):
        result = [0,0,0]
        result[0] = action//6
        result[1] = (action%6)//2
        result[2] = action%2
        return result

    def action_array_to_int(self, action_array):
        return action_array[0] * 6 + action_array[1] * 2 + action_array[2]

# if __name__ == "__main__":
#     from stable_baselines3.common.env_checker import check_env
#     import pygame
#     x = BurgerDogEnvironment(500,600)
#     x.player_rect = pygame.Rect(0, 0, 32, 32)
#     x.burger_rect = pygame.Rect(0, 0, 32, 32)
#     print(x.observation_space)
#     print(x.reset())
#     check_env(x)
