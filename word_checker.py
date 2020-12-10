from enum import IntEnum
import game

class Direction(IntEnum):
    Horizontal = 0,
    Vertical = 1

class WordChecker:

    def __init__(self, game):

        self.game = game;
        self.file_scrabble_words_path = "scrabble_words.txt";

    def is_valid_word(self):

        main_word = self.get_word_placed();

        main_word_string = self.word_with_coord_to_string(main_word);
        print(main_word_string);

        other_word_completed = self.get_other_completed_word();

        #Un mot valable possède au minimum 2 lettres
        if(len(main_word) == 1):
            return False;

        if(other_word_completed != None):

            if(len(other_word_completed) == 1):
                return False;

            other_word_completed_string = self.word_with_coord_to_string(other_word_completed);
            print("Autre mot complété:", other_word_completed_string);

        l_word_to_check = [main_word_string];
        if(other_word_completed != None):
            l_word_to_check.append(other_word_completed_string);



        file_scrabble_words = open(self.file_scrabble_words_path, "r");

        scrabble_words = file_scrabble_words.readlines();
        for scrabble_word in scrabble_words:

            scrabble_word = scrabble_word.replace("\n", "");
            scrabble_word = scrabble_word.upper();

            for word in l_word_to_check:

                if(word == scrabble_word):
                    l_word_to_check.remove(word);
                    print("Mot found");

        #Si il reste des mots dans cette liste c'est qu'ils n'ont pas été trouvés dans la liste de mots de l'officiel du scrabble
        if(len(l_word_to_check) != 0):
            return False;
        else:
            return True;



    def get_word_placed(self):

        game_board = self.game.get_game_board();
        l_case_modified_during_round = self.game.get_l_case_modified_during_round();

        #On regarde si le mot est horizontal ou vertical
        direction = self.get_word_direction(l_case_modified_during_round); print(direction);

        #On met le mot dans l'ordre avec les lettres du mot qu'on connait déjà, c'est à dire les lettres placées par le joueur durant son tour
        word = self.get_sorted_letter(direction, l_case_modified_during_round);

        #C'est surement le premier tour et le joueur a posé une seule lettre donc impossible de trouver une direction à ce mot
        if(direction == None):
            letter_x = l_case_modified_during_round[0][0];
            letter_y = l_case_modified_during_round[0][1];
            letter_index = game_board[letter_x][letter_y];

            return [(letter_x, letter_y, letter_index)];

        #On essaye d'allonger le mot c'est à dire voir s'il y a des lettres déjà placées à un autre round qui sont collées dans sa direction
        word = self.get_extended_word(direction, word);

        return word;

    def get_extended_word(self, direction, word_to_extend):

        game_board = self.game.get_game_board();

        extended_word = word_to_extend;
        print("3: ", extended_word)
        if(direction == Direction.Vertical):

            letter_y_min = word_to_extend[0];
            print("1: ", letter_y_min)

            y_min = letter_y_min[1];

            y = y_min-1;
            x = letter_y_min[0];
            while(game_board[x][y] != -1):

                letter = (x, y, game_board[x][y]);
                if(not(letter in extended_word)):
                    print(letter);
                    extended_word.append(letter);

                y -= 1

            y = y_min+1
            while(game_board[x][y] != -1):

                letter = (x, y, game_board[x][y]);
                if(not(letter in extended_word)):
                    print(letter);
                    extended_word.append(letter);

                y += 1

        elif(direction == Direction.Horizontal):

            letter_x_min = word_to_extend[0];

            x_min = letter_x_min[0];

            x = x_min-1;
            y = letter_x_min[1];
            while(game_board[x][y] != -1):

                letter = (x, y, game_board[x][y]);
                if(not(letter in extended_word)):
                    extended_word.append(letter);

                x -= 1

            x = x_min+1
            while(game_board[x][y] != -1):

                letter = (x, y, game_board[x][y]);
                if(not(letter in extended_word)):
                    extended_word.append(letter);

                x += 1

        print("Extended word avant tri", extended_word);

        #On a rajouté les lettres trouvées sans s'embêter avec l'ordre donc maintenant on remet le mot dans l'ordre
        extended_word = self.get_sorted_letter(direction, extended_word);

        print("Extended word après tri", extended_word);

        return extended_word;


    def get_sorted_letter(self, direction, l_letter_pos):

        game_board = self.game.get_game_board();

        l_letter_sorted = [];
        for letter_pos in l_letter_pos:
            letter_no_sorted_x = letter_pos[0];
            letter_no_sorted_y = letter_pos[1];

            letter_no_sorted_index = game_board[letter_no_sorted_x][letter_no_sorted_y];

            letter_no_sorted_information = (letter_no_sorted_x, letter_no_sorted_y, letter_no_sorted_index);

            if(len(l_letter_sorted) != 0):
                for i in range(len(l_letter_sorted)):

                    letter_sorted_pos = l_letter_sorted[i];
                    if(direction == Direction.Vertical):
                        letter_sorted_y = letter_sorted_pos[1];

                        if(letter_sorted_y > letter_no_sorted_y):

                            if(not(letter_no_sorted_information in l_letter_sorted)):

                                insert_index = i;

                                l_letter_sorted.insert(insert_index, letter_no_sorted_information);

                        if(i == len(l_letter_sorted)-1):
                            l_letter_sorted.append(letter_no_sorted_information);

                    elif(direction == Direction.Horizontal):
                        letter_sorted_x = letter_sorted_pos[0];

                        if(letter_sorted_x > letter_no_sorted_x):

                            if(not(letter_no_sorted_information in l_letter_sorted)):

                                insert_index = i;

                                l_letter_sorted.insert(insert_index, letter_no_sorted_information);

                        if(i == len(l_letter_sorted)-1):
                            l_letter_sorted.append(letter_no_sorted_information);

            else:
                l_letter_sorted.append(letter_no_sorted_information);

        return l_letter_sorted;

    def get_word_direction(self, l_know_letters):

        game_board = self.game.get_game_board();

        direction = None;

        #Si il y a qu'une seule lettre posée par le joueur dans son tour on tente de trouver la direction en regardant les lettres autour posées dans d'autres tour
        if(len(l_know_letters) >= 2):

            case_1_pos = l_know_letters[0];
            case_2_pos = l_know_letters[1];

            if(case_1_pos[0] == case_2_pos[0]):
                direction = Direction.Vertical;
            elif(case_1_pos[1] == case_2_pos[1]):
                direction = Direction.Horizontal;

        else:
            letter = l_know_letters[0];
            letter_x = letter[0];
            letter_y = letter[1];

            if(game_board[letter_x-1][letter_y] != -1 or game_board[letter_x+1][letter_y] != -1):
                direction = Direction.Horizontal;
            elif(game_board[letter_x][letter_y-1] != -1 or game_board[letter_x][letter_y+1] != -1):
                direction = Direction.Vertical;

        return direction;


    def get_other_completed_word(self):

        game_board = self.game.get_game_board();
        l_letter_pos = self.game.get_l_case_modified_during_round();

        main_word_direction = self.get_word_direction(l_letter_pos);

        completed_word = None;
        for letter_pos in l_letter_pos:

            letter_x = letter_pos[0];
            letter_y = letter_pos[1];

            if(main_word_direction == Direction.Vertical):

                if(game_board[letter_x-1][letter_y] != -1 or game_board[letter_x+1][letter_y] != -1):
                    completed_word = self.get_extended_word(Direction.Horizontal, [letter_pos]);

            elif(main_word_direction == Direction.Horizontal):

                if(game_board[letter_x][letter_y-1] != -1 or game_board[letter_x][letter_y+1] != -1):
                    completed_word = self.get_extended_word(Direction.Vertical, [letter_pos]);

        return completed_word;

    def word_with_coord_to_string(self, word_with_coord):

        word_string = "";
        for letter_information in word_with_coord:
            letter_index = letter_information[2];
            letter_string = chr(65+letter_index);

            word_string += letter_string;

        return word_string;

    def count_word_value(self, word):

        l_letter_information = self.game.get_l_letter_information();
        l_joker_pos = self.game.get_l_joker_pos();

        word_value = 0;
        word_double = False;
        word_triple = False;
        for letter in word:
            letter_x = letter[0];
            letter_y = letter[1];

            if(len(l_joker_pos)):
                if(letter_x == l_joker_pos[0] and letter_y == l_joker_pos[1]):
                    break;

            letter_index = letter[2];
            letter_string = chr(65+letter_index);
            letter_value = l_letter_information[letter_string]["val"];

            case_type = self.game.get_case_type(letter_x, letter_y);


            if(case_type == game.CaseType.LD):
                letter_value = letter_value*2;
            elif(case_type == game.CaseType.LT):
                letter_value = letter_value*3
            elif(case_type == game.CaseType.WD):
                word_double = True;
            elif(case_type == game.CaseType.WT):
                word_triple = True;

            word_value += letter_value;

        if(word_double):
            word_value = word_value*2;
        elif(word_triple):
            word_value = word_value*3;

        return word_value;



    def count_total_placed_value(self):

        main_word = self.get_word_placed();
        other_word_completed = self.get_other_completed_word();

        total_value = 0;
        total_value += self.count_word_value(main_word);

        if(other_word_completed != None):
            total_value += self.count_word_value(get_other_completed_word);

        return total_value;
