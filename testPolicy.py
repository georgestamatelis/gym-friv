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
#env = gym.make("gym_slitherin:agentPlatformer-v0") 
env = gym.make("gym_slitherin:traffic-v0")

print("fIRST WILL CHECK IF ENV IS OK")
check_env(env)

#policy_kwargs = dict(activation_fn=th.nn.ReLU,
#                     net_arch=[dict(pi=[32, 32], vf=[32, 32])])
print("NOW WILL TRAIN THE MODEL")
print(env.action_space)
#1207627  does well , also 1611500
model = DQN('CnnPolicy',env,verbose=1,buffer_size=100000)#,optimize_memory_usage=True,learning_starts=1000)#
#model = PPO('CnnPolicy', env, verbose=1) #try n_steps=6144
model.learn(total_timesteps=  1207627) 
print("learning done")
#model.save("DQN-ZOMBIE")
model.save("DQN-TRAFFIC-EASY")
#print("model Saved")
obs = env.reset()
for i in range(100000):
    action, _states = model.predict(obs.copy(),deterministic=True)
    obs, rewards, dones, info = env.step(action)
    print("action=",action,"reward=",rewards)
    env.render()
    if dones:
        print("why?")
        break
