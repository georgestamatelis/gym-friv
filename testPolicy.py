import gym
import torch as th

from stable_baselines3 import A2C #remember to try PPO
from stable_baselines3 import DQN #allso try DQN
from stable_baselines3 import PPO #allso try 
from stable_baselines3 import TD3
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.noise import NormalActionNoise
import numpy as np

env = gym.make("gym_slitherin:slitherin-v2")
print("fIRST WILL CHECK IF ENV IS OK")
check_env(env)

#policy_kwargs = dict(activation_fn=th.nn.ReLU,
#                     net_arch=[dict(pi=[32, 32], vf=[32, 32])])
print("NOW WILL TRAIN THE MODEL")
#model = PPO('CnnPolicy',env,verbose=1)
#model.learn(total_timesteps=10000,log_interval=1000)
#print("NOW WILL TRAIN THE MODEL")
# Instantiate the agent
#print("N ACTIONS =",env.action_space.shape)
model = DQN('CnnPolicy',env,verbose=1,buffer_size=10000,optimize_memory_usage=True,learning_starts=1000)
#model = PPO('CnnPolicy', env, verbose=1) #try 2500 time steps
model.learn(total_timesteps=10000)
#model.learn(n_eval_episodes=10)

obs = env.reset()
for i in range(10000):
    action, _states = model.predict(obs,deterministic=True)
    obs, rewards, dones, info = env.step(action)
    print("action=",action,"reward=",rewards)
    env.render()
    if dones:
        break
