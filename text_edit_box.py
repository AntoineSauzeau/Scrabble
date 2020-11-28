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

    def keyboard_event(self, e):
        pass;

    def draw(self, window):

        font = pygame.font.SysFont(self.font_name, size=self.text_size);

        l_img_letter = [];
        max_img_letter_width = 0;
        max_img_letter_height = 0;

        #On crée l'image pour chaque lettre afin d'obtenir la taille de la lette la plus grosse
        for i in range(len(self.text)):

            letter = self.text[i];

            img_letter = font.render(letter, True, self.color);
            l_img_letter.append(img_letter);

            img_letter_size = img_letter.get_size();
            if(img_letter_size[0] > max_img_letter_width):
                max_img_letter_width = img_letter_size[0];

            if(img_letter_size[1] > max_img_letter_width):
                max_img_letter_height = img_letter_size[1];

            if(self.n_letter_max != -1 and i == self.n_letter_max-1):
                break;

        #Si on a pas de lettre, on en prend au hasard pour avoir la taille max de l'image des lettres
        if(len(l_img_letter) == 0):
            img_letter = font.render("K", True, self.color);
            img_letter_size = img_letter.get_size();

            max_img_letter_width = img_letter_size[0];
            max_img_letter_height = img_letter_size[1];


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
        for i in range(len(l_img_letter)):

            img_letter = l_img_letter[i];
            img_letter_size = img_letter.get_size();

            img_x = self.pos[0]+self.padding+i*max_img_letter_width+max_img_letter_width/2-img_letter_size[0]/2+i*self.space_between_letter;
            img_y = self.pos[1]+self.padding+max_img_letter_height-img_letter_size[1];

            img_letter_rect = (img_x, img_y, max_img_letter_width, img_letter_size[1]);
            window.blit(img_letter, img_letter_rect);


        box_x = self.pos[0];
        box_y = self.pos[1];
        box_height = 2*self.padding+max_img_letter_height+7;

        box_rect = (box_x, box_y, box_width, box_height);

        box = Shape();
        box.new_rectangle(window, self.b_color, box_rect, 1);
        box.draw();

    def get_size(self):
        pass;


    #GETTERS/SETTERS
    def set_focused(self, focused):
        self.focused = focused;

    def set_n_letter(self, n_letter):
        self.n_letter = n_letter;

    def set_n_letter_max():
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
