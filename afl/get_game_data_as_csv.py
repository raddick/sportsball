import os
import io
import pandas
#import re
import json
from pprint import pprint
import numpy as np
afldir = '/Users/raddick/Documents/GitHub/sportsball/afl/'
os.chdir(afldir)
games_df = pandas.read_csv(afldir+'games_parsed.csv', encoding='utf-8', index_col='Unnamed: 0')
games_df = games_df.assign(round_number = np.nan)
games_df.loc[games_df['round'] == 'Qualifying Final', 'round_number'] = 31
games_df.loc[games_df['round'] == 'Elimination Final', 'round_number'] = 32
games_df.loc[games_df['round'] == 'Semi Final', 'round_number'] = 40
games_df.loc[games_df['round'] == 'Preliminary Final', 'round_number'] = 50
games_df.loc[games_df['round'] == 'Grand Final', 'round_number'] = 60
games_df.loc[games_df['round_number'].isnull(), 'round_number'] = games_df['round'][games_df['round_number'].isnull()].apply(lambda x: int(x))
games_df['round_number'] = pandas.to_numeric(games_df['round_number'], downcast='integer', errors='coerce')

with io.open(afldir+'player_stats_afltables/player_game_stats_12k.json', encoding='utf-8') as f:
    alldata = json.load(f)
df = pandas.DataFrame()
##player_game_df = pandas.DataFrame(data=None, columns=['playerID'])
##print(player_game_df)
game_stats_df = pandas.DataFrame()
for this_player in alldata:
    for this_playerID, his_data in this_player.items():
        print('Parsing data for {0:}...'.format(this_playerID))
        for this_year_data in his_data:
            for this_year, this_year_data_list in this_year_data.items():
#                print(this_year)
                for thisonegame in this_year_data_list:
                    for this_round, thisgamedata in thisonegame.items():
                        try:
                            round_number = int(this_round)
                        except ValueError:
                            if (this_round == 'QF'):
                                round_number = 31
                            elif (this_round == 'EF'):
                                round_number = 32
                            elif (this_round == 'SF'):
                                round_number = 40
                            elif (this_round == 'PF'):
                                round_number = 50
                            elif (this_round == 'GF'):
                                round_number = 60
                            else:
                                print('??????????.... this_round = '+this_round)
                        df = pandas.DataFrame.from_records(thisgamedata, index=[0])
                        df = df.assign(playerID = this_playerID)
                        df = df.assign(theyear = int(this_year))
                        df = df.assign(round_number = pandas.to_numeric(round_number, downcast='integer', errors='coerce'))
                        game_stats_df = pandas.concat((game_stats_df, df), axis=0)
print('fixing index...')
game_stats_df = game_stats_df.reset_index(drop=True)
print('writing out...')
column_order = ['playerID', 'team', 'theyear', 'round_number', 'Opponent', 'R', '%P', '1%', 'BH', 'BO', 'BR', 'CG', 'CL']
column_order += ['CM', 'CP', 'DI', 'FA', 'FF', 'GA', 'GL', 'HB', 'HO', 'IF', 'KI', 'MI', 'MK', 'RB', 'TK', 'UP']
game_stats_df[column_order].to_csv(afldir+'player_stats_csv/player_game_stats_12k.csv', encoding='utf-8')
print('Done!')
