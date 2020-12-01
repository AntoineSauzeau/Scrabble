import pygame
from shape import Shape
import time

class TextEditBox:
    def __init__(self, text="", n_letter=10, pos=(15,15)):

        self.text = text;
        self.n_letter = n_letter;
        self.pos = pos;

        self.font_name = "";
        self.focused = False;
        self.n_letter_max = -1;
        self.color = (255, 255, 255);
        self.b_color = (255, 255, 255);
        self.text_size = 20
        self.padding = 5;
        self.space_between_letter = 10;

    def keyboard_event(self, key):

        if(key == None):
            return;

        if(65 <= key and key < 91):
            letter = chr(key);
            self.add_letter(letter);
        elif(97 <= key and key < 123):
            letter = chr(key);
            self.add_letter(letter);
        else:
            if(key == 8):
                self.remove_last_letter();


    def draw(self, window):

        font = pygame.font.SysFont(self.font_name, size=self.text_size);

        max_img_letter_width, max_img_letter_height = self.get_max_letter_size();

        #On dessine les lignes qui montrent la position des lettres
        for x_i in range(self.n_letter):

            underline_width = max_img_letter_width;
            underline_y = self.pos[1]+self.padding+max_img_letter_height+3;
            underline_x = self.pos[0]+self.padding+x_i*underline_width+x_i*self.space_between_letter

            underline_start_pos = (underline_x, underline_y);
            underline_end_pos = (underline_x+underline_width, underline_y);

            pygame.draw.line(window, self.color, underline_start_pos, underline_end_pos, 2);

            if(x_i == self.n_letter-1):
                box_width = underline_x+underline_width+self.padding-self.space_between_letter;


        #On dessine les lettres
        for i in range(len(self.text)):

            letter = self.text[i];

            img_letter = font.render(letter, True, self.color);
            img_letter_size = img_letter.get_size();

            img_x = self.pos[0]+self.padding+i*max_img_letter_width+max_img_letter_width/2-img_letter_size[0]/2+i*self.space_between_letter;
            img_y = self.pos[1]+self.padding+max_img_letter_height-img_letter_size[1];

            img_letter_rect = (img_x, img_y, max_img_letter_width, img_letter_size[1]);
            window.blit(img_letter, img_letter_rect);

            if(self.n_letter_max != -1 and i == self.n_letter_max-1):
                break;


        box_x = self.pos[0];
        box_y = self.pos[1];
        box_height = 2*self.padding+max_img_letter_height+7;

        box_rect = (box_x, box_y, box_width, box_height);

        box = Shape();
        box.new_rectangle(window, self.b_color, box_rect, 1);
        box.draw();

    def in_bounds(self, x, y):

        size = self.get_size();

        x_min = self.pos[0];
        x_max = x_min + size[0];
        y_min = self.pos[1];
        y_max = y_min + size[1];

        return (x_min <= x and x <= x_max and y_min <= y and y <= y_max);

    def get_max_letter_size(self):

        font = pygame.font.SysFont(self.font_name, size=self.text_size);

        #On crée l'image pour chaque lettre afin d'obtenir la taille de la lettre la plus grosse

        img_m = font.render("m", True, self.color);
        img_j = font.render("j", True, self.color);

        img_m_width = img_m.get_size()[0];
        img_j_height = img_j.get_size()[1];

        return (img_m_width, img_j_height);


    def get_size(self):

        max_letter_size = self.get_max_letter_size();

        height = 2*self.padding+max_letter_size[1]+7;
        width = 2*self.padding+self.n_letter*max_letter_size[0]+(self.n_letter-1)*self.space_between_letter;

        return (width, height);

    def add_letter(self, letter):

        if(len(self.text) < self.n_letter or (len(self.text) < self.n_letter_max and n_letter_max != -1)):
            self.text += letter;

    def remove_last_letter(self):
        self.text = self.text[:len(self.text)-1]


    #GETTERS/SETTERS
    def set_focused(self, focused):
        self.focused = focused;

    def set_n_letter(self, n_letter):
        self.n_letter = n_letter;

    def set_n_letter_max(self):
        self.n_letter_max = n_letter_max;

    def set_text_size(self, text_size):
        self.text_size = text_size;

    def set_text(self, text):
        self.text = text;

    def set_color(self, color):
        self.color = color;

    def set_b_color(self, b_color):
        self.b_color = b_color;

    def set_padding(self, padding):
        self.padding = padding;

    def set_font_name(self, font_name):
        self.font_name = font_name;

    def set_pos(self, pos):
        self.pos = pos;

    def set_space_between_letter(self, space_between_letter):
        self.space_between_letter = space_between_letter;

    def get_focused(self):
        return self.focused;

    def get_n_letter(self):
        return self.n_letter;

    def get_n_letter_max(self):
        return self.n_letter_max;

    def get_text_size(self):
        return self.text_size;

    def get_text(self):
        return self.text;

    def get_color(self):
        return self.color;

    def get_b_color(self):
        return self.b_color;

    def get_padding(self):
        return self.padding;

    def get_font_name(self):
        return self.font_name;

    def get_pos(self):
        return self.pos;

    def get_space_between_letter(self):
        return self.space_between_letter;
