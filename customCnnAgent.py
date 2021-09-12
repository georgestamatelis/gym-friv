import gym
import torch as th
import torch.nn as nn

from stable_baselines3 import PPO
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

from stable_baselines3.common.env_checker import check_env

class CustomCNN(BaseFeaturesExtractor):
    """
    :param observation_space: (gym.Space)
    :param features_dim: (int) Number of features extracted.
        This corresponds to the number of unit for the last layer.
    """

    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 256):
        super(CustomCNN, self).__init__(observation_space, features_dim)
        # We assume CxHxW images (channels first)
        # Re-ordering will be done by pre-preprocessing or wrapper
        n_input_channels = observation_space.shape[0]
        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 32, kernel_size=8, stride=4, padding=0),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2, padding=0),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute shape by doing one forward pass
        with th.no_grad():
            n_flatten = self.cnn(
                th.as_tensor(observation_space.sample()[None]).float()
            ).shape[1]

        self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU())

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.linear(self.cnn(observations))

policy_kwargs = dict(
    features_extractor_class=CustomCNN,
    features_extractor_kwargs=dict(features_dim=128),
)


env = gym.make("gym_slitherin:spinSoccer-v2") 
check_env(env)


model = PPO(
    "CnnPolicy",env,verbose=1,
    create_eval_env=True,clip_range=0, 
    policy_kwargs=policy_kwargs)
model.learn(
    total_timesteps=  500000,eval_env=env,
    eval_freq=10000,n_eval_episodes=5
)
print("learning done") 
model.save("PPO-SOCCER-1-CUSTOMNET")
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