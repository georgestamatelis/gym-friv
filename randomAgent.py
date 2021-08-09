import gym
from gym.core import ActionWrapper
import matplotlib.pyplot as plt


#env = gym.make("gym_slitherin:slitherin-v2")
env = gym.make("gym_slitherin:CarParking-v0")


rendered=env.render(mode="rgb_array")
print("rendered shape=",rendered.shape)
obs = env.reset()
print(obs.shape)
while True:
    action=env.action_space.sample()
    #action=2
    obs, reward, done, info=env.step(action)
    env.render()
    print("Reward=",reward,"Action=",action)
    if done==True:
        obs=env.reset()


env.close()
