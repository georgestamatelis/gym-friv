import gym
from gym.core import ActionWrapper
import matplotlib.pyplot as plt
from stable_baselines3.common.env_checker import check_env


env = gym.make("gym_friv:pumpkin-v3") 

check_env(env)
#rendered=env.render(mode="rgb_array")
#print("rendered shape=",rendered.shape)
obs = env.reset()
print(obs.shape)
totalRew=0
numEpisodes=0
while numEpisodes<5:
    action=env.action_space.sample()
    #action=2
    obs, reward, done, info=env.step(action)
    totalRew+=reward
    env.render()
    #print("Reward=",reward,"Action=",action)
    if done==True:
        obs=env.reset()
        numEpisodes+=1
env.close()
print("mean reward =",totalRew/5)