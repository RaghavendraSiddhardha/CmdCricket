import sys
from classes import Player, Team
from tabulate import tabulate
import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_positive_integer(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = input(prompt)
            if not value.isnumeric():
                raise ValueError("Input must be a number.")
            value = int(value)
            if min_val is not None and value < min_val:
                raise ValueError(f"Input must be at least {min_val}.")
            if max_val is not None and value > max_val:
                raise ValueError(f"Input must be at most {max_val}.")
            return value
        except ValueError as ve:
            print(Fore.RED + f"Invalid input: {ve}")

def initialize_team(players_count):
    team = Team()
    for c in range(1, players_count + 1):
        while True:
            name = input(f"Enter player no {c} name: ").strip().capitalize()
            if name:
                team.add_player(name)
                break
            else:
                print(Fore.RED + "Player name cannot be empty. Please enter a valid name.")
    return team

def display_score(team, Target):
    print(Fore.GREEN + f"Your Score: {team.score}-{team.wickets_lost}     Runs Required: {Target - team.score}")

def display_final_results(team, Target,balls):
    if team.score == Target:
        print(Fore.GREEN + "You Won!")
        print(f"Final Score: {team.score}-{team.wickets_lost}")
    elif team.score == Target-1:
        print(Fore.YELLOW + "Match Tied")
    else:
        print(Fore.RED + f"Match Lost by {Target - team.score - 1 } runs")

from colorama import Fore
from tabulate import tabulate

def display_player_stats(team):
    # Define the table header
    data = [["Name", "Runs", "Balls", "Fours", "Sixes", "Strike Rate"]]
    
    # Initialize totals
    total_runs = 0
    total_balls = 0
    total_fours = 0
    total_sixes = 0
    
    # Prepare player data
    for player in team.players_list:
        row = []
        # Use color for different statuses
        if player.name not in team.out_list and player.balls_played > 0:
            row.append(f"{Fore.GREEN}{player.name}*{Fore.RESET}")  # Active player
        elif player.balls_played > 0:
            row.append(f"{Fore.RED}{player.name} (OUT){Fore.RESET}")  # Out player
        else:
            row.append(f"{Fore.YELLOW}{player.name} (DNB){Fore.RESET}")  # Did not bat
        
        # Append player stats
        row.extend([
            player.runs,
            player.balls_played,
            player.fours,
            player.sixes,
            round(player.get_strike_rate(), 2) if player.balls_played > 0 else 0.00
        ])
        
        # Update totals
        total_runs += player.runs
        total_balls += player.balls_played
        total_fours += player.fours
        total_sixes += player.sixes
        
        data.append(row)

    # Add a totals row
    total_row = [
        "Total",
        f"{total_runs}-{len(team.out_list)}",
        f"{int(total_balls/6)}.{total_balls%6} overs",
        total_fours,
        total_sixes,
        round(total_runs / total_balls * 100, 2) if total_balls > 0 else 0.00  # Total Strike Rate
    ]
    data.append(total_row)

    # Print the table with better formatting
    print("\n")
    print("Scorecard")
    print(tabulate(data, headers='firstrow', tablefmt='grid', stralign='center'))



def calculate_wicket_probability(run, difficulty):
    base_probability = 0.08 * difficulty  # Base probability for a dot ball

    if run == 0:
        return base_probability  # Dot ball, use base probability
    elif 1 <= run <= 3:
        return base_probability + 0.01 * run  # Small increase for 1-3 runs
    elif run == 4 :
        return base_probability + 0.05  # Larger increase for boundaries
    elif run == 5:
        return base_probability + 0.10
    elif run == 6:
        return base_probability + 0.15
    else:
        # For runs greater than maximum (e.g., > 6), this can be adjusted based on gameplay
        return base_probability + 0.1  # Significant increase for high runs

def main():
    try:
        print(Fore.CYAN + "Welcome to the Command-Line Cricket Game!\n")
        balls_input = get_positive_integer(Fore.YELLOW + "Enter No of overs: ", min_val=1)
        players = get_positive_integer(Fore.YELLOW + "Enter No of Players (2-11): ", min_val=2, max_val=11)
        difficulty = get_positive_integer(Fore.YELLOW + "Enter difficulty level (1-5): ", min_val=1, max_val=5)

        total_balls = 6 * balls_input
        team = initialize_team(players)

        # Set target based on difficulty
        min_target = int(total_balls * (difficulty * 0.5 + 0.5))
        max_target = int(total_balls * (difficulty * 0.5 + 1))
        Target = random.randint(min_target, max_target)
        print(Fore.GREEN + f"\nYour Target: {Target}\n")

        while total_balls > 0 and team.wickets_lost < players - 1:
            team.Total_bp += 1
            team.players_list[team.striker].balls_played += 1
            current_over = team.Total_bp // 6
            current_ball = team.Total_bp % 6
            
            print(Fore.YELLOW + f"\nOver {current_over}.{current_ball} | {team.players_list[team.striker].name} is on strike")

            try:
                run = int(input(Fore.WHITE + "Enter run (0-6): "))
                if run < 0 or run > 6:
                    raise ValueError("Run must be between 0 and 6.")
            except ValueError as ve:
                print(Fore.RED + f"Invalid input: {ve}")
                # Handle potential wicket based on difficulty
                team.handle_invalid_run(difficulty)
                total_balls -= 1
                continue

            # Calculate wicket probability
            wicket_probability = calculate_wicket_probability(run, difficulty)

            # Determine if it's a wicket based on run and randomness
            if random.random() < wicket_probability:
                print(Fore.RED + f"WICKET! {team.players_list[team.striker].name} is out.")
                team.out()
            else:
                team.update_score(run)
                if run % 2 != 0:
                    team.swap()
            
            # End of over
            if team.Total_bp % 6 == 0:
                team.swap()
                print(Fore.YELLOW + f"\nEnd of over {current_over + 1} | Runs Scored in this over: {team.ovr}")
                team.ovr = 0

            # Display score and rates
            display_score(team, Target)
            total_balls -= 1

            # Current Run Rate and Required Run Rate
            crr = round(team.score * 6 / team.Total_bp, 2) if team.Total_bp > 0 else 0
            rrr = round((Target - team.score) * 6 / total_balls, 2) if total_balls > 0 else 0
            
            # Print rates only once at the end of each ball
            print(Fore.MAGENTA + f"CRR: {crr} | RRR: {rrr}")

            # Check for win
            if team.score >= Target:
                display_final_results(team, Target,total_balls)
                break

        else:
            # If loop exits without break, match is either lost or tied
            display_final_results(team, Target,total_balls)

        display_player_stats(team)

    except KeyboardInterrupt:
        print(Fore.RED + "\nGame interrupted by user. Exiting...")
        sys.exit()

if __name__ == "__main__":
    main()