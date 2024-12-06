# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
from models import last_score_model, model0, model1, model2, model3, model4

def player(prev_play, opponent_history=[], scores=[0, 0, 0, 0, 0], prev_guesses=['R', 'R', 'R', 'R', 'R']):

    if prev_play == '':
        prev_play = 'R' # Default move for the first play
    
    # Updating of opponent history
    opponent_history.append(prev_play)
    l_opponent_history = len(opponent_history)

     # Creating a list of model functions
    models = [model0, model1, model2, model3, model4]

    # Computing scores for each model
    last_scores = [last_score_model(prev_guess, prev_play, l_opponent_history) for prev_guess in prev_guesses]
    scores = [score + last_score for score, last_score in zip(scores, last_scores)]

    # Normalizing scores to avoid overflow and emphasize long histories
    normalization_factor = sum(i**2 for i in range(1, l_opponent_history))
    if normalization_factor > 0:
        scores = [score / normalization_factor for score in scores]
  
    # Finding the model with the highest score
    max_score_index = scores.index(max(scores))

    # Calculating the model's guesses and updating prev_guesses
    prev_guesses = [models[i](opponent_history) for i in range(5)]

    # Chosing the model with higher score for the guess
    guess = prev_guesses[max_score_index]

    return guess