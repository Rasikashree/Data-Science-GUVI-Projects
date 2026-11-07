"""
Project: Predictive Analysis of IPL Match Outcomes

Business Case: The Indian Premier League (IPL) is one of the most popular cricket leagues
globally, generating massive interest and revenue each year. For franchise owners, sponsors,
broadcasters, and fans, predicting match outcomes accurately is crucial for strategic decision-making,
betting, and overall enjoyment of the sport. Leveraging data analytics and machine learning can provide
valuable insights into factors influencing match results, player performances, and team strategies.

Description: This project aims to conduct a comprehensive data analysis of IPL matches to predict
outcomes using historical match data, player statistics, weather conditions, and other relevant variables.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fivethirtyeight')
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls

matches = pd.read_csv('matches.csv')
delivery = pd.read_csv('deliveries.csv')
print(matches.head())
print(delivery.head())


# Cleaning and Transformations

matches.drop(['umpire3'], axis=1, inplace=True)

team_names = {
    'Sunrisers Hyderabad': 'SRH',
    'Mumbai Indians': 'MI',
    'Gujarat Lions': 'GL',
    'Rising Pune Supergiant': 'RPS',
    'Rising Pune Supergiants': 'RPS',
    'Royal Challengers Bangalore': 'RCB',
    'Kolkata Knight Riders': 'KKR',
    'Delhi Daredevils': 'DD',
    'Kings XI Punjab': 'KXIP',
    'Chennai Super Kings': 'CSK',
    'Rajasthan Royals': 'RR',
    'Deccan Chargers': 'DC',
    'Kochi Tuskers Kerala': 'KTK',
    'Pune Warriors': 'PW'
}

matches.replace(team_names, inplace=True)
delivery.replace(team_names, inplace=True)

# Basic Analysis

print("Total Matches Played:", matches.shape[0])
print("\nVenues Played At:", matches['city'].unique())
print("\nTeams:", matches['team1'].unique())
print("\nTotal Venues played:", matches['city'].nunique())
print("\nTotal Umpires:", matches['umpire1'].nunique())
print((matches['player_of_match'].value_counts()).idxmax(),": has the most number of man of the match awards")
print((matches['winner'].value_counts()).idxmax(),": has the highest number of match wins")

df = matches.iloc[[matches['win_by_runs'].idxmax()]]
print("Win by Runs",df[['season','team1','team2','winner','win_by_runs']])

df = matches.iloc[[matches['win_by_wickets'].idxmax()]]
print("Win by Wickets",df[['season','team1','team2','winner','win_by_wickets']])

# Toss Decisions
print("Sum:",matches['toss_decision'].value_counts().sum())
print("Toss Decisions in %\n", ((matches['toss_decision']).value_counts(normalize = True))*100)

# Toss Decisions across Seasons
plt.subplots(figsize = (10,6))
sns.countplot(x = 'season', hue = 'toss_decision', data = matches)
plt.show()


# Max Toss Winners
plt.subplots(figsize = (10,6))
ax = matches['toss_winner'].value_counts().plot.bar(width = 0.9, color = sns.color_palette('RdYlGn',20))
for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x() + 0.15, p.get_height()+1))
plt.show()

# Total Matches Vs Wins for Teams

matches_played_byteams = pd.concat([matches['team1'], matches['team2']])
matches_played_byteams = matches_played_byteams.value_counts().reset_index()
matches_played_byteams.columns = ['Teams','Total Matches']
matches_played_byteams['Wins'] = matches_played_byteams['Teams'].map(matches['winner'].value_counts()).fillna(0).astype(int)
matches_played_byteams.set_index("Teams", inplace = True)

trace1 = go.Bar(x = matches_played_byteams.index, y = matches_played_byteams['Total Matches'], name = 'Total Matches')
trace2 = go.Bar(x = matches_played_byteams.index, y = matches_played_byteams['Wins'], name = 'Matches Won')
data = [trace1, trace2]
layout = go.Layout(barmode = 'stack')
fig = go.Figure(data = data, layout = layout)
fig.show()


# py.init_notebook_mode(connected=True)
matches_played_byteams = pd.concat([matches['team1'], matches['team2']])
matches_played_byteams = matches_played_byteams.value_counts().reset_index()
matches_played_byteams.columns = ['Team', 'Total Matches']
wins = matches['winner'].value_counts().reset_index()
wins.columns = ['Team', 'Wins']
matches_played_byteams = matches_played_byteams.merge (wins, on='Team', how='left')
matches_played_byteams['Wins'].fillna(0, inplace=True) # Handle teams with no wins
matches_played_byteams.set_index('Team', inplace=True)
# Debug: Check the DataFrame structure
print(matches_played_byteams)
# Step 6: Create stacked bar chart
trace1 = go.Bar(x = matches_played_byteams.index, y = matches_played_byteams['Total Matches'], name = 'Total Matches')
trace2 = go.Bar(x = matches_played_byteams.index, y = matches_played_byteams['Wins'], name = 'Matches Won')
data = [trace1, trace2]
layout = go.Layout(title = 'Total Matches Vs Matches Won by Teams',xaxis = dict(title = 'Teams'),yaxis = dict(title = 'Count'),barmode = 'stack')
fig = go.Figure(data = data, layout = layout)
# py.iplot(fig, filename = 'stacked-bar')
fig.show()


# Is Toss Winner also the match winner
print("Matches Shape: ",matches.shape)
print("Length of df: ",len(df))
df = matches[matches['toss_winner'] == matches['winner']]
slices = [len(df), (636 - len(df))]
labels = ['yes','no']
plt.pie(slices, labels = labels, startangle = 90, shadow = True, explode = (0,0.1), autopct = "1.1f%%", colors = ['r','g'])
fig = plt.gcf()
fig.set_size_inches(6,6)
plt.show()


# Matches Played across each season
plt.figure(figsize=(10, 6))

sns.countplot(
    x='season',
    data=matches,
    hue='season',
    palette='winter',
    legend=False
)

plt.title("Matches Played Across Each Season")
plt.xlabel("Season")
plt.ylabel("Number of Matches")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Runs across the season
# Check the correct ID column in delivery
if 'match_id' in delivery.columns:
    delivery_id = 'match_id'
elif 'id' in delivery.columns:
    delivery_id = 'id'
else:
    raise KeyError("No match ID column found in delivery DataFrame")

batsmen = matches[['id', 'season']].merge(
    delivery,
    left_on='id',
    right_on=delivery_id,
    how='left'
)

season = batsmen.groupby('season')['total_runs'].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.plot(
    season['season'],
    season['total_runs'],
    marker='o'
)

plt.title("Total Runs Across the Seasons")
plt.xlabel("Season")
plt.ylabel("Total Runs")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# Average runs per match in each season
matches_per_season = (
    matches.groupby('season')['id']
    .nunique()
    .reset_index(name='matches')
)

avgruns_each_season = matches_per_season.merge(
    season,
    on='season',
    how='left'
)

avgruns_each_season['average_runs_per_match'] = (
    avgruns_each_season['total_runs'] /
    avgruns_each_season['matches']
)

plt.figure(figsize=(10, 6))
plt.plot(
    avgruns_each_season['season'],
    avgruns_each_season['average_runs_per_match'],
    marker='o'
)

plt.title("Average Runs Per Match Across Seasons")
plt.xlabel("Season")
plt.ylabel("Average Runs Per Match")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# Sixes and Fours Across the Season

# Count sixes in each season
sixes = batsmen.groupby('season')['batsman_runs'].apply(
    lambda x: (x == 6).sum()
).reset_index(name='6s')

# Count fours in each season
fours = batsmen.groupby('season')['batsman_runs'].apply(
    lambda x: (x == 4).sum()
).reset_index(name='4s')

# Merge sixes and fours
season_boundaries = sixes.merge(
    fours,
    on='season',
    how='left'
)

# Plot the results
season_boundaries.set_index('season')[['6s', '4s']].plot(
    marker='o',
    figsize=(10, 6)
)

plt.title('Sixes and Fours Across the Seasons')
plt.xlabel('Season')
plt.ylabel('Number of Boundaries')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Runs Per Over By Teams Across Seasons
runs_per_over = delivery.pivot_table(index = ['over'], columns = 'batting_team', values = 'total_runs', aggfunc = sum)
runs_per_over[(matches_played_byteams[matches_played_byteams['Total Matches'] > 50].index)].plot(color = ['b','r','#Ffb6b2',"g",'brown','y','#6666ff','black','#FFA500'])
x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
plt.xticks(x)
plt.ylabel('total runs scored')
fig = plt.gcf()
fig.set_size_inches(16,10)
plt.show()

# Favorite Grounds
plt.subplots(figsize=(10, 15))
ax = matches['venue'].value_counts().sort_values(ascending = True).plot.barh(width = 0.9, color = sns.color_palette('inferno',40))
ax.set_xlabel('Grounds')
ax.set_ylabel('Count')
plt.show()

# Maximum Man of Matches
plt.subplots(figsize=(10, 6))
ax = matches['player_of_match'].value_counts().head(10).plot.bar(width = 0.8, color = sns.color_palette('inferno',40))
ax.set_xlabel('player of match')
ax.set_ylabel('count')
for p in ax.patches:
    ax.annotate(format(p.get_height()),(p.get_x() + 0.15, p.get_height() + 0.25))
plt.show()

# Winner by Year
print('Winner by years:\n')
for i in range(2008,2017):
    df = ((matches[matches['season'] == i]).iloc[-1])
    print(df.iloc[[1,10]].values)

# Super Over
super_over = delivery[delivery['is_super_over'] == 1]
print("\n Total Matches with Super Overs:", super_over['match_id'].nunique())

# Favorite Umpires
plt.figure(figsize=(10, 6))

ump = pd.concat([matches['umpire1'], matches['umpire2']])

ax = ump.value_counts().head(10).plot.bar(
    width=0.8,
    color=sns.color_palette('summer', 10)
)

for p in ax.patches:
    ax.annotate(
        str(int(p.get_height())),
        (p.get_x() + p.get_width() / 2, p.get_height()),
        ha='center',
        va='bottom'
    )

plt.title("Top 10 Favorite Umpires")
plt.xlabel("Umpires")
plt.ylabel("Number of Matches")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Team1 Vs Team2
# MI Vs KKR

def team1_vs_team2(team1, team2):

    mt1 = matches[
        ((matches['team1'] == team1) & (matches['team2'] == team2)) |
        ((matches['team1'] == team2) & (matches['team2'] == team1))
    ]

    if mt1.empty:
        print("No matches found for these teams.")
        return

    plt.figure(figsize=(10, 6))

    sns.countplot(
        x='season',
        hue='winner',
        data=mt1,
        palette='Set3'
    )

    plt.title(f'{team1} Vs {team2}')
    plt.xlabel('Season')
    plt.ylabel('Number of Matches')
    plt.xticks(rotation=45)
    plt.legend(loc='upper center')
    plt.tight_layout()
    plt.show()
# Call the function
team1_vs_team2('MI', 'KKR')


# Matches Won by a team against other teams
def comparator(team1):
    teams = ['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW']
    teams.remove(team1)
    opponent = teams.copy()
    mt1 = matches[((matches['team1'] == team1) | (matches['team2'] == team1))]
    for i in opponent:
        mask = (((mt1['team1'] == i)| (mt1['team2'] == i))) & ((mt1['team1'] ==  team1) | (mt1['team2'] == team1))
        mt2 = mt1.loc[mask,'winner'].value_counts().to_frame().T
        print(mt2)
comparator('MI')

# Score Distribution For Teams by Innings
plt.subplots(figsize=(12, 6))
xyz = delivery.groupby(['match_id','inning','batting_team'])['total_runs'].sum().reset_index()
xyz.drop('match_id', axis = 1, inplace = True)
xyz.sort_values(by = ['batting_team','total_runs'], ascending = True)
score_1_inning = xyz[xyz['inning'] == 1]
score_2_inning = xyz[xyz['inning'] == 2]
sns.boxplot(x = 'batting_team', y = 'total_runs', data = score_1_inning).set_title("1st Innings")
plt.show()
sns.boxplot(x = 'batting_team', y = 'total_runs', data = score_2_inning).set_title("2nd Innings")
# fig = plt.gcf()
# fig.set_size_inches(12,6)
plt.show()

# 200+ Scores
high_scores = delivery.groupby(['match_id','inning','batting_team','bowling_team'])['total_runs'].sum().reset_index()
high_scores = high_scores[high_scores['total_runs'] >= 200]
print(high_scores.nlargest(10,'total_runs'))

fig,ax = plt.subplots(1,2)
sns.countplot(high_scores['batting_team'], ax = ax[0])
sns.countplot(high_scores['bowling_team'], ax = ax[1])
plt.xticks(rotation=90)
fig = plt.gcf()
fig.set_size_inches(18,6)
plt.show()

teams = ['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW']
print("Teams who have not ever scored 200+ runs", list(set(teams) - set(high_scores['batting_team'])))
print("Teams who have not connected over 200+ runs:", list(set(teams) - set(high_scores['bowling_team'])))

high = delivery.groupby(['match_id','inning','batting_team','bowling_team'])['total_runs'].sum().reset_index()
high.set_index(['match_id'],inplace = True)
high['total_runs'].max()
high = high.rename(columns = {'total_runs':'count'})
high = high[high['count'] >= 200].groupby(['inning', 'batting_team']).count()
print(high)


# Chances of Chasing 200+ Target
#
# slices = high_scores['is_score_chased'].value_counts()
# labels = slices.index.map({True: 'target chased', False: 'target not chased'}).tolist()
# plt.pie(slices.values, labels=labels, startangle=90,
#         shadow=True, explode=(0, 0.1), autopct='%1.1f%%')
# fig = plt.gcf()
# fig.set_size_inches(6, 6)
# plt.show()

balls = delivery.groupby(['batsman'])['ball'].count().reset_index()
runs = delivery.groupby(['batsman'])['batsman_runs'].sum().reset_index()
balls = balls.merge(runs, left_on = 'batsman', right_on = 'batsman', how = 'outer')
balls.rename({"ball": "ball_x", "batsman_runs": "ball_y"}, axis = 1, inplace = True)
fours = delivery.groupby('batsman')['batsman_runs'].agg(lambda x: (x == 4).sum()).reset_index()
sixes = delivery.groupby('batsman')['batsman_runs'].agg(lambda x: (x == 6).sum()).reset_index()
balls['strike_rate'] = balls['ball_y'] / balls['ball_x'] * 100
balls = balls.merge(sixes, left_on = 'batsman', right_on = 'batsman', how = 'outer')
balls = balls.merge(fours, left_on = 'batsman', right_on = 'batsman', how = 'outer')
compare = delivery.groupby(['match_id','batsman','batting_team'])['batsman_runs'].sum().reset_index()

compare = compare.groupby(['batsman','batting_team'])['batsman_runs'].max()
balls = balls.merge(compare, left_on = 'batsman',right_on = 'batsman', how = 'outer')
balls.rename({'ball_x':'balls',"ball_y": 'runs','batsman_runs_x': "6's", 'batsman_runs_y': "4's",'batting_team': "Team","batsman_runs": "Highest_score"}, axis = 1, inplace = True)
print(balls.head())


def batsman_comparator(stat1, stat2, batsman1, batsman2):
    sns.FacetGrid(balls, height = 8).map(plt.scatter, stat1,stat2, alpha = 0.5).add_legend()
    bats1 = balls[balls['batsman'].str.contains(batsman1)].sort_values(by = stat1, ascending = False)
    bats2 = balls[balls['batsman'].str.contains(batsman2)].sort_values(by = stat1, ascending = False)
    plt.scatter(bats2[stat1], bats2[stat2], s = 75, c = '#f73545')
    plt.text(x = bats2[stat1].values[0], y = bats2[stat2].values[0], s = batsman1, fontsize = 10, weight = 'bold', color = '#ff58fd')
    plt.gcf().set_size_inches(15,10)
    plt.title("Batsman Comparator", size = 25)
    plt.show()
batsman_comparator("6's","4's","Gayle","Villiers")


# Top 10 Batsman
plt.subplots(figsize = (10,6))
max_runs = delivery.groupby(['batsman'])['batsman_runs'].sum()
ax = max_runs.sort_values(ascending = False)[:10].plot.bar(width = 0.8, color = sns.color_palette("winter_r",20))
for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x() + 0.1, p.get_height() + 50), fontsize = 15)
plt.show()


# Top Batsman's with 1's, 2's, 3's, 4's
toppers = delivery.groupby(['batsman','batsman_runs'])['total_runs'].count().reset_index()
toppers = toppers.pivot_table(index = "batsman", columns = "batsman_runs", values = "total_runs", fill_value = 0)
fig, ax = plt.subplots(2,2,figsize = (18,12))
toppers[1].sort_values(ascending = False)[:5].plot(kind = 'barh', ax = ax[0,0], color = "#45ff45",width = 0.8)
ax[0,0].set_title("Most 1's")
ax[0,0].set_ylabel("")

toppers[2].sort_values(ascending = False)[:5].plot(kind = 'barh', ax = ax[0,1], color = "#4df6df",width = 0.8)
ax[0,1].set_title("Most 2's")
ax[0,1].set_ylabel("")

toppers[4].sort_values(ascending = False)[:5].plot(kind = 'barh', ax = ax[1,0], color = "#fbca5f",width = 0.8)
ax[1,0].set_title("Most 4's")
ax[1,0].set_ylabel("")

toppers[6].sort_values(ascending = False)[:5].plot(kind = 'barh', ax = ax[1,1], color = "#ffff00",width = 0.8)
ax[1,1].set_title("Most 6's")
ax[0,0].set_ylabel("")

plt.show()


# Top Individual Scores
top_scores = delivery.groupby(['match_id',"batsman",'batting_team'])['batsman_runs'].sum().reset_index()
top_scores.sort_values('batsman_runs', ascending = 0).head(10)
print(top_scores.nlargest(10,'batsman_runs'))

# Individual Scores by Top Batsman each Inning
swarm = ['CH Gayle', ' V Kohli', 'G Gambhir', 'SK Raina','VK Patham', 'MS Dhoni','AB de Villiers', 'DA Warner']
scores = delivery.groupby(['match_id','batsman','batting_team'])['batsman_runs'].sum().reset_index()
scores = scores[top_scores['batsman'].isin(swarm)]
sns.swarmplot(x = 'batsman', y = 'batsman_runs', data = scores, hue = 'batting_team', palette = 'Set2')
fig = plt.gcf()
fig.set_size_inches(14,8)
plt.ylim(-10,200)
plt.show()

#Runs Scored by Batsman Across Seasons
a = batsmen.groupby(['season','batsman'])['batsman_runs'].sum().reset_index()
a = a.groupby(['season', 'batsman'])['batsman_runs'].sum().unstack().T
a['Total'] = a.sum(axis = 1)
a.sort_values(by = 'Total', ascending = 0)[:5]
a.drop('Total',axis = 1, inplace = True)
a.T.plot(color = ['red','blue','#772272','green','#f0ff00'], marker = 'o')
fig = plt.gcf()
fig.set_size_inches(16,6)
plt.show()

# Frequency of Scores
plt.subplots(figsize = (10,6))
bins = range(0,180,10)
plt.hist(top_scores['batsman_runs'],bins, histtype = 'bar', rwidth = 1.2,color = '#ff00ff')
plt.xlabel('Runs')
plt.ylabel('Count')
plt.axvline(top_scores['batsman_runs'].mean(), color = 'b', linestyle = 'dashed', linewidth = 2)
plt.plot()
plt.show()


# Orange Caps Each Season (Highest Run Getter Per Season)
orange = matches[['id','season']]
orange = orange.merge(delivery, left_on = 'id', right_on = 'match_id', how = 'left')
orange = orange.groupby(['season', 'batsman'])['batsman_runs'].sum().reset_index()
orange = orange.sort_values('batsman_runs', ascending = 0)
orange = orange.drop_duplicates(subset = ['season'], keep = 'first')
orange.sort_values(by = 'season')
trace1 = go.Bar(x = orange['season'].values, y = orange['batsman_runs'].values,name = 'Total Matches', text = orange['batsman'].values, marker = dict(color = 'rgb(255,140,0)', line = dict(color = 'rgb(8,48,107)', width = 1.5)), opacity = 1)
layout =  go.Layout(title = "Orange-Cap Holders")
data = [trace1]
fig = go.Figure(data = data, layout = layout)
# py.iplot(fig, filename = 'stacked-bar')
fig.show()

# Top Bowlers
# Highest Wicket Taker
plt.subplots(figsize = (10,6))
dismissal_kinds = ['bowled','caught','lbw','stumped','caught and bowled',' hit wicket']
ct = delivery[delivery['dismissal_kind'].isin(dismissal_kinds)]
ax = ct['bowler'].value_counts()[:10].plot.bar(width = 0.8, color = sns.color_palette('summer_r',20))
for p in ax.patches:
    ax.annotate(format(p.get_height()), (p.get_x() + 0.10, p.get_height()), fontsize = 15)
    plt.show()

# Maximum Overs
eco = delivery.groupby(['bowler']).sum(numeric_only = True)
eco['total balls'] = delivery['bowler'].value_counts()
eco['overs'] = (eco['total balls'] // 6)
eco[eco['overs'] > 200].sort_values(by = 'overs',ascending = 0)['overs'].head(5).reset_index()
eco['economy'] = (eco['total_runs'] / (eco['overs']))
print(eco[eco['overs'] > 300].sort_values('economy')[:10].economy.reset_index().T)

# Top 20 Bowlers
bowlers = delivery.groupby('bowler').sum(numeric_only = True).reset_index()
bowl = delivery['bowler'].value_counts().reset_index()
bowl.columns = ['bowler','balls']
bowl['index'] = range(1, len(bowl) + 1)
bowl['bowler'] = bowl['bowler'].astype(str)
bowlers['bowler'] = bowlers['bowler'].astype(str)
bowlers = bowlers.merge(bowl, on = 'bowler', how = 'left')
bowlers = bowlers[['bowler','total_runs','balls']]
bowlers.rename({'total_runs': "runs_given"}, axis = 1, inplace = True)
bowlers['overs'] = bowlers['balls'] // 6
dismissal_kinds = ["bowled", "caught","lbw","stumped","caught and bowled"," hit wicket"]
ct = delivery[delivery['dismissal_kind'].isin(dismissal_kinds)]
ct = ct['bowler'].value_counts()[:20].reset_index()
ct.columns = ['bowler', 'wickets']
ct['bowler'] = ct['bowler'].astype(str)
bowlers = bowlers.merge(ct, on = 'bowler', how = 'left').dropna()
bowlers['economy'] = bowlers['runs_given'] / bowlers['overs']
print(bowlers.head(20))


trace = go.Scatter(
    y = bowlers['wickets'],
    x = bowlers['bowler'],
    mode = 'markers',
    marker = dict(
        size = bowlers['wickets'].values,
        color = bowlers['economy'].values,
        colorscale = 'Viridis',
        colorbar = dict(title = 'Economy')
    ),
    text = bowlers['overs'].values
)
data = [trace]
layout = go.Layout(autosize = True, title = 'Top 20 wicket taking bowlers', hovermode = 'closest', xaxis = dict(showgrid = False, zeroline = False, showline = False, title = 'Bowlers'),
                   yaxis = dict(title = 'Wickets Taken', ticklen = 5, gridwidth = 2, showgrid = False, zeroline = False, showline =  False),
                   showlegend = False)
fig = go.Figure(data = data, layout = layout)
# py.iplot(fig, filename = 'scatterChol')
fig.show()

# Highest Dismissals For a Batsman by a Bowler

def get_top_bowler(batsman_name):

    batsman_data = delivery[delivery['batsman'] == batsman_name]

    batsman_data = batsman_data[
        batsman_data['dismissal_kind'].isin(
            ['caught', 'lbw', 'bowled', 'stumped',
             'caught and bowled', 'hit wicket']
        )
    ]

    top_bowler = batsman_data.groupby('bowler').count().sort_values(
        by='dismissal_kind', ascending=False
    )['dismissal_kind'][:1].reset_index()

    top_bowler['batsman'] = batsman_name

    return top_bowler


batsmen = [
    'CH Gayle', 'V Kohli', 'SK Raina', 'AB de Villiers',
    'MS Dhoni', 'G Gambhir', 'RG Sharma', 'RV Uthappa',
    'S Dhawan', 'DA Warner'
]

results = [get_top_bowler(batsman) for batsman in batsmen]

new = pd.concat(results, ignore_index=True)

new = new[['batsman', 'bowler', 'dismissal_kind']]

new.columns = ['batsman', 'bowler', 'No_of_Dismissals']

print(new.head())
# Purple Caps Each Season
dismissal_kinds = ["bowled","caught","lbw","stumped","caught and bowled"," hit wicket"]
purple = delivery[delivery['dismissal_kind'].isin(dismissal_kinds)]
purple = delivery.merge(matches, left_on = 'match_id', right_on = 'id', how = 'left')
purple = purple.groupby(['season','bowler'])['dismissal_kind'].count().reset_index()
purple = purple.sort_values('dismissal_kind', ascending = False)
purple = purple.drop_duplicates('season',keep = 'first').sort_values(by = 'season')
purple.rename({'dismissal_kind': 'count_wickets'}, axis = 1, inplace = True)
print(purple)
trace1 = go.Bar(
    x = purple['season'].values,
    y = purple['count_wickets'].values,
    name = 'Total Matches',
    text = purple['bowler'].values,
    marker = dict(
        color = 'rgb(75,0,130)',
        line = dict(color = 'rgb(108,148,107)', width = 1.5)
    ),
    opacity = 1
)
layout = go.Layout(title = 'Purple-Cap Holders')
data = [trace1]
fig = go.Figure(data = data, layout = layout)
fig.show()
