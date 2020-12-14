from enum import IntEnum
import threading
import random

from player import Player
from word_checker import WordChecker
from save_manager import SaveManager
from stats import Stats
from message import Message

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
    """
        Describes a scrabble game
    """

    def __init__(self, l_player=[]):

        #Bonus/Joker
        self.l_case_WT = [[0,0],[0,7],[0,14],[7,0],[7,14],[14,0],[14,7],[14,14]]
        self.l_case_WD = [[1,1],[1,13],[2,2],[2,12],[3,3],[3,11],[4,4],[4,10],[7,7],[10,4],[10,10],[11,3],[11,11],[12,2],[12,12],[13,1],[13,13]]
        self.l_case_LT = [[1,5],[1,9],[5,1],[5,5],[5,9],[5,13],[9,1],[9,5],[9,9],[9,13],[13,5],[13,9]]
        self.l_case_LD = [[0,3],[0,11],[2,6],[2,8],[3,0],[3,7],[3,14],[6,2],[6,6],[6,8],[6,12],[7,3],[7,11],[8,2],[8,6],[8,8],[8,12],[11,0],[11,7],[11,14],[12,6],[12,8],[14,3],[14,11]]

        self.l_case_bonus_covered = [];                 #We store the position of the covered bonus boxes in order not to apply their bonus later.

        self.l_joker_pos = [];

        #Player/Easel
        self.l_easel_case_to_renew = [];
        self.l_player = l_player
        self.player_index = 0;                  #Player who is playing
        self.picking_mode = False;                  #True if the player is in the process of choosing letters to be replaced in his easel by other picked letters

        #Game state
        self.played_time = 0;                   #Time played in seconds
        self.n_round = 1;
        self.game_status = GameStatus.NotStarted;
        self.last_round = False;
        self.game_taken_up = False;                 #True if the game has been loaded from a backup
        self.game_board = [];                   #Represents the game board of 15*15, contains the index in the alphabet of the letters laid down
        self.first_letter = True;                   #True if no letter has been placed on the game board
        self.timer = None;
        self.l_case_modified_during_round = [];                 #List of the positions of the letters placed on the game board during the round

        #Stack
        self.stack = [];
        self.l_letter_information = {};                 #Stores the number of each letter in the initial stack and their value.

        #Stats
        self.n_placed_letter = 0;
        self.n_placed_word = 0;
        self.n_scrabble = 0;

        self.stats = Stats(self);

        if(self.game_taken_up == False):
            self.stats.load();



        self.word_checker = WordChecker(self);
        self.save_manager = SaveManager(self);

        self.game_interface = None;



        for player in l_player:
            player.set_game_instance(self);

        #The 225 squares of the board are initialized at -1, i.e. empty, without letters.
        for x in range(15):

            x_list = [];
            for y in range(15):
                x_list.append(-1);

            self.game_board.append(x_list);

        self.init_l_letter_information();
        self.init_stack();


    def start_game(self):
        """
            Starts the game
        """

        self.game_status = GameStatus.InProgress;

        for player in self.l_player:
            player.set_game_instance(self);

        #We fill the easel of each player
        for player in self.l_player:
            easel = player.get_easel();
            easel.fill();

        #If we have just loaded a game at the launch of the game there may already be a letter of pose so we check
        if(self.game_board[7][7] != -1):
            self.first_letter = False;

        self.loop_timer();

    def loop_timer(self):
        """
            Called by the thread timer callback, it adds 1 second
            to the elapsed time and restarts the timer
        """

        if(self.game_status == GameStatus.Paused or self.game_status == GameStatus.Finished):
            return;

        self.played_time += 1;

        self.timer = threading.Timer(1, self.loop_timer);
        self.timer.daemon = True;
        self.timer.start();

    def start_timer(self):
        """
            Start the timer
        """

        self.timer = threading.Timer(1, self.loop_timer);
        self.timer.daemon = True;
        self.timer.start();

    def stop_timer(self):
        """
            Stop the Timer
        """

        if(self.timer != None):
            self.timer.cancel();

    def add_letter_to_game_board(self, case_x, case_y, letter_index):
        """
            Adds the letter to the coordinates received by parameters
            on the game board if this is allowed
        """

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
        """
            Receive a list of letter positions on the game board and remove them.
        """

        for letter_pos in l_letter_pos:
            letter_x = letter_pos[0];
            letter_y = letter_pos[1];

            self.game_board[letter_x][letter_y] = -1;

        if(self.game_board[7][7] == -1):
            self.first_letter = True;


    def next_round(self):

        if(self.game_status == GameStatus.Finished):
            return;

        self.n_round += 1;
        player = self.l_player[self.player_index];
        player_name = player.get_name();

        if(self.picking_mode):
            self.remove_letter_on_game_board(self.l_case_modified_during_round);
            self.l_case_modified_during_round.clear();
            self.picking_mode = False;

        if(len(self.l_case_modified_during_round) != 0):

            print(self.word_checker.is_valid_word());

            word_placed_with_coord = self.word_checker.get_word_placed();
            word_placed = self.word_checker.word_with_coord_to_string(word_placed_with_coord);

            if(self.word_checker.is_valid_word()):
                total_value_placed = self.word_checker.count_total_placed_value();
                self.desactivate_covered_bonus();

                player.add_score(total_value_placed);

                self.game_interface.show_message_placed_word(word_placed, total_value_placed, player_name);
                if(len(self.l_case_modified_during_round) == 7):
                    self.game_interface.show_message_scrabble(player_name);

                    self.n_scrabble += 1;
                    n_player_scrabble = player.get_n_scrabble();
                    n_player_scrabble += 1;

                self.n_placed_word += 1;
                n_player_placed_word = player.get_n_placed_word();
                player.set_n_placed_word(n_player_placed_word+1);

                self.n_placed_letter += len(self.l_case_modified_during_round);
                n_player_placed_letter = player.get_n_placed_letter();
                player.set_n_placed_letter(n_player_placed_letter+len(self.l_case_modified_during_round));



            else:
                self.remove_letter_on_game_board(self.l_case_modified_during_round);

                self.game_interface.show_message_placed_word(word_placed, 0, player_name);


        l_letter_picked = [];
        for case_index in self.l_easel_case_to_renew:
            easel = player.get_easel();

            letter_index = easel.renew_letter(case_index);
            if(letter_index == None):
                continue;

            if(letter_index != 26):
                letter = chr(65+letter_index);
            else:
                letter = "?";

            l_letter_picked.append(letter);

        if(len(self.l_easel_case_to_renew) != 0):
            if(len(l_letter_picked) != 0):
                print(player_name, l_letter_picked, len(self.stack));
                self.game_interface.show_message_pick_stack(player_name, l_letter_picked, len(self.stack));

        self.l_easel_case_to_renew.clear();

        self.l_case_modified_during_round.clear();
        easel = player.get_easel();
        easel.fill();

        if(len(self.stack) == 0):

            for player in self.l_player:

                player_easel = player.get_easel();
                if(player_easel.empty()):
                    self.end_game();
                    return;



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
        """
            Fill the stack and mix
        """

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
        """
            Picks a letter from the stack and return it
        """

        if(len(self.stack) == 0):
            return None;

        letter = self.stack[0];     #La pioche est déjà mélangée dans il suffit de prendre de prendre le 1er index pour avoir une lettre "aléatoire"
        self.stack.pop(0);

        return letter;

    def get_case_type(self, case_x, case_y):
        """
            Returns the type of the bonus case if there is one, otherwise returns None.
        """

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
        """
            Returns True if the coordinates of the case correspond to those of a bonus case, False if not
        """

        case_type = self.get_case_type(case_x, case_y);

        return (case_type == CaseType.LD or case_type == CaseType.LT or case_type == CaseType.WD or case_type == CaseType.WT);


    def is_valid_case_for_play(self, case_x, case_y):
        """
            Return True if it is allowed to put a letter in this case, False if not.
        """

        #We check that the first letter is well placed in the centre of the game board
        if(self.first_letter == True):
            if(case_x != 7 or case_y != 7):
                return False;

        print(self.l_case_modified_during_round);

        #The player has the right to replace only the letters placed during the current round
        if(self.game_board[case_x][case_y] != -1):
            for i in range(len(self.l_case_modified_during_round)):
                case_modified_pos = self.l_case_modified_during_round[i];

                if(case_x == case_modified_pos[0] and case_y == case_modified_pos[1]):
                    break;

                if(i == len(self.l_case_modified_during_round)-1):
                    return False;

        if(case_x != 7 or case_y != 7):

            #Check that there is a letter in one of the 4 cases around it.
            if(not(self.has_letter_around(case_x, case_y))):
                return False;

        return True;

    def has_letter_around(self, case_x, case_y):
        """
            Returns True if there is at least one letter on one of the 4 cases
            around the case given in parameters, False if this is not the situation
       """

        if(case_x-1 != -1):
            if(self.game_board[case_x-1][case_y] != -1):
                return True;
        if(case_y-1 != -1):
            if(self.game_board[case_x][case_y-1] != -1):
                return True;
        if(case_x+1 != 15):
            if(self.game_board[case_x+1][case_y] != -1):
                return True;
        if(case_y+1 != 15):
            if(self.game_board[case_x][case_y+1] != -1):
                return True;


    def desactivate_covered_bonus(self):

        for x in range(15):
            for y in range(15):

                if(self.is_case_bonus(x, y)):
                    self.l_case_bonus_covered.append([x, y]);

    def save_game(self):
        self.save_manager.create_save();

    #A exécuter après le chargement d'une sauvegarde
    def load_game(self):
        self.stats.load();

    def end_game(self):
        """
            Manages the end of the game, saves statistics, displays the winner, etc.
        """

        self.game_status = GameStatus.Finished;

        #We look at which player has an empty easel to see which one has finished the game.
        finisher_player = None;
        for player in self.l_player:

            easel = player.get_easel();
            if(easel.empty()):
                finisher_player = player;


        #We apply end-of-game maluses and bonuses according to the letters remaining in the easel to the players' scores
        finisher_bonus = 0;
        for player in self.l_player:

            easel = player.get_easel();

            if(finisher_player != player):

                easel_value = easel.count_total_value();
                player_score = player.get_score();

                penalty = easel_value;
                if((player_score - penalty) < 0):
                    player_score = 0;
                else:
                    player_score -= penalty;

                player.set_score(player_score);
                finisher_bonus += easel_value;

        finisher_player.add_score(finisher_bonus);

        #If possible, we pick up the player with the highest score.
        winner = None;
        first_player_score = -1;
        second_player_score = -1;

        for player in self.l_player:

            player_score = player.get_score();

            if(player_score >= first_player_score):
                second_player_score = first_player_score;
                first_player_score = player_score;

                winner = player;

        #We look to see if there is equality
        if(first_player_score == second_player_score):
            winner = None;

        winner_name = winner.get_name();
        self.game_interface.show_message_end_game(winner_name, first_player_score);

        #We save the stats of the game in a file
        global_stats = self.stats.get_l_global_stats();

        global_stats["n_game"] += 1;
        global_stats["n_scrabble"] += self.n_scrabble;
        global_stats["n_placed_letter"] += self.n_placed_letter;
        global_stats["n_placed_word"] += self.n_placed_word;
        global_stats["time_played"] += self.played_time;

        l_player_stats = self.stats.get_l_player_stats();
        for player in self.l_player:

            player_name = player.get_name();
            player_stats = l_player_stats[player_name];

            player_stats["n_scrabble"] += player.get_n_scrabble();
            player_stats["n_placed_letter"] += player.get_n_placed_letter();
            player_stats["n_placed_word"] += player.get_n_placed_word();
            player_stats["time_played"] += self.played_time;

            if(player == winner):
                player_stats["n_win"] += 1;
            else:
                player_stats["n_lose"] += 1;


        self.stats.save();



    #GETTERS/SETTERS
    def get_l_player(self):
        return self.l_player;

    def get_player_turn(self):

        if(self.player_index >= len(self.l_player)):
            return None;

        return self.l_player[self.player_index];

    def get_game_status(self):
        return self.game_status;

    def get_game_board(self):
        return self.game_board;

    def get_l_case_modified_during_round(self):
        return self.l_case_modified_during_round;

    def get_l_letter_information(self):
        return self.l_letter_information;

    def get_l_easel_case_to_renew(self):
        return self.l_easel_case_to_renew;

    def get_played_time(self):
        return self.played_time;

    def get_n_round(self):
        return self.n_round;

    def get_player_index(self):
        return self.player_index;

    def get_stack(self):
        return self.stack;

    def get_first_letter(self):
        return self.first_letter;

    def get_l_case_bonus_covered(self):
        return self.l_case_bonus_covered;

    def get_picking_mode(self):
        return self.picking_mode;

    def get_l_joker_pos(self):
        return self.l_joker_pos;

    def get_game_taken_up(self):
        return self.game_taken_up

    def get_n_placed_letter(self):
        return self.n_placed_letter;

    def get_n_placed_word(self):
        return self.n_placed_word;

    def get_n_scrabble(self):
        return self.n_scrabble;

    def set_game_status(self, game_status):
        self.game_status = game_status;

    def set_game_board(self, game_board):
        self.game_board = game_board;

    def set_l_case_modified_during_round(self, l_case_modified_during_round):
        self.l_case_modified_during_round = l_case_modified_during_round;

    def set_l_letter_information(self, l_letter_information):
        self.l_letter_information = l_letter_information;

    def set_l_easel_case_to_renew(self, l_easel_case_to_renew):
        self.l_easel_case_to_renew = l_easel_case_to_renew;

    def set_played_time(self, played_time):
        self.played_time = played_time;

    def set_n_round(self, n_round):
        self.n_round = n_round;

    def set_player_index(self, player_index):
        self.player_index = player_index;

    def set_stack(self, stack):
        self.stack = stack;

    def set_first_letter(self, first_letter):
        self.first_letter = first_letter;

    def set_l_case_bonus_covered(self, l_case_bonus_covered):
        self.l_case_bonus_covered;

    def set_l_player(self, l_player):
        self.l_player = l_player;

    def set_game_interface_instance(self, game_interface):
        self.game_interface = game_interface;

    def set_picking_mode(self, picking_mode):
        self.picking_mode = picking_mode;

    def set_l_joker_pos(self, l_joker_pos):
        self.l_joker_pos = l_joker_pos;

    def set_game_taken_up(self, game_taken_up):
        self.game_taken_up = game_taken_up;

    def set_n_placed_letter(self, n_placed_letter):
        self.n_placed_letter = n_placed_letter;

    def set_n_placed_word(self, n_placed_word):
        self.n_placed_word = n_placed_word;

    def set_n_scrabble(self, n_scrabble):
        self.n_scrabble = n_scrabble;




def get_played_time_formatted(played_time):
    """
        Formats a duration in seconds into a string like this 02:24:56
    """

    second = played_time;
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
