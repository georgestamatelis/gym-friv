from gym.envs.registration import register 
register(id='slitherin-v0',entry_point='gym_slitherin.envs:SlitherinEnv',) 
register(id='zombieOnslaught-v0',entry_point='gym_slitherin.envs:zombieOnslaught',)
register(id='hill-climber-v0',entry_point='gym_slitherin.envs:Hill_Climber_Env',)
register(id='CarParking-v0',entry_point='gym_slitherin.envs:CarParking',)
register(id='CarParking-v3',entry_point='gym_slitherin.envs:CarParking3',)