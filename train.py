from operator import mod
from stable_baselines3 import PPO as algo
import game_interface

train_env = game_interface.burger_dog
path = f"trained_models\\{algo.__name__}"
try:
    model = algo.load(path, env=train_env)
except:
    model = algo("MlpPolicy", train_env)
    print("Akash")

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
            actions[0]-=1
            actions[1]-=1
            obs, reward, done, info = game_interface.step(actions)

            episode_reward += reward
            game_interface.update_display()

            for event in game_interface.pygame.event.get():
                pass
            
        print(f"{i} {j} Score = {episode_reward}")
    





