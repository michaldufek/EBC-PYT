import json

# Define a class for team statistics
class TeamStats:
    def __init__(self):
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.scored = 0
        self.conceded = 0

# Define a class for managing matches and statistics
class MatchManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.team_stats = {}
        self.player_stats = {}

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_data(self, data):
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def add_match(self, date, team1, team2, result, scorers):
        goals_team1, goals_team2 = map(int, result.split(':'))
        self.update_team_stats(team1, team2, goals_team1, goals_team2)
        self.update_player_stats(scorers)
        match = {'date': date, 'team1': team1, 'team2': team2, 'result': result, 'scorers': scorers}
        matches = self.load_data()
        matches.append(match)
        self.save_data(matches)
        print('Match successfully added.')

    def update_team_stats(self, team1, team2, goals_team1, goals_team2):
        # Ensure team records exist
        if team1 not in self.team_stats:
            self.team_stats[team1] = TeamStats()
        if team2 not in self.team_stats:
            self.team_stats[team2] = TeamStats()

        self.team_stats[team1].scored += goals_team1
        self.team_stats[team1].conceded += goals_team2
        self.team_stats[team2].scored += goals_team2
        self.team_stats[team2].conceded += goals_team1

        if goals_team1 > goals_team2:
            self.team_stats[team1].wins += 1
            self.team_stats[team2].losses += 1
        elif goals_team1 < goals_team2:
            self.team_stats[team2].wins += 1
            self.team_stats[team1].losses += 1
        else:
            self.team_stats[team1].draws += 1
            self.team_stats[team2].draws += 1

    def update_player_stats(self, scorers):
        if scorers.strip():
            for scorer_info in scorers.split(','):
                name, goals = scorer_info.strip().rsplit(' ', 1)
                if name not in self.player_stats:
                    self.player_stats[name] = 0
                self.player_stats[name] += int(goals)

    def print_league_table(self):
        print('League Table:')
        print(f'{"Team":<20} {"Points":<7} {"Goals":<9} {"Wins":<5} {"Draws":<6} {"Losses":<6}')
        print('-' * 60)
        sorted_teams = sorted(self.team_stats.items(), key=lambda x: (x[1].wins * 3 + x[1].draws, x[1].scored - x[1].conceded), reverse=True)
        for team, stats in sorted_teams:
            points = stats.wins * 3 + stats.draws
            goals = f'{stats.scored}-{stats.conceded}'
            print(f'{team:<20} {points:<7} {goals:<9} {stats.wins:<5} {stats.draws:<6} {stats.losses:<6}')

    def print_top_scorers(self):
        print('Top Scorers:')
        print(f'{"Player":<20} {"Goals":<5}')
        print('-' * 27)
        sorted_scorers = sorted(self.player_stats.items(), key=lambda x: x[1], reverse=True)
        for player, goals in sorted_scorers:
            print(f'{player:<20} {goals:<5}')

def main():
    manager = MatchManager('matches.json')
    existing_matches = manager.load_data()
    for match in existing_matches:
        manager.update_team_stats(match['team1'], match['team2'], *map(int, match['result'].split(':')))
        manager.update_player_stats(match['scorers'])

    done = False
    while not done:
        print("\nAvailable actions: [1] Add match, [2] Show league table, [3] Show top scorers, [4] Exit")
        action = input("Select an action (1-4): ")

        if action == '1':
            date = input('Match date (DD.MM.YYYY): ')
            team1 = input('Home team: ')
            team2 = input('Away team: ')
            result = input('Result (home goals:away goals): ')
            scorers = input('Scorers (player name and number of goals, separated by a comma): ')
            manager.add_match(date, team1, team2, result, scorers)
        elif action == '2':
            manager.print_league_table()
        elif action == '3':
            manager.print_top_scorers()
        elif action == '4':
            print("Exiting application...")
            done = True
        else:
            print("Invalid action, please choose again.")

if __name__ == "__main__":
    main()
