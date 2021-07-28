from gym.envs.registration import register 
register(id='slitherin-v0',entry_point='gym_slitherin.envs:SlitherinEnv',) 
register(id='slitherin-v2',entry_point='gym_slitherin.envs:SlitherinEnv2',)
register(id='hill-climber-v0',entry_point='gym_slitherin.envs:Hill_Climber_Env',)