






global_possible_directions = [ [0,1], [1,0], [0,-1], [-1,0] ]

# global_possible_directions = [ [0,1] ]


one_dimensional_possible_directions = [1, -1]

############################################
## Weights (probabilities) for directions ##
############################################

global_weights = [0.25, 0.25, 0.25, 0.25]




# global_weights = [0.1,  
#                   0.4,
#                   0.1,
#                   0.4
#                     ]




# For running the experiments
list_of_parameteres_dict = [
    {'alpha':0.8 , 'mu': 0.4, 'delta': 0.0001, 'epsilon': 0.9}, # baseline

    {'alpha':1   , 'mu': 0.4, 'delta': 0.0001, 'epsilon': 0.9}, # change alpha

    {'alpha':0.8 , 'mu': 0.2, 'delta': 0.0001, 'epsilon': 0.9}, # change mu
    {'alpha':0.8 , 'mu': 0.6, 'delta': 0.0001, 'epsilon': 0.9},

    {'alpha':0.8 , 'mu': 0.4, 'delta': 0.01  , 'epsilon': 0.9}, # change density
    {'alpha':0.8 , 'mu': 0.4, 'delta': 0.001 , 'epsilon': 0.9},

    {'alpha':0.8 , 'mu': 0.4, 'delta': 0.0001, 'epsilon': 0.5}, # change epsilon

]
 
