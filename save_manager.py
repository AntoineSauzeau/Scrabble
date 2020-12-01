import json
from datetime import datetime

class SaveManager:

    def __init__(self, game=None):

        self.game = game;

        self.save_file_path = "save.json";

    def load_save(self, save_name):
        pass;

    def create_save(self):

        date = datetime.today();

        file_save = open(self.save_file_path, "r");
        data_string = file_save.read();

        file_save.close();

        data_all_save = json.loads(data_string);
        data_save = {}

        game = self.game;
        data_save["played_time"] = game.get_played_time();
        data_save["n_round"] = game.get_n_round();
        data_save["player_index"] = game.get_player_index();
        data_save["game_status"] = game.get_game_status();
        data_save["game_board"] = game.get_game_board();

        save_name = str(date.now());
        data_all_save[save_name] = data_save;

        file_save = open(self.save_file_path, "w");
        json.dump(data_all_save, file_save);

        file_save.close();

    def get_l_save_name(self):

        l_save_name = [];

        file_save = open(self.save_file_path, "r");
        data_string = file_save.read();

        data_all_save = json.loads(data_string);
        for save in data_all_save.items():

            save_name = save[0];
            l_save_name.append(save_name);

        return l_save_name;

    def set_game_instance(self, game):
        self.game = game;
