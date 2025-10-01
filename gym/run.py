import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
import time


env = gym.make("LunarLander-v3", render_mode="human")

model = PPO("MlpPolicy", env, verbose = 1)
model.learn(total_timesteps = 100000)

mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
print(f"Mean reward: {mean_reward} +/- {std_reward}")
model.save("ppo_lunarlander")

model = PPO.load("ppo_lunarlander")
episodes = 5
for episode in range(1, episodes +1):
    obs = env.reset()
    done = False
    while not done:
        env.render()
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        score += reward
    print(f"Episode:{episode} Score:{score}")
    time.sleep(1)
env.close()
