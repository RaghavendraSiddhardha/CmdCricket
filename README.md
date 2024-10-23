# CmdCricket
CmdCricket is a command-line cricket game where players chase a target score by batting through overs. Customize the number of players, overs, and difficulty. The game features scoring, strike rate calculations, and random wickets, providing a fun and challenging cricket experience in your terminal!
Command-Line Cricket Game
Overview
This is a simple command-line cricket game where players can simulate a cricket match by entering overs, the number of players, and difficulty level. The objective is to chase down a target score set by the game within a limited number of balls. The game will guide you through each ball of the innings and keep track of scores, wickets, and other match statistics.

Features
Set overs, number of players, and difficulty level.
Chase a randomly generated target.
Keep track of player statistics (runs, balls faced, boundaries, strike rate).
Real-time score updates and match summary.
Use of tabulate for pretty output.
Requirements
Python 3.x
Install required libraries:
bash
Copy code
pip install tabulate
How to Play
Clone the repository:

bash
Copy code
git clone https://github.com/YOUR_USERNAME/cricket-cmd-game.git
cd cricket-cmd-game
Run the game:

bash
Copy code
python main.py
Follow the on-screen prompts to enter the number of overs, players, and difficulty level (1-5).

Enter the number of runs scored on each ball.

The game will keep track of the score and wickets, and declare if you win, lose, or tie the match.

Game Instructions
The player starts by selecting the number of overs, players, and difficulty level.
The target score is randomly generated based on difficulty.
On each ball, the player must enter the number of runs (between 0-6).
The game keeps track of runs scored, wickets lost, and overs bowled.
The objective is to chase the target score before running out of balls or players.
Example
mathematica
Copy code
Enter No of overs: 2
Enter No of Players(>1): 3
Enter difficulty level(1-5): 2

Your Target:  20

Over 0.1
Player 1 is on strike
Enter run(0-6): 4
Your Score 4-0     Runs Required: 16
CRR-4.0 RRR-5.33
...
Code Structure
main.py: Contains the game logic and user interaction.
classes.py: Defines the Player and Team classes to manage player stats and team functionality.
