def score_model(prev_play, opponent_history=[])
    
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    bad_response = {'S': 'P', 'P': 'R', 'R': 'S'}

    return