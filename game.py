from enum import IntEnum
import threading
import random
import pdb
from player import Player
from word_checker import WordChecker

class GameStatus(IntEnum):
    NotStarted = 0,
    InProgress = 1,
    Paused = 2,
    Finished = 3

class CaseType(IntEnum):
    WT = 0,
    WD = 1,
    LT = 2,
    LD = 3

class Game():

    def __init__(self, l_player):

        self.l_player = l_player

        self.l_case_WT = [[0,0],[0,7],[0,14],[7,0],[7,14],[14,0],[14,7],[14,14]]
        self.l_case_WD = [[1,1],[1,13],[2,2],[2,12],[3,3],[3,11],[4,4],[4,10],[7,7],[10,4],[10,10],[11,3],[11,11],[12,2],[12,12],[13,1],[13,13]]
        self.l_case_LT = [[1,5],[1,9],[5,1],[5,5],[5,9],[5,13],[9,1],[9,5],[9,9],[9,13],[13,5],[13,9]]
        self.l_case_LD = [[0,3],[0,11],[2,6],[2,8],[3,0],[3,7],[3,14],[6,2],[6,6],[6,8],[6,12],[7,3],[7,11],[8,2],[8,6],[8,8],[8,12],[11,0],[11,7],[11,14],[12,6],[12,8],[14,3],[14,11]]

        self.l_case_bonus_covered = [];
        self.l_easel_case_to_renew = [];

        self.played_time = 0;   #En seconde
        self.n_round = 1;
        self.player_index = 0;            #Stocke l'utilisateur qui joue
        self.game_status = GameStatus.NotStarted;

        self.game_board = [];       #Liste à 2 dimensions représentant le placement des lettres sur le plateau de jeu
        self.stack = [];
        self.l_letter_information = {};

        self.first_letter = True;
        self.l_case_modified_during_round = [];
        self.word_checker = WordChecker(self);

        for player in l_player:
            player.set_game_instance(self);

        #On initialise les 225 cases du plateau à -1
        for x in range(15):

            x_list = [];
            for y in range(15):
                x_list.append(-1);

            self.game_board.append(x_list);

        self.init_l_letter_information();
        self.init_stack();


    def start_game(self):
        self.game_status = GameStatus.InProgress;

        for player in self.l_player:
            player.set_game_instance(self);

        for player in self.l_player:
            easel = player.get_easel();
            easel.fill();

        self.loop_timer();

    def loop_timer(self):
        self.played_time += 1;

        if(self.game_status == GameStatus.Paused or self.game_status == GameStatus.Finished):
            return;

        timer = threading.Timer(1, self.loop_timer);
        timer.start();

    def add_letter_to_game_board(self, case_x, case_y, letter_index):

        if(self.game_status == GameStatus.Paused or self.game_status == GameStatus.Finished):
            return False;

        if(not(self.is_valid_case_for_play(case_x, case_y))):
            return False;


        #Si il y a une déjà une lettre on vérifie qu'elle n'a pas été posé pendant un autre tour
        if(self.game_board[case_x][case_y] != -1):

            if(len(self.l_case_modified_during_round) == 0):
                return False;

            for i in range(len(self.l_case_modified_during_round)):

                case_modified = self.l_case_modified_during_round[i];
                if(case_modified[0] == case_x and case_modified[1] == case_y):

                    player = self.get_player_turn();
                    player_easel = player.get_easel();

                    i_first_free_place_easel = player_easel.get_first_free_place();
                    l_letter_easel = player_easel.get_l_letter();

                    #On remet la lettre déjà sur la case dans le chevalet pour la remplacer par la nouvelle lettre
                    l_letter_easel[i_first_free_place_easel] = self.game_board[case_x][case_y];

                    break;

                if(i == len(self.l_case_modified_during_round)-1):
                    return False;


        self.game_board[case_x][case_y] = letter_index;

        if(not((case_x, case_y) in self.l_case_modified_during_round)):
            self.l_case_modified_during_round.append((case_x, case_y));

        self.first_letter = False;

        return True;

    def remove_letter_on_game_board(self, l_letter_pos):

        for letter_pos in l_letter_pos:
            letter_x = letter_pos[0];
            letter_y = letter_pos[1];

            self.game_board[letter_x][letter_y] = -1;

        if(self.game_board[7][7] == -1):
            self.first_letter = True;


    def next_round(self):

        self.n_round += 1;
        player = self.l_player[self.player_index];

        if(len(self.l_case_modified_during_round) != 0):

            print(self.word_checker.is_valid_word());

            if(self.word_checker.is_valid_word()):
                total_value_placed = self.word_checker.count_total_placed_value();
                self.desactivate_covered_bonus();

                player.add_score(total_value_placed);

            else:
                self.remove_letter_on_game_board(self.l_case_modified_during_round);

        for case_index in self.l_easel_case_to_renew:
            easel = player.get_easel();
            easel.renew_letter(case_index);

        self.l_easel_case_to_renew.clear();

        self.l_case_modified_during_round.clear();
        easel = player.get_easel();
        easel.fill();

        if(self.player_index+1 == len(self.l_player)):
            self.player_index = 0;
        else:
            self.player_index += 1;


    def init_l_letter_information(self):

        self.l_letter_information["A"] = {"occ": 9, "val": 1}
        self.l_letter_information["B"] = {"occ": 2, "val": 3}
        self.l_letter_information["C"] = {"occ": 2, "val": 3}
        self.l_letter_information["D"] = {"occ": 3, "val": 2}
        self.l_letter_information["E"] = {"occ": 15, "val": 1}
        self.l_letter_information["F"] = {"occ": 2, "val": 4}
        self.l_letter_information["G"] = {"occ": 2, "val": 2}
        self.l_letter_information["H"] = {"occ": 2, "val": 4}
        self.l_letter_information["I"] = {"occ": 8, "val": 1}
        self.l_letter_information["J"] = {"occ": 1, "val": 8}
        self.l_letter_information["K"] = {"occ": 1, "val": 10}
        self.l_letter_information["L"] = {"occ": 5, "val": 1}
        self.l_letter_information["M"] = {"occ": 3, "val": 2}
        self.l_letter_information["N"] = {"occ": 6, "val": 1}
        self.l_letter_information["O"] = {"occ": 6, "val": 1}
        self.l_letter_information["P"] = {"occ": 2, "val": 3}
        self.l_letter_information["Q"] = {"occ": 1, "val": 8}
        self.l_letter_information["R"] = {"occ": 6, "val": 1}
        self.l_letter_information["S"] = {"occ": 6, "val": 1}
        self.l_letter_information["T"] = {"occ": 6, "val": 1}
        self.l_letter_information["U"] = {"occ": 6, "val": 1}
        self.l_letter_information["V"] = {"occ": 2, "val": 4}
        self.l_letter_information["W"] = {"occ": 1, "val": 10}
        self.l_letter_information["X"] = {"occ": 1, "val": 10}
        self.l_letter_information["Y"] = {"occ": 1, "val": 10}
        self.l_letter_information["Z"] = {"occ": 1, "val": 10}
        self.l_letter_information["?"] = {"occ": 2, "val": 0}

    def init_stack(self):

        for i in range(26):
            letter = chr(65+i);
            letter_information = self.l_letter_information[letter];

            occurence = letter_information["occ"];
            for j in range(occurence):
                self.stack.append(letter);

        joker_occurence = self.l_letter_information["?"]["occ"];
        for i in range(joker_occurence):
            self.stack.append("?");

        random.shuffle(self.stack);

        print(self.stack);

    def pick_a_letter(self):

        letter = self.stack[0];     #La pioche est déjà mélangée dans il suffit de prendre de prendre le 1er index pour avoir une lettre "aléatoire"
        self.stack.pop(0);

        #En attendant d'implémenter les jokers
        if(letter == "?"):
            letter = "A";

        return letter;

    def get_case_type(self, case_x, case_y):

        for case in self.l_case_LT:
            if(case[0] == case_x and case[1] == case_y):
                return CaseType.LT;

        for case in self.l_case_LD:
            if(case[0] == case_x and case[1] == case_y):
                return CaseType.LD;

        for case in self.l_case_WT:
            if(case[0] == case_x and case[1] == case_y):
                return CaseType.WT;

        for case in self.l_case_WD:
            if(case[0] == case_x and case[1] == case_y):
                return CaseType.WD;

    def is_case_bonus(self, case_x, case_y):

        case_type = self.get_case_type(case_x, case_y);

        return (case_type == CaseType.LD or case_type == CaseType.LT or case_type == CaseType.WD or case_type == CaseType.WT);


    #Renvoie True si on peut poser une lettre sur cette case
    def is_valid_case_for_play(self, case_x, case_y):

        #On fait attention à ce que la première lettre soit posé au milieu du plateau
        if(self.first_letter == True):
            if(case_x != 7 or case_y != 7):
                return False;

        print(self.l_case_modified_during_round);

        #Le joueur a le droit de remplacer seulement les lettre posé pendant le tour actuel
        if(self.game_board[case_x][case_y] != -1):
            for i in range(len(self.l_case_modified_during_round)):
                case_modified_pos = self.l_case_modified_during_round[i];

                if(case_x == case_modified_pos[0] and case_y == case_modified_pos[1]):
                    break;

                if(i == len(self.l_case_modified_during_round)-1):
                    return False;

        #On vérifie qu'il y ait bien une lettre sur une des 4 cases autour
        if(not(self.has_letter_around(case_x, case_y)) and self.first_letter != True):
            return False;

        return True;

    def has_letter_around(self, case_x, case_y):

        if(self.game_board[case_x-1][case_y] != -1):
            return True;
        elif(self.game_board[case_x][case_y-1] != -1):
            return True;
        elif(self.game_board[case_x+1][case_y] != -1):
            return True;
        elif(self.game_board[case_x][case_y+1] != -1):
            return True;


    def desactivate_covered_bonus(self):

        for x in range(15):
            for y in range(15):

                if(self.is_case_bonus(x, y)):
                    self.l_case_bonus_covered.append([x, y]);




    #GETTERS/SETTERS
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
        return self.l_player[self.player_index];

    def get_game_status(self):
        return self.game_status;

    def set_player_turn(player):
        self.player_turn = player;

    def set_game_status(self, game_status):
        self.game_status = game_status;

    def get_game_board(self):
        return self.game_board;

    def get_l_case_modified_during_round(self):
        return self.l_case_modified_during_round;

    def get_l_letter_information(self):
        return self.l_letter_information;

    def get_l_easel_case_to_renew(self):
        return self.l_easel_case_to_renew;
