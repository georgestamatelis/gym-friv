import gym
import matplotlib.pyplot as plt
from stable_baselines3.common.env_checker import check_env

#env = gym.make("gym_slitherin:slitherin-v0") 
env = gym.make("gym_slitherin:CarParking-v0")
#env = gym.make("MountainCar-v0")

check_env(env)
env.render()
obs = env.reset()
screen = env.render(mode = "rgb_array")
plt.imshow(screen)
plt.show()