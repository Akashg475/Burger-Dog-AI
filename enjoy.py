import os
import sys

import game_interface
from sb3_contrib import TRPO as ALGO

enjoy_env = game_interface.burger_dog
trained_model =ALGO.load(os.path.join(os.path.dirname(__file__), "final_trained_models", ALGO.__name__),enjoy_env)

while True:
    done = False
    obs = enjoy_env.reset()
    game_interface.update_HUD()
    while not done:

        actions, _ = trained_model.predict(obs, deterministic=True)
        obs, reward, done, info = game_interface.step(enjoy_env.action_int_to_array(actions))
        game_interface.update_display()

        for event in game_interface.pygame.event.get():
            if event.type == game_interface.pygame.QUIT:
                sys.exit(0)

    game_interface.game_over()