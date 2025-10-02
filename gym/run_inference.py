import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
import time

env = gym.make("LunarLander-v3", render_mode="human")
model = PPO.load("ppo_lunarlander")
episodes = 20
for episode in range(1, episodes +1):
    obs, info = env.reset()
    done = False
    score = 0
    while not done:
        env.render()
        action, _states = model.predict(obs)
        obs, reward, done, _, _ = env.step(action)
        score += reward
    print(f"Episode:{episode} Score:{score}")
    time.sleep(1)
env.close()
