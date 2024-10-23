class Player:
    def __init__(self, name):
        self.name = name
        self.runs = 0
        self.fours = 0
        self.sixes = 0
        self.balls_played = 0
        self.chance = 1  # For handling warnings

    def get_strike_rate(self):
        return (self.runs / self.balls_played) * 100 if self.balls_played > 0 else 0.0


class Team:
    def __init__(self):
        self.score = 0
        self.striker = 0
        self.non_striker = 1
        self.wickets_lost = 0
        self.players = 0
        self.Total_bp = 0  # Total balls played
        self.ovr = 0  # Runs in current over
        self.players_list = []
        self.out_list = []

    def add_player(self, name):
        self.players_list.append(Player(name))
        self.players += 1

    def swap(self):
        self.striker, self.non_striker = self.non_striker, self.striker

    def out(self):
        out_player = self.players_list[self.striker]
        print(f"{out_player.name} is out for {out_player.runs} ({out_player.balls_played} balls)")
        self.out_list.append(out_player.name)
        self.wickets_lost += 1
        if self.wickets_lost >= len(self.players_list) - 1:
            print("\nAll out")
            return
        self.striker = self.wickets_lost + 1
        if self.striker >= len(self.players_list):
            print("No more players left to bat.")
            return
        print(f"Next Batsman: {self.players_list[self.striker].name}")

    def handle_invalid_run(self, difficulty):
        # Handle invalid run input as a potential wicket based on difficulty
        player = self.players_list[self.striker]
        if player.chance > 0:
            player.chance -= 1
            print("Invalid run entered! This is the final warning.")
        else:
            print(f"{player.name} is out due to invalid input.")
            self.out()

    def update_score(self, run):
        self.score += run
        self.ovr += run
        player = self.players_list[self.striker]
        player.runs += run
        if run == 4:
            player.fours += 1
        elif run == 6:
            player.sixes += 1
