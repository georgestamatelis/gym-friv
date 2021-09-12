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
env = gym.make("gym_slitherin:spinSoccer-v3") 
#env = gym.make("gym_slitherin:chickenGoEnv-v0")

print("fIRST WILL CHECK IF ENV IS OK")
check_env(env)

#policy_kwargs = dict(activation_fn=th.nn.ReLU,
#                     net_arch=[dict(pi=[32, 32], vf=[32, 32])])
print("NOW WILL TRAIN THE MODEL")
print(env.action_space)
#0.0001 seems good for spin soccer 0

model = PPO(
    'CnnPolicy',env,verbose=1,
    create_eval_env=True,clip_range=0.2, seed=185
   
    )
    #,optimize_memory_usage=True,learning_starts=1000)#
#model = PPO('CnnPolicy', env, verbose=1) #try n_steps=6144
#try 129025 
model.learn(
    total_timesteps=  50000,eval_env=env,
    eval_freq=10000,n_eval_episodes=5,
    ) 
print("learning done") 
model.save("PPO-SOCCER-3")
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
