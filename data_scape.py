from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

'''Get the Per Game Stats table'''
# Set up webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run the browser in headless mode
driver = webdriver.Chrome(options=options)

# Get the webpage
url = 'https://www.basketball-reference.com/leagues/NBA_2023_per_game.html'
driver.get(url)

# Save the page content to an HTML file
page_content = driver.page_source

with open('nba_stats_cache.html', 'w', encoding='utf-8') as cache_file:
    cache_file.write(page_content)

# Close the webdriver
driver.quit()

# Read the cached HTML content
with open('nba_stats_cache.html', 'r', encoding='utf-8') as cache_file:
    page_content = cache_file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(page_content, 'html.parser')

# Find the Per Game Stats table
pgs_table = soup.find(id='per_game_stats')

'''Extract the stats'''
# Extract player names and stats from the table
table_rows = pgs_table.tbody.find_all('tr')
player_stats = []
processed_players = set()

for row in table_rows:
    row_class = row.get('class')
    if row_class not in ['thead', 'stat_total']:
        try:
            player_name = row.find('td', {'data-stat': 'player'}).a.text
            team = row.find('td', {'data-stat': 'team_id'}).text
            points = row.find('td', {'data-stat': 'pts_per_g'}).text
            assists = row.find('td', {'data-stat': 'ast_per_g'}).text
            rebounds = row.find('td', {'data-stat': 'trb_per_g'}).text

            if player_name not in processed_players:
                if player_name and points and assists and rebounds:
                    player_stats.append((player_name, float(points), float(assists), float(rebounds)))
                    if team == "TOT":
                        processed_players.add(player_name)
        except (AttributeError, NoSuchElementException):
            continue

# Sort the players and print the top 10 players in PPG, APG, and RPG
for stat, stat_name in [('PPG', 'Points Per Game'), ('APG', 'Assists Per Game'), ('RPG', 'Rebounds Per Game')]:
    index = {'PPG': 1, 'APG': 2, 'RPG': 3}[stat]
    player_stats.sort(key=lambda x: x[index], reverse=True)

    print(f"Top 10 Players in {stat_name}:")
    for i, (player_name, points, assists, rebounds) in enumerate(player_stats[:10]):
        print(f"{i + 1}. {player_name}: {points if stat == 'PPG' else assists if stat == 'APG' else rebounds}")
    print()

driver.quit()
