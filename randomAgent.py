import gym
from gym.core import ActionWrapper
import matplotlib.pyplot as plt


#env = gym.make("gym_slitherin:slitherin-v2")
env = gym.make("gym_slitherin:hill-climber-v0")



obs = env.reset()
print(obs.shape)
while True:
    #action=env.action_space.sample()
    action=2
    obs, reward, done, info=env.step(action)
    env.render()
    if done==True:
        obs=env.reset()


env.close()
