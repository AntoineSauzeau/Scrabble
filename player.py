
class Player:

    def __init__(self, name=""):

        self.name = name;
        self.score = 0
        self.easel = Easel(self);    #Stocke les lettres contenu dans le chevalet

    def add_score(self, value):
        self.score += value;


    #getters/setters
    def get_score(self):
        return self.score;

    def get_name(self):
        return self.name;

    def get_easel(self):
        return self.easel;

    def set_score(self, score):
        self.score = score;

    def set_name(self, name):
        self.name = name;

    def set_easel(self, easel):
        self.easel = easel;

    def set_game_instance(self, game):
        self.game = game;
        self.easel.set_game_instance(game);

class Easel:

    def __init__(self, player):

        self.player = player;
        self.l_letter = [-1, -1, -1, -1, -1, -1, -1];

    #La fonction prend la liste des positions du chevalet à renouveller avec de nouvelles lettres piochées
    def renew_letter(self, easel_index):

            picked_letter = self.game.pick_a_letter();
            picked_letter_index = ord(picked_letter)-65;

            self.l_letter[easel_index] = picked_letter_index;
            print(picked_letter_index);

    def get_first_free_place(self):

        for i in range(len(self.l_letter)):

            letter_index = self.l_letter[i];
            if(letter_index == -1):
                return i;

    def renew_all(self):

        for i in range(7):
                self.renew_letter(i);

    def fill(self):

        for i in range(7):
            if(self.l_letter[i] == -1):
                self.renew_letter(i);

    def get_l_letter(self):
        return self.l_letter;

    def set_l_letter(self, l_letter):
        self.l_letter = l_letter;

    def set_game_instance(self, game):
        self.game = game;
