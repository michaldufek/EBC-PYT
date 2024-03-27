import json
from collections import defaultdict

# Soubor, kde budou uloženy informace o zápasech
data_file = 'matches.json'

# Struktura pro ukládání a výpočet statistik týmů a hráčů
team_stats = defaultdict(lambda: {'wins': 0, 'draws': 0, 'losses': 0, 'scored': 0, 'conceded': 0})
player_stats = defaultdict(int)

# Funkce pro načtení dat ze souboru
def load_data():
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return []

# Funkce pro uložení dat do souboru
def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f)

# Funkce pro přidání zápasu
def add_match():
    date = input('Datum zápasu (DD.MM.YYYY): ')
    team1 = input('Domácí tým: ')
    team2 = input('Hostující tým: ')
    result = input('Výsledek (góly domácích:góly hostů): ')
    scorers = input('Střelci (jméno hráče a počet gólů, odděleno čárkou): ')

    # Aktualizace statistik týmů a hráčů
    goals_team1, goals_team2 = map(int, result.split(':'))
    update_team_stats(team1, team2, goals_team1, goals_team2)
    update_player_stats(scorers)

    # Uložení záznamu o zápase
    match = {'date': date, 'team1': team1, 'team2': team2, 'result': result, 'scorers': scorers}
    matches = load_data()
    matches.append(match)
    save_data(matches)
    print('Zápas byl úspěšně přidán.')

# Funkce pro aktualizaci statistik týmů
def update_team_stats(team1, team2, goals_team1, goals_team2):
    team_stats[team1]['scored'] += goals_team1
    team_stats[team1]['conceded'] += goals_team2
    team_stats[team2]['scored'] += goals_team2
    team_stats[team2]['conceded'] += goals_team1

    if goals_team1 > goals_team2:  # Vítězství domácích
        team_stats[team1]['wins'] += 1
        team_stats[team2]['losses'] += 1
    elif goals_team1 < goals_team2:  # Vítězství hostů
        team_stats[team2]['wins'] += 1
        team_stats[team1]['losses'] += 1
    else:  # Remíza
        team_stats[team1]['draws'] += 1
        team_stats[team2]['draws'] += 1

# Function for updating player statistics
def update_player_stats(scorers):
    if scorers.strip():  # If there are any scorers
        for scorer_info in scorers.split(','):
            parts = scorer_info.strip().rsplit(' ', 1)  # Split from the right to get the last part as goals
            if len(parts) == 2:  # Ensuring that there is a name and a goal count
                name, goals = parts
                player_stats[name.strip()] += int(goals)


# Function for printing the league table
def print_league_table():
    print('Ligová tabulka:')
    print(f'{"Team":<20} {"Points":<7} {"Goals":<9} {"Wins":<5} {"Draws":<6} {"Losses":<6}')
    print('-' * 60)  # Print a dividing line for clarity
    # Sorting teams by points and goal difference
    sorted_teams = sorted(team_stats.items(), key=lambda x: (x[1]['wins']*3 + x[1]['draws'], x[1]['scored'] - x[1]['conceded']), reverse=True)
    for team, stats in sorted_teams:
        points = stats['wins']*3 + stats['draws']
        goals = f'{stats["scored"]}-{stats["conceded"]}'
        print(f'{team:<20} {points:<7} {goals:<9} {stats["wins"]:<5} {stats["draws"]:<6} {stats["losses"]:<6}')

# Function for printing the top scorers table
def print_top_scorers():
    print('Top scorers:')
    print(f'{"Player":<20} {"Goals":<5}')
    print('-' * 27)  # Print a dividing line for clarity
    # Sorting players by the number of goals
    sorted_scorers = sorted(player_stats.items(), key=lambda x: x[1], reverse=True)
    for player, goals in sorted_scorers:
        print(f'{player:<20} {goals:<5}')


def main():
    # Load existing matches and update statistics
    existing_matches = load_data()
    for match in existing_matches:
        team1, team2 = match['team1'], match['team2']
        goals_team1, goals_team2 = map(int, match['result'].split(':'))
        scorers = match['scorers']
        update_team_stats(team1, team2, goals_team1, goals_team2)
        update_player_stats(scorers)

    # Main application loop
    done = False
    while not done:
        print("\nAvailable actions: [1] Add match, [2] Show league table, [3] Show top scorers, [4] Exit")
        action = input("Select an action (1-4): ")

        if action == '1':
            add_match()
        elif action == '2':
            print_league_table()
        elif action == '3':
            print_top_scorers()
        elif action == '4':
            print("Exiting application...")
            done = True
        else:
            print("Invalid action, please choose again.")

if __name__ == "__main__":
    main()

# EoF