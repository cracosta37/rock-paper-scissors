import pandas as pd

from RPS_game import play, mrugesh, abbey, quincy, kris
from RPS import player

import constants as c

players = [mrugesh, abbey, quincy, kris]
record = pd.DataFrame(columns=['game_id', 'round', 'p1', 'p2'])


for i in range(4):
    play(player, players[i], c.NUMBER_OF_GAMES)
    temp_df = pd.DataFrame({
        'game_id': i,                  
        'round': range(c.NUMBER_OF_GAMES),          
        'p1': player.opponent_history,
        'p2': player.player_history         
    })
    record = pd.concat([record, temp_df], ignore_index=True)

record['p1'] = record['p1'].map({'R': 0, 'P': 1, 'S': 2})
record['p2'] = record['p2'].map({'R': 0, 'P': 1, 'S': 2})

record.to_csv('record.csv')