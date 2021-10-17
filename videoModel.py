import gym
import torch as th

from stable_baselines3 import A2C #remember to try PPO
from stable_baselines3 import DQN #allso try DQN
from stable_baselines3 import PPO #allso try 
from stable_baselines3 import TD3
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.noise import NormalActionNoise
import numpy as np

#env = gym.make("gym_slitherin:onionBoyEnv-v0") 
env = gym.make("gym_slitherin:traffic-v0") 

model=PPO.load("DQN-TRAFFIC-EASY")

obs = env.reset()
for i in range(100000):
    action, _states = model.predict(obs.copy(),deterministic=True)
    obs, rewards, dones, info = env.step(action)
    print("action=",action,"reward=",rewards)
    env.render()
    if dones:
        obs=env.reset()
