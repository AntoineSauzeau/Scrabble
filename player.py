class Player:

    score = 0
    easel = [0, 1, 2, 3, 4, 5, 6]    #Stocke les lettres contenu dans le chevalet

    def __init__(self, name):
        self.name = name;

    #getters/setters
    def get_score(self):
        return self.score;

    def get_name(self):
        return self.name;

    def get_easel(self):
        return self.easel;

    def set_score(self, score):
        self.score = score;
