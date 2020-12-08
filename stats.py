import json

class Stats:

    def __init__(self, game=None):

        self.game = game;

        self.stats_file_path = "stats.json";

        self.n_game = 0;
        self.n_scrabble = 0;
        self.time_played = 0;
        self.n_placed_word = 0;
        self.n_placed_letter = 0;

        self.l_player_stats = {};

    def load(self):

        file_stats = open(self.stats_file_path, "r");
        data_string = file_stats.read();

        file_stats.close();

        data_stats = json.loads(data_string);
        self.n_game = data_stats["n_game"];
        self.n_scrabble = data_stats["n_scrabble"];
        self.time_played = data_stats["time_played"];
        self.n_letter_placed = data_stats["n_placed_letter"];
        self.n_placed_word = data_stats["n_placed_word"];

        l_player_stats = data_stats["l_player_stats"];
        for (player_name, player_stats) in l_player_stats.items():

            l_player_stats[player_name]["n_win"] = player_stats["n_win"];
            l_player_stats[player_name]["n_lose"] = player_stats["n_lose"];
            l_player_stats[player_name]["n_scrabble"] = player_stats["n_scrabble"];
            l_player_stats[player_name]["time_played"] = player_stats["time_played"];
            l_player_stats[player_name]["n_placed_letter"] = player_stats["n_placed_letter"];
            l_player_stats[player_name]["n_placed_word"] = player_stats["n_placed_word"];
            l_player_stats[player_name]["score_earned"] = player_stats["score_earned"];


        file_stats = open(self.stats_file_path, "r");
        json.dump(data_stats, file_stats);

        file_stats.close();


    def save(self):

        file_stats = open(self.stats_file_path, "r");
        data_string = file_stats.read();

        file_stats.close();

        data_stats = json.loads(data_string);
        data_stats["n_game"] = self.n_game;
        data_stats["n_scrabble"] = self.n_scrabble;
        data_stats["time_played"] = self.time_played;
        data_stats["n_placed_word"] = self.n_placed_word;
        data_stats["n_placed_letter"] = self.n_placed_letter;

        l_player_stats = data_stats["l_player_stats"];
        for (player_name, player_stats) in l_player_stats.items():

            player_stats["n_win"] = l_player_stats[player_name]["n_win"];
            player_stats["n_lose"] = l_player_stats[player_name]["n_lose"];
            player_stats["n_scrabble"] = l_player_stats[player_name]["n_scrabble"];
            player_stats["time_played"] = l_player_stats[player_name]["time_played"];
            player_stats["n_placed_letter"] = l_player_stats[player_name]["n_placed_letter"];
            player_stats["n_placed_word"] = l_player_stats[player_name]["n_placed_word"];
            player_stats["score_earned"] = l_player_stats[player_name]["score_earned"];


        file_stats = open(self.stats_file_path, "r");
        json.dump(data_stats, file_stats);

        file_stats.close();

    def get_l_player(self):
        pass;

    def reset_all(self):
        pass;

    def reset_player(self, player_name):
        pass;


    def get_player_stats(self, player_name):
        pass;

    def set_game_instance(self, game):
        self.game_ = game;
