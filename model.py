import numpy as np
from random import randint

def score_model(model, opponent_history=[]): 
    if len(opponent_history) < 2:
        return float(-1.0)
    
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    worse_response = {'S': 'P', 'P': 'R', 'R': 'S'}

    model_record = []
    w_max = 0
    for i in range(1, len(opponent_history)):
        if model(opponent_history[:i]) == ideal_response[opponent_history[i]]:
            model_record.append(i**2)
        elif model(opponent_history[:i]) == worse_response[opponent_history[i]]:
            model_record.append(-i**2)
        w_max += i**2

        if w_max == 0:
            return float(0.0)
   
    return np.sum(model_record) / w_max

def model0(opponent_history=[]):
    return

def model1(opponent_history=[]):
    return

def model2(opponent_history=[]):
    return

def model3(opponent_history=[]):
    return

def model4(opponent_history=[]):
    return