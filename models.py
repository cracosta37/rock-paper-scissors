import pandas as pd
import numpy as np
from random import choice
from joblib import load

import constants as c

def last_score_model(prev_guess, prev_play, l_opponent_history): 
    """
    Returns the last term of the summation used to calculate the score
    for a model's performance based on the opponent's history.
    """

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    worse_response = {'S': 'P', 'P': 'R', 'R': 'S'}

    if prev_guess == ideal_response[prev_play]:
        return (l_opponent_history-1)**2   
    if prev_guess == worse_response[prev_play]:
        return -(l_opponent_history-1)**2
    return 0

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

def model0(opponent_history, player_history):
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

def model1(opponent_history, player_history):
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

def model2(opponent_history, player_history):
    """
    Chooses the choice that would beat the player's most frequent recent 
    choice. Based on repeated choices
    """

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    if len(opponent_history) > 4:
        recent_history = pd.Series(opponent_history[-5:])
        most_freq = recent_history.value_counts().index[0]
        guess = ideal_response[most_freq]
    elif len(opponent_history) > 0:
        history_series = pd.Series(opponent_history)
        most_freq = history_series.value_counts().index[0]
        guess = ideal_response[most_freq]
    else: 
        guess = choice(['R', 'P', 'S'])
    return guess

def model3(opponent_history, player_history):
    """
    Chooses the choice that would beat the player's least frequent recent 
    choice. Based on repeated choices
    """

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    if len(opponent_history) > 4:
        recent_history = pd.Series(opponent_history[-5:])
        least_freq = recent_history.value_counts().index[-1]
        guess = ideal_response[least_freq]
    elif len(opponent_history) > 0:
        history_series = pd.Series(opponent_history)
        least_freq = history_series.value_counts().index[-1]
        guess = ideal_response[least_freq]
    else:
        guess = choice(['R', 'P', 'S'])
    return guess

def model4(opponent_history, player_history):
    """
    Chooses the choice that would beat the predicted the next player's choice using a NN model. 
    """
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    rps_nums = ['R', 'P', 'S']
    
    if not hasattr(model4, "nn_model"):
        model4.nn_model = load('models/nn_model.pkl')

    if len(opponent_history) < c.NUMBER_OF_INPUTS:
        guess = choice(['R', 'P', 'S'])
        return guess
    
    recent_opponent_history = np.array(pd.Series(opponent_history[-c.NUMBER_OF_INPUTS:]).map({'R': 0, 'P': 1, 'S': 2}))
    recent_player_history = np.array(pd.Series(player_history[-c.NUMBER_OF_INPUTS:]).map({'R': 0, 'P': 1, 'S': 2}))

    recent_history = np.hstack([recent_opponent_history, recent_player_history])
    recent_history = recent_history.reshape(1, -1)

    prediction = model4.nn_model.predict(recent_history, verbose=0)
    prediction = rps_nums[int(np.argmax(prediction[0]))]

    guess = ideal_response[prediction]
    return guess