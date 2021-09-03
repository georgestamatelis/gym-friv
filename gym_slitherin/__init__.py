from gym.envs.registration import register 
register(id='chickenGoEnv-v0',entry_point='gym_slitherin.envs:chickenGoEnv',)

register(id='zombieOnslaught-v0',entry_point='gym_slitherin.envs:zombieOnslaughtEasyEnv',)
register(id='zombieOnslaught-v1',entry_point='gym_slitherin.envs:zombieOnslaughtHardEnv',)

register(id='hill-climber-v0',entry_point='gym_slitherin.envs:Hill_Climber_Env',)

register(id='CarParking-v0',entry_point='gym_slitherin.envs:CarParking',)
register(id='CarParking-v3',entry_point='gym_slitherin.envs:CarParking3',)
register(id='agentPlatformer-v0',entry_point='gym_slitherin.envs:agentPlatformerEnv',)
register(id='agentPlatformer-v2',entry_point='gym_slitherin.envs:agentPlatformerEnv2',)
register(id='agentPlatformer-v3',entry_point='gym_slitherin.envs:agentPlatformerEnv3',)

register(id='onionBoyEnv-v0',entry_point='gym_slitherin.envs:onionBoyEnv',)
register(id='eyeCopter-v0',entry_point='gym_slitherin.envs:eyeCopterEnv1',)

register(id='traffic-v0',entry_point='gym_slitherin.envs:iLoveTrafficEnv1',)
