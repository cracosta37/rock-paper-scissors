# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
from models import last_score_model, model0, model1, model2, model3, model4

import constants as c

def player(prev_play):

    # Resetting values at the start of the game
    if not hasattr(player, "opponent_history") or prev_play == '':
        prev_play = c.DEFAULT_PREV_PLAY
        player.opponent_history = []
        player.scores = c.DEFAULT_SCORES.copy()
        player.prev_guesses = c.DEFAULT_GUESSES.copy()

    # Updating of opponent history
    player.opponent_history.append(prev_play)
    l_opponent_history = len(player.opponent_history)

     # Creating a list of model functions
    models = [model0, model1, model2, model3, model4]

    # Computing scores for each model
    last_scores = [last_score_model(prev_guess, prev_play, l_opponent_history) for prev_guess in player.prev_guesses]
    player.scores = [score + last_score for score, last_score in zip(player.scores, last_scores)]

    # Normalizing scores to avoid overflow and emphasize long histories
    normalization_factor = sum(i**2 for i in range(l_opponent_history)) or 1
    normalized_scores = [score / normalization_factor for score in player.scores]
   
    # Finding the model with the highest score
    max_score_index = normalized_scores.index(max(normalized_scores))

    # Calculating the model's guesses and updating prev_guesses
    player.prev_guesses = [models[i](player.opponent_history) for i in range(5)]

    # Chosing the model with higher score for the guess
    guess = player.prev_guesses[max_score_index]

    return guess