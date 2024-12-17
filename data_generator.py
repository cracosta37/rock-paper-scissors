import pandas as pd

from RPS_game import play, mrugesh, abbey, quincy, kris
from RPS import player

import constants as c

players = [mrugesh, abbey, quincy, kris]
record = pd.DataFrame(columns=['game_id', 'round', 'p1'])


for i in range(4):
    play(player, players[i], 1000)
    temp_df = pd.DataFrame({
        'game_id': i,                  
        'round': range(1000),          
        'p1': player.opponent_history          
    })
    record = pd.concat([record, temp_df], ignore_index=True)

record['p1'] = record['p1'].map({'R': 0, 'P': 1, 'S': 2})

record.to_csv('record.csv')
