from button import Button
import pygame
import os

class GameInterface():

    BOARD_SIZE = 550;
    BOARD_PADDING = 6;

    l_button = [];

    def __init__(self, interface, game):

        print("Constructor Gameinterface");

        self.interface = interface;
        self.game = game;

        self.init_graphic_elements();
        self.load_images();

    def init_graphic_elements(self):

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        bttn_pick_new_letters = Button();
        bttn_pick_new_letters.set_text("Piocher de nouvelles lettres");
        bttn_pick_new_letters.set_text_size(24);
        bttn_pick_new_letters.set_color((255, 255, 255));
        bttn_pick_new_letters.set_pos((interface_width/2, 670));
        bttn_pick_new_letters.set_underline(True);

        bttn_next_round = Button();
        bttn_next_round.set_text("Passer au tour suivant");
        bttn_next_round.set_text_size(25);
        bttn_next_round.set_color((255, 255, 255));
        bttn_next_round.set_pos((870, 650));
        bttn_next_round.set_padding(10);
        bttn_next_round.set_border(True);
        bttn_next_round.set_border_thickness(3);

        self.l_button.append(bttn_pick_new_letters);
        self.l_button.append(bttn_next_round);

    def load_images(self):

        self.scrabble_board = pygame.image.load(os.path.join("Images", "scrabble_board.png"));
        self.scrabble_board = pygame.transform.scale(self.scrabble_board, (self.BOARD_SIZE, self.BOARD_SIZE));

    def draw(self, window):

        case_size = (self.BOARD_SIZE-self.BOARD_PADDING*2)/15

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        background_rect = (0, 0, interface_width, interface_height);
        pygame.draw.rect(window, (41, 63, 20), background_rect);



        #PART DRAW BOARD

        board_x = interface_width/2-self.BOARD_SIZE/2;
        board_y = 21;

        window.blit(self.scrabble_board, (board_x, board_y));


        #PART DRAW EASEL

        easel_width = self.BOARD_SIZE/1.3;
        easel_height = easel_width/7;

        letter_case_size = easel_width/7

        font = pygame.font.SysFont("", size=20);
        for i in range(7):
            x = interface_width/2-easel_width/2+i*letter_case_size;
            y = 585

            letter_case_rect = (x, y, letter_case_size, letter_case_size);
            pygame.draw.rect(window, (255, 255, 255), letter_case_rect, 2);

            image_index_letter = font.render(str(i+1), True, (255, 255, 255));

            image_size = font.size(str(i+1));
            image_x = x+letter_case_size/2-image_size[0]/2
            image_y = y+letter_case_size/2-image_size[1]/2

            window.blit(image_index_letter, (image_x, image_y));



        #PART DRAW SCORE

        font = pygame.font.SysFont("", size=30);
        img_text_score = font.render("Score", True, (255, 255, 255));

        window.blit(img_text_score, (800, 150));

        font = pygame.font.SysFont("", size=25);

        l_player = self.game.get_l_player();
        y = 178
        for player in l_player:
            player_name = player.get_name();
            player_score = player.get_score();

            txt_score_player = player_name + ": " + str(player_score) + " points";
            img_text_score_player = font.render(txt_score_player, True, (255, 255, 255));

            window.blit(img_text_score_player, (800, y));
            y+=25;


        #PART DRAW BUTTONS

        for button in self.l_button:
            button.draw(window);


        #DRAW GRID MARKS

        img_y = 5;
        x_min = interface_width/2-(self.BOARD_SIZE)/2+self.BOARD_PADDING+case_size/2;
        for x_i in range(0, 15):
            letter = chr(65+x_i);

            font = pygame.font.SysFont("", size=20);
            img_grid_mark = font.render(letter, True, (255, 255, 255));

            image_size = font.size(letter);
            img_x = x_min+x_i*case_size-image_size[0]/2;

            window.blit(img_grid_mark, (img_x, img_y));

        img_x = x_min-case_size/2-26
        y_min = board_y+self.BOARD_PADDING+case_size/2
        for y_i in range(0, 15):
            number = str(y_i+1)

            font = pygame.font.SysFont("", size=20);
            img_grid_mark = font.render(number, True, (255, 255, 255));

            image_size = font.size(number);
            img_y = y_min+y_i*case_size-image_size[1]/2;

            window.blit(img_grid_mark, (img_x, img_y));


            #PART DRAW TIME

            font = pygame.font.SysFont("", size=25);
            text_time_played = self.game.get_played_time_formatted();

            img_text_time_played = font.render(text_time_played, True, (255, 255, 255));
            window.blit(img_text_time_played, (10, 10));


            font = pygame.font.SysFont("", size=25);
            img_txt_player_turn = font.render("C'est à Antoine de jouer !", True, (255, 255, 255));

            image_size = img_txt_player_turn.get_size();
            window.blit(img_txt_player_turn, (870-image_size[0]/2, 600));


        '''for x in range(0, 15):
            for y in range(0, 15):
                board_rect = (self.BOARD_PADDING+x*case_size, self.BOARD_PADDING+y*case_size, case_size, case_size);
                pygame.draw.rect(window, (255, 255, 255), board_rect);'''



        pygame.display.flip();


    def event(self, e):

        self.interface.draw();

        pass;
