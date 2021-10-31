from math import e
import gym
from gym.core import ActionWrapper
import matplotlib.pyplot as plt
from stable_baselines3.common.env_checker import check_env
import random


env = gym.make("gym_friv:chickenGoEnv-v1") 

check_env(env)
#rendered=env.render(mode="rgb_array")
#print("rendered shape=",rendered.shape)
obs = env.reset()
print(obs.shape)
totalRew=0
numEpisodes=0
action=env.action_space.sample()
print("sampled action =",action)
while numEpisodes<5:
  
    #action=2
    if random.random() >0.7:
        obs, reward, done, info=env.step(env.action_space.sample())
    else:
        obs, reward, done, info=env.step(action)
    totalRew+=reward
    env.render()
    #print("Reward=",reward,"Action=",action)
    if done==True:
        obs=env.reset()
        numEpisodes+=1
env.close()
print("mean reward =",totalRew/5)