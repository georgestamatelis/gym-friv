from gym.envs.registration import register 
register(id='chickenGoEnv-v0',entry_point='gym_friv.envs:chickenGoEnvSlow',)
register(id='chickenGoEnv-v1',entry_point='gym_friv.envs:chickenGoEnv',)

register(id='zombieOnslaught-v0',entry_point='gym_friv.envs:zombieOnslaughtEasyEnv',)
register(id='zombieOnslaught-v1',entry_point='gym_friv.envs:zombieOnslaughtHardEnv',)

register(id='hill-climber-v0',entry_point='gym_friv.envs:Hill_Climber_Env',)

register(id='CarParking-v0',entry_point='gym_friv.envs:CarParking1',)
register(id='CarParking-v2',entry_point='gym_friv.envs:CarParking2',)

register(id='agentPlatformer-v0',entry_point='gym_friv.envs:agentPlatformerEnv',)
register(id='agentPlatformer-v2',entry_point='gym_friv.envs:agentPlatformerEnv2',)
register(id='agentPlatformer-v3',entry_point='gym_friv.envs:agentPlatformerEnv3',)

register(id='onionBoyEnv-v0',entry_point='gym_friv.envs:onionBoyEnv',)

register(id='eyeCopter-v0',entry_point='gym_friv.envs:eyeCopterEnv1',)

register(id='traffic-v0',entry_point='gym_friv.envs:iLoveTrafficEnv0',)
register(id='traffic-v1',entry_point='gym_friv.envs:iLoveTrafficEnvLVL1',)
register(id='traffic-v2',entry_point='gym_friv.envs:iLoveTrafficEnv2',)
register(id='traffic-v3',entry_point='gym_friv.envs:iLoveTrafficEnv3',)
register(id='traffic-v4',entry_point='gym_friv.envs:iLoveTrafficEnv4',)





register(id='spinSoccer-v0',entry_point='gym_friv.envs:spinSoccerEnv',)
register(id='spinSoccer-v1',entry_point='gym_friv.envs:spinSoccerEnv1',)
register(id='spinSoccer-v2',entry_point='gym_friv.envs:spinSoccerEnv2',)
register(id='spinSoccer-v3',entry_point='gym_friv.envs:spinSoccerEnv3',)


register(id='pumpkin-v1',entry_point='gym_friv.envs:bossLevelPumpkin1',)
register(id='pumpkin-v2',entry_point='gym_friv.envs:bossLevelPumpkin2',)
register(id='pumpkin-v3',entry_point='gym_friv.envs:bossLevelPumpkin3',)
