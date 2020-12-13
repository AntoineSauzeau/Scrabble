import json

class Stats:

    def __init__(self, game=None):

        self.game = game;

        self.stats_file_path = "stats.json";

        self.l_global_stats = {};
        self.l_global_stats["n_game"] = 0;
        self.l_global_stats["n_scrabble"] = 0;
        self.l_global_stats["time_played"] = 0;
        self.l_global_stats["n_placed_word"] = 0;
        self.l_global_stats["n_placed_letter"] = 0;

        self.l_player_stats = {};

    def load(self):

        file_stats = open(self.stats_file_path, "r");
        data_string = file_stats.read();

        file_stats.close();

        data_stats = json.loads(data_string);

        if(len(data_stats["l_global_stats"]) != 0):
            self.l_global_stats = data_stats["l_global_stats"];

        l_player_data = data_stats["l_player_stats"];
        if(len(l_player_data) != 0):

            for player_name, player_stats in l_player_data.items():

                self.init_player_stats(player_name);

                #self.l_player_stats[player_name] = {};
                self.l_player_stats[player_name]["n_win"] = player_stats["n_win"];
                self.l_player_stats[player_name]["n_lose"] = player_stats["n_lose"];
                self.l_player_stats[player_name]["n_scrabble"] = player_stats["n_scrabble"];
                self.l_player_stats[player_name]["time_played"] = player_stats["time_played"];
                self.l_player_stats[player_name]["n_placed_word"] = player_stats["n_placed_word"];
                self.l_player_stats[player_name]["n_placed_letter"] = player_stats["n_placed_letter"];


        if(self.game != None):

            l_game_player = self.game.get_l_player();
            for player in l_game_player:

                player_name = player.get_name();
                if(not(player_name in self.l_player_stats)):

                    self.init_player_stats(player_name);

    def init_player_stats(self, player_name):

        self.l_player_stats[player_name] = {};
        self.l_player_stats[player_name]["n_win"] = 0;
        self.l_player_stats[player_name]["n_lose"] = 0;
        self.l_player_stats[player_name]["n_scrabble"] = 0;
        self.l_player_stats[player_name]["time_played"] = 0;
        self.l_player_stats[player_name]["n_placed_word"] = 0;
        self.l_player_stats[player_name]["n_placed_letter"] = 0;

    def save(self):

        file_stats = open(self.stats_file_path, "r");
        data_string = file_stats.read();

        file_stats.close();

        data_stats = json.loads(data_string);

        data_stats["l_global_stats"] = self.l_global_stats;
        data_stats["l_player_stats"] = self.l_player_stats;

        file_stats = open(self.stats_file_path, "w");
        json.dump(data_stats, file_stats);

        file_stats.close();

    def get_l_player_name(self):
        return list(self.l_player_stats.keys());


    def reset(self):

        data_stats = {};
        data_stats["l_global_stats"] = {};
        data_stats["l_player_stats"] = {};

        file_stats = open(self.stats_file_path, "w");
        json.dump(data_stats, file_stats);

        file_stats.close();

        self.load();


    def get_player_stats(self, player_name):
        pass;

    def get_l_global_stats(self):
        return self.l_global_stats;

    def get_l_player_stats(self):
        return self.l_player_stats;

    def set_game_instance(self, game):
        self.game = game;
