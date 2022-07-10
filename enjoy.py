Possible_Agents = ["A2C", "DQN", "PPO", "ARS", "MaskablePPO", "QRDQN", "TRPO"]
AGENT_NAME = "A2C"

import os
import sys

import game_interface


if AGENT_NAME == "A2C":
    from stable_baselines3 import A2C as ALGO
elif AGENT_NAME == "DQN":
    from stable_baselines3 import DQN as ALGO
elif AGENT_NAME == "PPO":
    from stable_baselines3 import PPO as ALGO
elif AGENT_NAME == "ARS":
    from sb3_contrib import ARS as ALGO
elif AGENT_NAME == "MaskablePPO":
    from sb3_contrib import MaskablePPO as ALGO
elif AGENT_NAME =="QRDQN":
    from sb3_contrib import QRDQN as ALGO
elif AGENT_NAME == "TRPO":
    from sb3_contrib import TRPO as ALGO
else:
    raise ValueError("Agent Name not in Possible Agents")

enjoy_env = game_interface.burger_dog
trained_model =ALGO.load(os.path.join(os.path.dirname(__file__), "trained_models", ALGO.__name__),enjoy_env)

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