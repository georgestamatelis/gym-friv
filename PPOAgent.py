import gym
import torch as th

from stable_baselines3 import A2C 
from stable_baselines3 import DQN
from stable_baselines3 import PPO
from stable_baselines3 import TD3
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.noise import NormalActionNoise
import numpy as np

#env = gym.make("gym_slitherin:onionBoyEnv-v0") 
#env = gym.make("gym_slitherin:-v2") 
env = gym.make("gym_friv:pumpkin-v3")

print("FIRST WILL CHECK IF ENV IS OK")
check_env(env)

#policy_kwargs = dict(activation_fn=th.nn.ReLU,
#                     net_arch=[dict(pi=[32, 32], vf=[32, 32])])
print("NOW WILL TRAIN THE MODEL")
print(env.action_space)

model = PPO(
    'CnnPolicy',env,verbose=1,
    create_eval_env=True,clip_range=0.2,
    seed=185
   
    )

#model = A2C(
#    'CnnPolicy', env, verbose=1,seed=185,
#    create_eval_env=True) 

#378880
model.learn(
    total_timesteps= 2000000,eval_env=env,
    eval_freq=25000,n_eval_episodes=5
    ) 
print("learning done") 
model.save("PPO-PUMPKIN-3")
#print("model Saved")
obs = env.reset()
for i in range(100000):
    action, _states = model.predict(obs.copy(),deterministic=True)
    obs, rewards, dones, info = env.step(action)
    print("action=",action,"reward=",rewards)
    env.render()
    if dones:
        print("done")
        break
