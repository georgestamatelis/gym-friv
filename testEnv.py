import gym
import matplotlib.pyplot as plt
from stable_baselines3.common.env_checker import check_env
import cv2
#env = gym.make("gym_slitherin:zombieOnslaught-v0") 
env = gym.make("gym_slitherin:onionBoyEnv-v0")
#env = gym.make("gym_slitherin:agentPlatformer-v3")

check_env(env)
obs = env.reset()
#obs = cv2.cvtColor(obs,cv2.COLOR_BGR2GRAY)
env.render()
#screen = env.render(mode = "rgb_array")
print("obs.shape=",obs.shape)
plt.imshow(obs)
plt.show()