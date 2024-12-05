# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
from models import score_model, model0, model1, model2, model3, model4

def player(prev_play, opponent_history=[]):

    if prev_play == "":
        prev_play = "R"  # Default move for the first play
    
    opponent_history.append(prev_play)

    # List of model functions
    models = [model0, model1, model2, model3, model4]

    # Compute scores for each model
    scores = [score_model(model, opponent_history) for model in models]
    
    # Find the model with the highest score
    max_score_index = scores.index(max(scores))

    # Use the corresponding model to make a guess
    guess = models[max_score_index](opponent_history)
    
    return guess