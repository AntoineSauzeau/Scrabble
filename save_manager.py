import json
from datetime import datetime

from player import Player

class SaveManager:
    """
        Provides functions to load and save games
    """

    def __init__(self, game=None):

        self.game = game;

        self.save_file_path = "save.json";

    def load_save(self, save_name):
        """
            Recovers the saved data and loads the game, i.e. it uses them
            to put the game instance as it was when it was saved.
        """

        try:
            file_save = open(self.save_file_path, "r");
            data_string = file_save.read();
        except FileNotFoundError:
            data_string = "{}";

        file_save.close();

        data_all_save = json.loads(data_string);
        data_save = data_all_save[save_name];

        self.game.set_played_time(data_save["played_time"]);
        self.game.set_n_round(data_save["n_round"]);
        self.game.set_player_index(data_save["player_index"]);
        self.game.set_game_board(data_save["game_board"]);
        self.game.set_l_joker_pos(data_save["l_joker_pos"]);
        self.game.set_stack(data_save["stack"]);
        self.game.set_l_case_modified_during_round(data_save["l_case_modified_during_round"]);
        self.game.set_l_case_bonus_covered(data_save["l_case_bonus_covered"]);
        self.game.set_n_placed_letter(data_save["n_placed_letter"]);
        self.game.set_n_placed_word(data_save["n_placed_word"]);
        self.game.set_n_scrabble(data_save["n_scrabble"]);


        l_player = [];
        data_l_player = data_save["l_player"];
        for data_player in data_l_player:

            player = Player();
            player.set_name(data_player["name"]);
            player.set_score(data_player["score"]);
            player.set_n_placed_letter(data_save["n_placed_letter"]);
            player.set_n_placed_word(data_save["n_placed_word"]);
            player.set_n_scrabble(data_save["n_scrabble"]);

            easel = player.get_easel();
            easel_data = data_player["easel"];

            easel.set_l_letter(easel_data["l_letter"]);

            l_player.append(player);

        self.game.set_l_player(l_player);

        self.game.set_game_taken_up(True);
        self.game.load_game();

    def create_save(self):
        """
            Creates a backup of a game from its game instance
        """

        date = datetime.today();

        try:
            file_save = open(self.save_file_path, "r");
            data_string = file_save.read();
        except FileNotFoundError:
            data_string = "{}";

        file_save.close();

        data_all_save = json.loads(data_string);
        data_save = {}

        game = self.game;
        data_save["played_time"] = game.get_played_time();
        data_save["n_round"] = game.get_n_round();
        data_save["player_index"] = game.get_player_index();
        data_save["game_board"] = game.get_game_board();
        data_save["l_joker_pos"] = game.get_l_joker_pos();
        data_save["stack"] = game.get_stack();
        data_save["l_case_modified_during_round"] = game.get_l_case_modified_during_round();
        data_save["l_case_bonus_covered"] = game.get_l_case_bonus_covered();
        data_save["n_placed_letter"] = game.get_n_placed_letter();
        data_save["n_placed_word"] = game.get_n_placed_word();
        data_save["n_scrabble"] = game.get_n_scrabble();

        data_save["l_player"] = [];
        for player in game.get_l_player():

            player_data = {};

            player_data["name"] = player.get_name();
            player_data["score"] = player.get_score();
            player_data["n_placed_letter"] = player.get_n_placed_letter();
            player_data["n_placed_word"] = player.get_n_placed_word();
            player_data["n_scrabble"] = player.get_n_scrabble();

            easel = player.get_easel();
            easel_data = {};
            easel_data["l_letter"] = easel.get_l_letter();

            player_data["easel"] = easel_data;

            data_save["l_player"].append(player_data);

        save_name = str(date.now());
        save_name = save_name[:19];

        data_all_save[save_name] = data_save;

        file_save = open(self.save_file_path, "w");
        json.dump(data_all_save, file_save);

        file_save.close();

    def remove_save(self, save_name):
        """
            Remove a backup in backup file
        """

        try:
            file_save = open(self.save_file_path, "r");
            data_string = file_save.read();
        except FileNotFoundError:
            data_string = "{}";

        file_save.close();

        data_all_save = json.loads(data_string);
        data_all_save.pop(save_name);

        file_save = open(self.save_file_path, "w");
        json.dump(data_all_save, file_save);

        file_save.close();

    def reset(self):
        """
            Deletes all backups
        """

        file_save = open(self.save_file_path, "w");
        file_save.write("{}");


    def get_l_save_name(self):
        """
            Returns the names of all players who have data saved in the backup file
        """

        l_save_name = [];

        try:
            file_save = open(self.save_file_path, "r");
            data_string = file_save.read();
        except FileNotFoundError:
            data_string = "{}";

        data_all_save = json.loads(data_string);
        for save in data_all_save.items():

            save_name = save[0];
            l_save_name.append(save_name);

        l_save_name.reverse();

        return l_save_name;



    #GETTERS/SETTERS
    def set_game_instance(self, game):
        self.game = game;
