from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO

#following the youtube video: "https://www.youtube.com/watch?v=Nt7WJa2iu0s" to create a prediction of premier league results

#landing page for EPL Stats
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
data = requests.get(standings_url)
soup = BeautifulSoup(data.text, "html.parser")

#get the standings table with all the teams
standings_table = soup.select('table.stats_table')[0]
#extract team links
links = standings_table.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if '/squads/' in l]
team_urls = [f"https://fbref.com{l}" for l in links]
team_url = team_urls[0]

#go into individual team pages
data = requests.get(team_url)
html_content = StringIO(data.text)
#get the scores and fixtures for each game
matches = pd.read_html(html_content, match="Scores & Fixtures")[0]

#get the shooting stats
soup = BeautifulSoup(data.text, "html.parser")
links = soup.find_all('a')
links = [l.get("href") for l in links]
#find all the links that go to the shooting table for each match of that season
links = [l for l in links if l and 'all_comps/shooting/' in l]
print(links)
data = requests.get(f"https://fbref.com{links[0]}")
#get the shooting table
html_content = StringIO(data.text)
#only want the first table which is specifically liverpools data for shooting  <- this may be a bit skewed but
shooting_table = pd.read_html(html_content, match="Shooting")[0]
shooting_table.columns = shooting_table.columns.droplevel()
print(shooting_table.head())
print(matches.head())

#next to merge the shooting data and the matches data together in a single table as they are synced up per game
team_data = matches.merge(shooting_table[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
print(team_data)


