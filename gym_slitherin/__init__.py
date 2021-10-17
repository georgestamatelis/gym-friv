from gym.envs.registration import register 
register(id='chickenGoEnv-v0',entry_point='gym_slitherin.envs:chickenGoEnvSlow',)
register(id='chickenGoEnv-v1',entry_point='gym_slitherin.envs:chickenGoEnv',)

register(id='zombieOnslaught-v0',entry_point='gym_slitherin.envs:zombieOnslaughtEasyEnv',)
register(id='zombieOnslaught-v1',entry_point='gym_slitherin.envs:zombieOnslaughtHardEnv',)

register(id='hill-climber-v0',entry_point='gym_slitherin.envs:Hill_Climber_Env',)

register(id='CarParking-v0',entry_point='gym_slitherin.envs:CarParking1',)
register(id='CarParking-v3',entry_point='gym_slitherin.envs:CarParking3',)

register(id='agentPlatformer-v0',entry_point='gym_slitherin.envs:agentPlatformerEnv',)
register(id='agentPlatformer-v2',entry_point='gym_slitherin.envs:agentPlatformerEnv2',)
register(id='agentPlatformer-v3',entry_point='gym_slitherin.envs:agentPlatformerEnv3',)

register(id='onionBoyEnv-v0',entry_point='gym_slitherin.envs:onionBoyEnv',)

register(id='eyeCopter-v0',entry_point='gym_slitherin.envs:eyeCopterEnv1',)

register(id='traffic-v0',entry_point='gym_slitherin.envs:iLoveTrafficEnv0',)
register(id='traffic-v1',entry_point='gym_slitherin.envs:iLoveTrafficEnvLVL1',)
register(id='traffic-v2',entry_point='gym_slitherin.envs:iLoveTrafficEnv2',)
register(id='traffic-v3',entry_point='gym_slitherin.envs:iLoveTrafficEnv3',)
register(id='traffic-v4',entry_point='gym_slitherin.envs:iLoveTrafficEnv4',)





register(id='spinSoccer-v0',entry_point='gym_slitherin.envs:spinSoccerEnv',)
register(id='spinSoccer-v1',entry_point='gym_slitherin.envs:spinSoccerEnv1',)
register(id='spinSoccer-v2',entry_point='gym_slitherin.envs:spinSoccerEnv2',)
register(id='spinSoccer-v3',entry_point='gym_slitherin.envs:spinSoccerEnv3',)
