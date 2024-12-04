# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
from models import score_model, model0, model1, model2, model3, model4

def player(prev_play, opponent_history=[]):
    if prev_play == "":
        prev_play = "R"
    
    opponent_history.append(prev_play)

    scores = []

    for i in range(5):
        score = score_model(f'model{i}', opponent_history)
        scores.append(score)
    
    max_score_model = int(scores.index(max(scores)))

    guess = f'model{max_score_model}'(opponent_history)

    return guess
