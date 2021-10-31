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
env = gym.make("gym_friv:onionBoyEnv-v0") 
#env = gym.make("gym_slitherin:chickenGoEnv-v0")

print("FIRST WILL CHECK IF ENV IS OK")
check_env(env)

#policy_kwargs = dict(activation_fn=th.nn.ReLU,
#                     net_arch=[dict(pi=[32, 32], vf=[32, 32])])
print("NOW WILL TRAIN THE MODEL")
print(env.action_space)



model = DQN(
    'CnnPolicy', env, verbose=1,seed=185,
    buffer_size=100000,optimize_memory_usage=True,learning_starts=4000,
    create_eval_env=True) #try n_steps=6144

model.learn(
    total_timesteps= 2000000,eval_env=env,
    eval_freq=100000,n_eval_episodes=5
    ) 
print("learning done") 
model.save("DQN-ONION")
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
