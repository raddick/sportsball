import os
import pandas
import numpy as np
afldir = '/Users/raddick/Documents/GitHub/sportsball/afl/'
os.chdir(afldir)
df = pandas.read_csv(afldir+'all_stats.csv', encoding='utf-8', low_memory=False)#, index_col=['playerID', 'gameID'])

sum_columns = ['1%', 'BH', 'BO', 'BR', 'CG', 'CL', 'CM', 'CP']
sum_columns += ['DI', 'FA', 'FF', 'GA', 'GL', 'HB', 'HO', 'IF', 'KI', 'MI', 'MK']
sum_columns += ['RB', 'TK', 'UP']

career_stats_df = df.groupby('playerID')[sum_columns].sum()

names_df = pandas.read_csv(afldir+'all_player_names.csv')
names_df = names_df.rename(columns={'player_id': 'playerID'})

career_stats_df = career_stats_df.merge(names_df[['playerID', 'name_last', 'name_first', 'first_year', 'last_year']], how='left', on='playerID')
career_stats_df = career_stats_df.set_index('playerID')

career_stats_df.to_csv(afldir+'career_stats.csv', encoding='utf-8')

game_stats_df = df.groupby(['gameID', 'team'])[sum_columns].sum()
games_df = pandas.read_csv('games_parsed.csv', encoding='utf-8', index_col='Unnamed: 0')
games_df = games_df.set_index('gameID', drop=True)
game_stats_df = game_stats_df.join(games_df, how='left')
game_stats_df = game_stats_df.reset_index()
game_stats_df = game_stats_df.assign(home_game = np.nan)
game_stats_df.loc[game_stats_df['team'] == game_stats_df['home_team'], 'home_game'] = True
game_stats_df.loc[game_stats_df['team'] != game_stats_df['home_team'], 'home_game'] = False

game_stats_df = game_stats_df.assign(result = np.nan)
game_stats_df.loc[(game_stats_df['home_score'] == game_stats_df['away_score']), 'result'] = 'D'

game_stats_df.loc[(game_stats_df['home_game'] == True) & (game_stats_df['home_score'] > game_stats_df['away_score']), 'result'] = 'W'
game_stats_df.loc[(game_stats_df['home_game'] == True) & (game_stats_df['home_score'] < game_stats_df['away_score']), 'result'] = 'L'

game_stats_df.loc[(game_stats_df['home_game'] == False) & (game_stats_df['away_score'] > game_stats_df['home_score']), 'result'] = 'W'
game_stats_df.loc[(game_stats_df['home_game'] == False) & (game_stats_df['away_score'] < game_stats_df['home_score']), 'result'] = 'L'

game_stats_df = game_stats_df.assign(points = np.nan)
game_stats_df.loc[game_stats_df['result'] == 'L', 'points'] = 0
game_stats_df.loc[game_stats_df['result'] == 'D', 'points'] = 1
game_stats_df.loc[game_stats_df['result'] == 'W', 'points'] = 2

game_stats_df.to_csv(afldir+'game_stats.csv', encoding='utf-8')
print('Done!')
