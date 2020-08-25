import os
import pandas
import re
afldir = '/Users/raddick/Documents/GitHub/sportsball/afl/'
os.chdir(afldir)
df = pandas.read_csv(afldir+'all_afl_games.csv', encoding='utf-8')
df = df.assign(hq1g = df['home_scoreline'].apply(lambda x: re.split('\s+', x.strip())[0].split('.')[0]))
df = df.assign(hq1b = df['home_scoreline'].apply(lambda x: re.split('\s+', x.strip())[0].split('.')[1]))
df = df.assign(hq2g = df['home_scoreline'].apply(lambda x: re.split('\s+', x.strip())[1].split('.')[0]))
df = df.assign(hq2b = df['home_scoreline'].apply(lambda x: re.split('\s+', x.strip())[1].split('.')[1]))
df = df.assign(hq3g = df['home_scoreline'].apply(lambda x: re.split('\s+', x.strip())[2].split('.')[0]))
df = df.assign(hq3b = df['home_scoreline'].apply(lambda x: re.split('\s+', x.strip())[2].split('.')[1]))
df = df.assign(home_goals = df['home_scoreline'].apply(lambda x: re.split('\s+', x.strip())[3].split('.')[0]))
df = df.assign(home_behinds = df['home_scoreline'].apply(lambda x: re.split('\s+', x.strip())[3].split('.')[1]))
df = df.assign(aq1g = df['away_scoreline'].apply(lambda x: re.split('\s+', x.strip())[0].split('.')[0]))
df = df.assign(aq1b = df['away_scoreline'].apply(lambda x: re.split('\s+', x.strip())[0].split('.')[1]))
df = df.assign(aq2g = df['away_scoreline'].apply(lambda x: re.split('\s+', x.strip())[1].split('.')[0]))
df = df.assign(aq2b = df['away_scoreline'].apply(lambda x: re.split('\s+', x.strip())[1].split('.')[1]))
df = df.assign(aq3g = df['away_scoreline'].apply(lambda x: re.split('\s+', x.strip())[2].split('.')[0]))
df = df.assign(aq3b = df['away_scoreline'].apply(lambda x: re.split('\s+', x.strip())[2].split('.')[1]))
df = df.assign(away_goals = df['away_scoreline'].apply(lambda x: re.split('\s+', x.strip())[3].split('.')[0]))
df = df.assign(away_behinds = df['away_scoreline'].apply(lambda x: re.split('\s+', x.strip())[3].split('.')[1]))


df = df.assign(game_time_string = df['infos'].apply(lambda x: x[0:x.find('Att: ')]))
df = df.assign(game_time = pandas.to_datetime(df['game_time_string'], errors='coerce'))
df.loc[df['game_time_string'].apply(lambda x: x.find('(') > -1), 'game_time'] = pandas.to_datetime(df['infos'][df['game_time'].isnull()].apply(lambda x: x[:x.find('(')].strip()), errors='coerce')
df.loc[df['game_time'].isnull(), 'game_time_string'] = df['infos'][df['game_time'].isnull()].apply(lambda x: x[:x.find('Venue: ')].strip())
df.loc[df['game_time'].isnull(), 'game_time'] = pandas.to_datetime(df['game_time_string'][df['game_time'].isnull()], errors='coerce')

df = df.assign(attendance = pandas.to_numeric(df['infos'][df['infos'].apply(lambda x: x.find('Att:') != None)].apply(lambda x: x[x.find('Att: ')+5:x.find('Venue: ')].replace(',', '')), downcast='integer', errors='coerce'))
df = df.assign(venue = df['infos'].apply(lambda x: x[x.find('Venue: ')+7:].strip()))

abbrev_df = pandas.read_excel(afldir+'team_abbrevs.xlsx')
df = df.assign(home_abbrev = df.merge(abbrev_df, how='left', left_on='home_team', right_on='team')['abbrev'])

df = df.assign(gameID = df.apply(lambda row: row['home_abbrev']+row['game_time'].strftime('%Y%m%d'), axis=1))

df = df.drop_duplicates()

columns = ['gameID', 'season', 'round', 'game_time', 'venue', 'attendance']
columns += ['home_team', 'hq1g', 'hq1b', 'hq2g', 'hq2b', 'hq3g', 'hq3b', 'home_goals', 'home_behinds', 'home_score']
columns += ['away_team', 'aq1g', 'aq1b', 'aq2g', 'aq2b', 'aq3g', 'aq3b', 'away_goals', 'away_behinds', 'away_score']

df[columns].to_csv(afldir+'games_parsed.csv', encoding='utf-8')
print('Done!')
#print(df[['gameID', 'home_team', 'home_score', 'away_team', 'away_score', 'game_time']][df.duplicated('gameID', keep=False) == True].sort_values('gameID'))