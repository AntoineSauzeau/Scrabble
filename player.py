class Player:

    score = 0

    def __init__(self, name):
        self.name = name;

    #getters/setters
    def get_score(self):
        return self.score;

    def get_name(self):
        return self.name;

    def set_score(self, score):
        self.score = score;
