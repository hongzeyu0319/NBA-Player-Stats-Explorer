import json

def load_player_stats(json_file):
    """
    Load NBA player stats from a JSON file.

    Parameters
    ----------
    json_file : str
        The path to the JSON file containing the player stats.

    Returns
    -------
    list
        A list of dictionaries representing the player stats, with each dictionary
        containing the following keys: 'player', 'season', 'team', 'games_played',
        'games_started', 'minutes_played', 'field_goals', 'field_goal_attempts',
        'field_goal_percentage', 'three_pointers', 'three_point_attempts',
        'three_point_percentage', 'two_pointers', 'two_point_attempts',
        'two_point_percentage', 'free_throws', 'free_throw_attempts',
        'free_throw_percentage', 'offensive_rebounds', 'defensive_rebounds',
        'total_rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'personal_fouls',
        'points'.
    """
    with open(json_file, 'r', encoding='utf-8') as file:
        player_stats = json.load(file)
    return player_stats

