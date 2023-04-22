from utils import load_player_stats, check_quit
from tree import BSTNode

print("Welcome to the NBA Player Stats Explorer!\n")
print("You can quit the game anytime by typing quit:)\n")

while True:
    # Load the data
    while True:
        try:
            year = input("Please provide the year you want to check, for example 22-23 season should be year 2023 (year no prior than 2000 only): ")
            check_quit(year)
            year = int(year)
            if year < 2000:
                print("Please provide a year no prior than 2000")
            else:
                break
        except ValueError:
            print("Invalid input, please provide a valid year")

    while True:
        season = input("\nWould you like to explore regular season stats or playoff season stats, please type in 'regular' or 'playoff':")
        check_quit(season)
        if season == 'playoff':
            json_file = f'playoff_data/nba_{year}_playoff_stats_cache.json'
            break 
        elif season == 'regular':
            json_file = f'reg_data/nba_{year}_stats_cache.json'
            break
        else:
            print('Invalid input, please try again') 

    player_stats = load_player_stats(json_file)

    # Build the binary search tree
    root = BSTNode(player_stats[0])
    for player in player_stats[1:]:
        root.insert(player)

    # Find a player who averages a certain statistic
    while True:
        try:
            target_stat_input = input("\nWhich statistic would you like to find the closest player for? Please enter 'pts', 'reb', or 'ast': ")
            check_quit(target_stat_input)
            if target_stat_input not in ['pts', 'reb', 'ast']:
                raise ValueError("Invalid input, please enter 'pts', 'reb', or 'ast'")
            break
        except ValueError as e:
            print(e)

    stat_name = ""
    if target_stat_input == 'pts':
        target_stat = 'pts_per_g'
        stat_name = 'points'
    elif target_stat_input == 'reb':
        target_stat = 'trb_per_g'
        stat_name = 'rebounds'
    elif target_stat_input == 'ast':
        target_stat = 'ast_per_g'
        stat_name = 'assists'

    while True:
        try:
            target_stat_value_input = input(f"\nEnter a target {stat_name} per game to find the closest player: ")
            check_quit(target_stat_value_input)
            target_stat_value = float(target_stat_value_input)
            break
        except ValueError:
            print("Invalid input, please provide a valid number")

    closest_player = root.find_closest(target_stat_value, target_stat_value, target_stat_value, root.player_data)
    print(f"\nPlayer closest to {target_stat_value} {stat_name} per game: {closest_player['player']} ({closest_player[target_stat]} {stat_name})\n")

    # Find the player with the statistic value most similar to the player you want
    player_stat_value = 0

    while True:
        try:
            player_name = input("\nPlease provide the player you want to check for the closest stats: ")
            check_quit(player_name)
            player_found = False
            
            for player in player_stats:
                if player["player"] == player_name:
                    player_stat_value = float(player[target_stat])
                    print(f"{player_name}'s average {stat_name} per game: {player_stat_value}\n")
                    player_found = True
                    break
                
            if not player_found:
                raise ValueError("The player name is not correct, please check the spelling of the name\n")

        except ValueError as e:
            print(e)

        closest_player = root.find_closest(player_stat_value, player_stat_value, player_stat_value, root.player_data)
        
        if closest_player["player"] != player_name:
            print(f"Player with the {stat_name} average closest to {player_name}: {closest_player['player']} ({closest_player[target_stat]} {stat_name})\n")
        else:
            print(f"{player_name} has a unique {stat_name} average.\n")

        # Ask the user if they want to check another player
        while True:
            try:
                play_again = input("Would you like to check another player? (y/n): ")
                check_quit(play_again)
                if play_again.lower() not in ['y', 'n']:
                    raise ValueError("Invalid input, please enter 'y' or 'n'")
                break
            except ValueError as e:
                print(e)

        if play_again.lower() == 'n':
            break

    while True:
        try:
            play_again = input("Do you want to play the whole game again? (y/n): ")
            check_quit(play_again)
            if play_again.lower() not in ['y', 'n']:
                raise ValueError("Invalid input, please enter 'y' or 'n'")
            break
        except ValueError as e:
            print(e)

    if play_again.lower() == 'n':
        break


print("Thank you for using NBA Stats Explorer!\n")
