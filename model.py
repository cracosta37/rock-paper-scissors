import numpy as np
from random import choice

def score_model(model, opponent_history=[]): 
    """ Returns a score for a model's performance based on opponent history """

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

def vectorize(choice1, choice2):
    """ Returns a vector describing the difference between one choice and another """

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    worse_response = {'S': 'P', 'P': 'R', 'R': 'S'}

    if choice1 == ideal_response[choice2]:
        return 1
    elif choice1 == worse_response[choice2]:
        return -1
    else:
        return 0

def model0(opponent_history=[]):
    """
    Chooses the guess that would lose to or beat the player's 
    last guess. Based on whether a player is changing their answers 
    or not in the past three rounds.
    """

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    worse_response = {'S': 'P', 'P': 'R', 'R': 'S'}
    
    if len(opponent_history) > 2:      
        repeats = sum(opponent_history[-i] == opponent_history[-i-1] for i in range(1, 3)) 
        if repeats > 1:
            guess = ideal_response[opponent_history[-1]]
        else:
            guess = worse_response[opponent_history[-1]]
    elif len(opponent_history) > 0:
        guess = worse_response[opponent_history[-1]]
    else:
        guess = choice(['R', 'P', 'S'])
    return guess

def model1(opponent_history=[]):
    """
    Vector-based choice based on past three rounds. For simple patterns, such as 
    S-R-P-S-R-P..., P-R-P-R..., or P-P-P...
    """

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    worse_response = {'S': 'P', 'P': 'R', 'R': 'S'}

    if len(opponent_history) > 1:        
        if len(opponent_history) > 2:
            vector1 = vectorize(opponent_history[-1], opponent_history[-2]) 
            vector2 = vectorize(opponent_history[-2], opponent_history[-3])            
            if vector1 == vector2:
                vector = vector1
            else:
                vector = vector2
        else:
            vector = vectorize(opponent_history[-1], opponent_history[-2])
        
        if vector == 1:
            guess = ideal_response[ideal_response[opponent_history[-1]]]
        elif vector == -1:
            guess = ideal_response[worse_response[opponent_history[-1]]]
        elif vector == 0:
            guess = ideal_response[opponent_history[-1]]
    else:
        guess = choice(['R', 'P', 'S'])
    return guess

def model2(opponent_history=[]):
    return

def model3(opponent_history=[]):
    return

def model4(opponent_history=[]):
    return