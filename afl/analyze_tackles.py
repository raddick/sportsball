import os
import pandas
import scipy.stats as stats

firstyear = 1993
afldir = '/Users/raddick/Documents/GitHub/sportsball/afl/'
os.chdir(afldir)
df = pandas.read_csv(afldir+'game_stats.csv', encoding='utf-8', low_memory=False, index_col=['gameID', 'team'])
df = df.drop('Unnamed: 0', axis=1)

print('Analyzing {0:,.0f} AFL games since {1:.0f}...\n'.format(len(df[df['season'] >= firstyear])/2, firstyear))
print('Winning teams average {0:.02f} tackles per game.'.format(df[(df['season'] >= firstyear) & (df['result'] == 'W')]['TK'].mean()))
print('Losing teams average {0:.02f} tackles per game.'.format(df[(df['season'] >= firstyear) & (df['result'] == 'L')]['TK'].mean()))

(t,p) = stats.ttest_rel(df[(df['season'] >= firstyear) & (df['result'] == 'W')]['TK'], df[(df['season'] >= firstyear) & (df['result'] == 'L')]['TK'])
print('This is statistically significant (p = {0:.03f}).'.format(p))