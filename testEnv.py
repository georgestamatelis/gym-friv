import gym
import matplotlib.pyplot as plt
from stable_baselines3.common.env_checker import check_env
import cv2
env = gym.make("gym_slitherin:spinSoccer-v1") 
#env = gym.make("gym_slitherin:onionBoyEnv-v0")
#env = gym.make("gym_slitherin:agentPlatformer-v3")

check_env(env)
#env.render()
obs = env.reset()
#env.render()
screen = env.render(mode = "rgb_array")
print("obs.shape=",obs.shape)
cv2.imshow("reset",obs)
cv2.imshow("test",screen)
cv2.waitKey(0)