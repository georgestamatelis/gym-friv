import gym
import matplotlib.pyplot as plt


env = gym.make("gym_slitherin:slitherin-v2")



obs = env.reset()
while True:
    action=env.action_space.sample()
    obs, reward, done, info=env.step(action)
    env.render()
    if done==True:
        obs=env.reset()
env.close()
