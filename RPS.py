# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
from models import last_score_model, model0, model1, model2, model3, model4

import constants as c

def player(prev_play):

    # Resetting values at the start of the game
    if not hasattr(player, "opponent_history") or prev_play == '':
        prev_play = c.DEFAULT_PREV_PLAY
        player.prev_guess = c.DEFAULT_PREV_GUESS
        player.opponent_history = []
        player.player_history = []
        player.scores = c.DEFAULT_SCORES.copy()
        player.prev_guesses = c.DEFAULT_GUESSES.copy()

    # Updating of opponent and player histories
    player.opponent_history.append(prev_play)
    player.player_history.append(player.prev_guess)
    l_opponent_history = len(player.opponent_history)

     # Creating a list of model functions
    models = [model0, model1, model2, model3, model4]

    # Computing scores for each model
    last_scores = [last_score_model(model_prev_guess, prev_play, l_opponent_history) for model_prev_guess in player.prev_guesses]
    player.scores = [score + last_score for score, last_score in zip(player.scores, last_scores)]
   
    # Finding the model with the highest score
    max_score_index = player.scores.index(max(player.scores))

    # Calculating the model's guesses and updating prev_guesses
    player.prev_guesses = [models[i](player.opponent_history, player.player_history) for i in range(5)]

    # Chosing the model with higher score for the guess
    guess = player.prev_guesses[max_score_index]

    # Updating prev_guess
    player.prev_guess = guess

    return guess