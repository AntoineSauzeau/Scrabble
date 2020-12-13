import json

class Settings:

    def __init__(self):

        self.settings_file_path = "settings.json";

        file_settings = open(self.settings_file_path, "r");
        data_string = file_settings.read();

        file_settings.close();

        self.settings = json.loads(data_string);


    def save(self):

        file_settings = open(self.settings_file_path, "w");
        json.dump(self.settings, file_settings);

        file_settings.close();


    def get_l_settings(self):
        return self.settings;
