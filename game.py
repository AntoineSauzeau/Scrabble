from enum import IntEnum
import threading

class GameStatus(IntEnum):
    NotStarted = 0,
    InProgress = 1,
    Paused = 2,
    Finished = 3

class Game():

    l_case_WT = [[0,0],[0,7],[0,14],[7,0],[7,14],[14,0],[14,7],[14,14]]
    l_case_WD = [[1,1],[1,13],[2,2],[2,12],[3,3],[3,11],[4,4],[4,10],[7,7],[10,4],[10,10],[11,3],[11,11],[12,2],[12,12],[13,1],[13,13]]
    l_case_LT = [[1,5],[1,9],[5,1],[5,5],[5,9],[5,13],[9,1],[9,5],[9,9],[9,13],[13,5],[13,9]]
    l_case_LD = [[0,3],[0,11],[2,6],[2,8],[3,0],[3,7],[3,14],[6,2],[6,6],[6,8],[6,12],[7,3],[7,11],[8,2],[8,6],[8,8],[8,12],[11,0],[11,7],[11,14],[12,6],[12,8],[14,3],[14,11]]

    played_time = 0;   #En seconde
    player_turn = None;
    game_status = GameStatus.NotStarted;

    def __init__(self, l_player):

        self.l_player = l_player

    def start_game(self):
        self.game_status = GameStatus.InProgress;
        self.player_turn = self.l_player[0];

        self.loop_timer();

    def loop_timer(self):
        self.played_time += 1;

        if(self.game_status == GameStatus.Paused or self.game_status == GameStatus.Finished):
            return;

        timer = threading.Timer(1, self.loop_timer, args = None, kwargs = None);
        timer.start();

    def get_l_player(self):
        return self.l_player;

    def get_played_time_formatted(self):

        second = self.played_time;
        minute = 0;
        hour = 0;

        if(second // 3600):
            hour = second // 3600;
            second -= hour * 3600;

        if(second // 60):
            minute = second // 60;
            second -= minute * 60;

        if(second < 10):
            second_text = "0" + str(second);
        else:
            second_text = str(second);

        if(minute < 10):
            minute_text = "0" + str(minute);
        else:
            minute_text = str(minute);

        if(hour < 10):
            hour_text = "0" + str(hour);
        else:
            hour_text = str(hour);

        played_time_formatted = hour_text + ":" + minute_text + ":" + second_text;

        return played_time_formatted;

    def get_player_turn(self):
        return self.player_turn;

    def get_game_status(self):
        return self.game_status;

    def set_player_turn(player):
        self.player_turn = player;
