
class Player:

    def __init__(self, name):

        self.name = name;
        self.score = 0
        self.easel = [-1, -1, -1, -1, -1, -1, -1]    #Stocke les lettres contenu dans le chevalet

    #La fonction prend la liste des positions du chevalet à renouveller avec de nouvelles lettres piochées
    def renew_easel(self, easel_index):

            picked_letter = self.game.pick_a_letter();
            picked_letter_index = ord(picked_letter)-65;

            self.easel[easel_index] = picked_letter_index;
            print(picked_letter_index);

    def get_first_free_place_in_easel(self):

        for i in range(len(self.easel)):

            letter_index = self.easel[i];
            if(letter_index == -1):
                return i;


    #getters/setters
    def get_score(self):
        return self.score;

    def get_name(self):
        return self.name;

    def get_easel(self):
        return self.easel;

    def set_score(self, score):
        self.score = score;

    def set_game_instance(self, game):
        self.game = game;
