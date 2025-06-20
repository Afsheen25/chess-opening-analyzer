import pandas as pd
import numpy as np

cols = ['Result', 'ECO', 'Opening']
df = pd.read_csv("data/tournament-chess-games.csv", usecols=cols)

df.dropna(inplace=True)

def get_winner(result):
    if result == "1-0":
        return "white"
    elif result == "0-1":
        return "black"
    else:
        return "draw"
    
df['winner'] = df['Result'].apply(get_winner)

print(df.head())

grouped = df.groupby(['ECO', 'Opening'])['winner'].value_counts().unstack(fill_value=0).reset_index()
grouped['Total'] = grouped['white'] + grouped['black'] + grouped['draw']
grouped['White_Win_%'] = (grouped['white'] / grouped['Total']) * 100
grouped['Black_Win_%'] = (grouped['black'] / grouped['Total']) * 100
grouped['Draw_%'] = (grouped['draw'] / grouped['Total']) * 100

grouped['WinRate_Variance'] = grouped.apply(lambda row: np.var([row['White_Win_%'], row['Black_Win_%']]), axis=1)
grouped['WinRate_StdDev'] = grouped.apply(lambda row: np.std([row['White_Win_%'], row['Black_Win_%']]), axis=1)

most_played = grouped.sort_values(by='Total', ascending=False).head()
most_consistent = grouped.sort_values(by='WinRate_StdDev').head()
grouped.to_csv("data/opening_stats_summary.csv", index=False)
