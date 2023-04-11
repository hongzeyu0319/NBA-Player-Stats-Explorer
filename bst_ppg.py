'''
Under construction...

Playaround with the BST for finding the closest player in PPG

'''

from utils import load_player_stats
from BSTNode import BSTNode

print("Welcome to the NBA Player Stats Explorer!\n")

# Load the data
year = input("Please provide the year you want to check, for example 22-23 season should be year 2023: ")
json_file = f'reg_data/nba_{year}_stats_cache.json' 
player_stats = load_player_stats(json_file)

# Build the binary search tree
root = BSTNode(player_stats[0])
for player in player_stats[1:]:
    root.insert(player)

# Find a player who averages 30.0 points
target_points = 30.0
closest_player = root.find_closest(target_points, root.player_data)
print(f"\nPlayer closest to {target_points} points per game: {closest_player['player']} ({closest_player['pts_per_g']} points)\n")

# Find the player with the scoring average most similar to the player you want
player_points = 0

while True:
    try:
        player_name = input("Please provide the player you want to check: ")
        player_found = False
        
        for player in player_stats:
            if player["player"] == player_name:
                player_points = float(player["pts_per_g"])
                print(f"{player_name}'s average points per game: {player_points}\n")
                player_found = True
                break
        
        if player_found:
            break
        else:
            raise ValueError("The player name is not correct, please check the spelling\n")
    
    except ValueError as e:
        print(e)

closest_player = root.find_closest(player_points, root.player_data)
if closest_player["player"] != player_name:
    print(f"Player with the scoring average same to {player_name}: {closest_player['player']} ({closest_player['pts_per_g']} points)\n")
else:
    print(f"{player_name} has a unique scoring average.\n")

print("Thank you for using NBA Stats Explorer!\n")
