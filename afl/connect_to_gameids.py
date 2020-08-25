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

stats_df = pandas.DataFrame()
for i in range(0,13):
    print(i)
    filename = afldir+'player_stats_csv/player_game_stats_{0:.0f}k.csv'.format(i)
    df = pandas.read_csv(filename, encoding='utf-8', low_memory=False)
    stats_df = pandas.concat((stats_df, df), axis=0)
stats_df = stats_df.rename(columns={'theyear': 'season'})
#print(stats_df[['playerID', 'theyear', 'round_number', 'team', 'Opponent']].sample(1))
#print('\n')
#print(games_df[['season', 'round_number', 'home_team', 'away_team']].sample(2))
print('joining...')


#stats_df = stats_df.merge(games_df[['season','round_number','gameID']], how='left', on=['season', 'round_number'])
#stats_df = stats_df.drop('Unnamed: 0', axis=1)


hstats_df = stats_df.merge(games_df[['season', 'round_number', 'home_team', 'gameID']], how='left', left_on=['season', 'round_number', 'team'], right_on=['season', 'round_number', 'home_team'])
hstats_df = hstats_df[hstats_df['home_team'].notnull()]

astats_df = stats_df.merge(games_df[['season', 'round_number', 'away_team', 'gameID']], how='left', left_on=['season', 'round_number', 'team'], right_on=['season', 'round_number', 'away_team'])
astats_df = astats_df[astats_df['away_team'].notnull()]

allstats_df = pandas.concat((hstats_df, astats_df), axis=0)
allstats_df = allstats_df.drop(['Unnamed: 0', 'home_team', 'away_team'], axis=1)

allstats_df = allstats_df.set_index(['playerID', 'gameID'])

allstats_df.to_csv('all_stats.csv', encoding='utf-8')
print('Done!')
