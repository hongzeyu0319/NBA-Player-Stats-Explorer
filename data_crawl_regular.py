'''Crawling and scraping multiple years of NBA regular season player stats'''
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

def get_season_stats(season):
    """
    Get the Per Game Stats table for the regular season of a given NBA season and return the stats as a list of dictionaries.

    Parameters
    ----------
    season : int
        The year of the NBA season to fetch the stats for, e.g., 2022 for the 2021-2022 season.

    Returns
    -------
    player_stats : list of dict
        A list of dictionaries containing the per-game stats for each player in the given NBA season.
        Each dictionary contains the stats as key-value pairs, where the key is the stat name (e.g., "pts_per_g")
        and the value is the corresponding stat value.

    Notes
    -----
    This function uses a headless Chrome webdriver to fetch the season stats from the basketball-reference.com website.
    The stats are then extracted from the HTML content using BeautifulSoup and returned as a list of dictionaries.

    The function also saves the fetched HTML content to a cache file, which is later read to parse the stats.
    This is done to avoid fetching the same data multiple times and reduce the load on the basketball-reference.com servers.
    """
    # Set up webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run the browser in headless mode
    driver = webdriver.Chrome(options=options)

    # Get the webpage
    url = f'https://www.basketball-reference.com/leagues/NBA_{season}_per_game.html'
    driver.get(url)

    # Save the page content to an HTML file
    page_content = driver.page_source

    cache_file_name = f'reg_data/nba_{season}_stats_cache.html'
    with open(cache_file_name, 'w', encoding='utf-8') as cache_file:
        cache_file.write(page_content)

    # Close the webdriver
    driver.quit()

    # Read the cached HTML content
    with open(cache_file_name, 'r', encoding='utf-8') as cache_file:
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
                player_data = {}
                for td in row.find_all('td'):
                    data_stat = td.get('data-stat')
                    player_data[data_stat] = td.text

                if 'player' in player_data:
                    player_name = player_data['player']
                    team = player_data['team_id']

                    if player_name not in processed_players:
                        player_stats.append(player_data)
                        if team == "TOT":
                            processed_players.add(player_name)

            except (AttributeError, NoSuchElementException):
                continue

    return player_stats

# Set the range of seasons we want to scrape
start_season = 2000
end_season = 2023

# Iterate through each season
for season in range(start_season, end_season + 1):
    player_stats = get_season_stats(season)

    # Save the stats to a JSON file
    with open(f'reg_data/nba_{season}_stats_cache.json', 'w', encoding='utf-8') as json_file:
        json.dump(player_stats, json_file, ensure_ascii=False, indent=4)
