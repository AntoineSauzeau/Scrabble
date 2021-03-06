
class Player:
    """
        Represent a player
    """

    def __init__(self, name=""):

        self.name = name;
        self.score = 0;
        self.easel = Easel(self);

        #Stats
        self.n_placed_letter = 0;
        self.n_placed_word = 0;
        self.n_scrabble = 0;

    def add_score(self, value):
        self.score += value;


    #GETTERS/SETTERS
    def get_score(self):
        return self.score;

    def get_name(self):
        return self.name;

    def get_easel(self):
        return self.easel;

    def get_n_placed_letter(self):
        return self.n_placed_letter;

    def get_n_placed_word(self):
        return self.n_placed_word;

    def get_n_scrabble(self):
        return self.n_scrabble;

    def set_score(self, score):
        self.score = score;

    def set_name(self, name):
        self.name = name;

    def set_easel(self, easel):
        self.easel = easel;

    def set_n_placed_letter(self, n_placed_letter):
        self.n_placed_letter = n_placed_letter;

    def set_n_placed_word(self, n_placed_word):
        self.n_placed_word = n_placed_word;

    def set_n_scrabble(self, n_scrabble):
        self.n_scrabble = n_scrabble

    def set_game_instance(self, game):
        self.game = game;
        self.easel.set_game_instance(game);

class Easel:
    """
        Represent the easel of a player
    """

    def __init__(self, player):

        self.player = player;
        self.l_letter = [-1, -1, -1, -1, -1, -1, -1];

    def renew_letter(self, easel_index):
        """
            Picks a letter and places it in the easel at the position indicated by parameters
        """

        picked_letter = self.game.pick_a_letter();

        if(picked_letter == None):
            self.l_letter[easel_index] = -1;
            return None;

        if(picked_letter != "?"):
            picked_letter_index = ord(picked_letter)-65;
        else:
            picked_letter_index = 26;

        self.l_letter[easel_index] = picked_letter_index;
        return picked_letter_index;

    def get_first_free_place(self):
        """
            Returns the first empty place in the easel
        """

        for i in range(len(self.l_letter)):

            letter_index = self.l_letter[i];
            if(letter_index == -1):
                return i;

    def renew_all(self):
        """
            Replace all the letters on the easel with new picked letters
        """

        for i in range(7):
                self.renew_letter(i);

    def fill(self):
        """
            Fill the easel with new letters at the empty spaces.
        """

        for i in range(7):
            if(self.l_letter[i] == -1):
                self.renew_letter(i);

    def count_total_value(self):
        """
            Returns the total value of the easel by adding up the value of all the letters in the easel
        """

        l_letter_information = self.game.get_l_letter_information();
        easel_value = 0;

        for i in range(7):
            letter_index = self.l_letter[i];
            if(letter_index == -1):
                continue;

            letter = chr(letter_index+65);

            letter_value = l_letter_information[letter]["val"];
            easel_value += letter_value;

        return easel_value;

    def empty(self):
        """
            Returns True if the easel is empty
        """

        for i in range(7):
            letter_index = self.l_letter[i];
            if(letter_index != -1):
                return False;

        return True;



    #GETTERS/SETTERS
    def get_l_letter(self):
        return self.l_letter;

    def set_l_letter(self, l_letter):
        self.l_letter = l_letter;

    def set_game_instance(self, game):
        self.game = game;
