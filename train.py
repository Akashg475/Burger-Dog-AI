Possible_Agents = ["A2C", "DQN", "PPO", "ARS", "MaskablePPO", "QRDQN", "TRPO"]
AGENT_NAME = "A2C"


import os
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

train_env = game_interface.burger_dog
path = os.path.join(os.path.dirname(__file__), "trained_models", ALGO.__name__)
try:
    model = ALGO.load(path, env=train_env)
except FileNotFoundError:
    model = ALGO("MlpPolicy", train_env)

for i in range(100):
    # Learn
    model.learn(1e5)

    # Save 
    model.save(path)

    # Evaluate Model 5 times
    for j in range(5):
        done = False
        obs = train_env.reset()
        episode_reward = 0
        game_interface.update_HUD()
        while not done:

            actions, _ = model.predict(obs, deterministic=True)
            obs, reward, done, info = game_interface.step(train_env.action_int_to_array(actions))
            episode_reward += reward
            game_interface.update_display()

            for event in game_interface.pygame.event.get():
                pass

        print(f"Evaluation No. {i} - Episode No.{j} - Score = {episode_reward}")
    print()
