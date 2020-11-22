from button import Button
import pygame
import os
from game import GameStatus

class GameInterface():

    BOARD_SIZE = 550;
    BOARD_PADDING = 6;

    l_button_to_draw = [];
    l_img_letter = [];
    picking_mode = False;           #Variable à True quand l'utilisateur est en train de choisir des lettres à dégager pour en piocher d'autres

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

        self.bttn_next_round = Button();
        self.bttn_next_round.set_text("Commencer la partie");
        self.bttn_next_round.set_text_size(25);
        self.bttn_next_round.set_color((255, 255, 255));
        self.bttn_next_round.set_pos((970, 650));
        self.bttn_next_round.set_padding(10);
        self.bttn_next_round.set_border(True);
        self.bttn_next_round.set_border_thickness(3);

        self.bttn_pause = Button();
        self.bttn_pause.set_text("Mettre en pause")
        self.bttn_pause.set_text_size(26);
        self.bttn_pause.set_color((255, 255, 255));
        self.bttn_pause.set_pos((127, 300));
        self.bttn_pause.set_padding(8);

        bttn_display_help = Button();
        bttn_display_help.set_text("Afficher l'aide");
        bttn_display_help.set_text_size(26);
        bttn_display_help.set_color((255, 255, 255));
        bttn_display_help.set_pos((127, 330));
        bttn_display_help.set_padding(8);

        bttn_return_to_menu = Button();
        bttn_return_to_menu.set_text("Retour au menu principal");
        bttn_return_to_menu.set_text_size(24);
        bttn_return_to_menu.set_color((255, 255, 255));
        bttn_return_to_menu.set_pos((127, 380));
        bttn_return_to_menu.set_padding(8);

        self.l_button_to_draw.append(bttn_pick_new_letters);
        self.l_button_to_draw.append(self.bttn_next_round);
        self.l_button_to_draw.append(self.bttn_pause);
        self.l_button_to_draw.append(bttn_display_help);
        self.l_button_to_draw.append(bttn_return_to_menu);


    def load_images(self):

        self.scrabble_board = pygame.image.load(os.path.join("Images", "scrabble_board.png"));
        self.scrabble_board = pygame.transform.scale(self.scrabble_board, (self.BOARD_SIZE, self.BOARD_SIZE));

        for i in range(24):
            img_letter_name = "letter_" + chr(65+i) + ".png"
            img_letter_path = os.path.join("Images", "Letters", img_letter_name);

            img_letter = pygame.image.load(img_letter_path);

            case_size = int((self.BOARD_SIZE-self.BOARD_PADDING*2)/15);

            self.l_img_letter.append(img_letter);


    def draw(self, window):

        case_size = (self.BOARD_SIZE-self.BOARD_PADDING*2)/15

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        background_rect = (0, 0, interface_width, interface_height);
        pygame.draw.rect(window, (46, 40, 42), background_rect);



        #PART DRAW BOARD

        board_x = interface_width/2-self.BOARD_SIZE/2;
        board_y = 21;

        window.blit(self.scrabble_board, (board_x, board_y));


        #PART DRAW EASEL

        easel_width = self.BOARD_SIZE/1.3;
        easel_height = easel_width/7;

        letter_case_size = int(easel_width/7)

        font = pygame.font.SysFont("", size=20);
        for i in range(7):
            x = interface_width/2-easel_width/2+i*letter_case_size;
            y = 585

            letter_case_rect = (x, y, letter_case_size, letter_case_size);
            pygame.draw.rect(window, (255, 255, 255), letter_case_rect, 2);

            image_index_letter = font.render(str(i+1), True, (255, 255, 255));

            img_index_letter_size = font.size(str(i+1));
            img_x = x+letter_case_size/2-img_index_letter_size[0]/2;
            img_y = y+letter_case_size/2-img_index_letter_size[1]/2;

            window.blit(image_index_letter, (img_x, img_y));

            player_turn = self.game.get_player_turn();
            if(player_turn != None):
                letter_index = player_turn.get_easel()[i];

                if(letter_index != -1):
                    img_letter = self.l_img_letter[letter_index];
                    img_letter = pygame.transform.scale(img_letter, (letter_case_size-2, letter_case_size-2));

                    pygame.draw.rect(window, (0, 0, 0), letter_case_rect, 3);

                    #On réduit légèrement la taille des lettres pour qu'elles rentrent dans les cases sans effacer les contours
                    letter_case_rect = (x+1, y+1, letter_case_size-2, letter_case_size-2);
                    window.blit(img_letter, letter_case_rect);




        #PART DRAW SCORE

        font = pygame.font.SysFont("", size=30);
        img_text_score = font.render("Score", True, (255, 255, 255));

        window.blit(img_text_score, (865, 150));

        font = pygame.font.SysFont("", size=25);

        l_player = self.game.get_l_player();
        y = 178
        for player in l_player:
            player_name = player.get_name();
            player_score = player.get_score();

            txt_score_player = player_name + ": " + str(player_score) + " points";
            img_text_score_player = font.render(txt_score_player, True, (255, 255, 255));

            window.blit(img_text_score_player, (865, y));
            y+=25;


        #PART DRAW BUTTONS

        game_status = self.game.get_game_status();
        if(game_status != GameStatus.NotStarted):
            self.bttn_next_round.set_text("Passer au tour suivant");

        for button in self.l_button_to_draw:
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


        #PART DRAW MENU

        font = pygame.font.SysFont("", size=26);
        img_text_menu = font.render("Menu de jeu", True, (255, 255, 255));

        img_text_menu_size = img_text_menu.get_size();
        img_text_menu_x = 127-img_text_menu_size[0]/2;
        img_text_menu_y = 258-img_text_menu_size[1]/2;

        window.blit(img_text_menu, (img_text_menu_x, img_text_menu_y));

        line_start_pos = (127-img_text_menu_size[0]/2, 279);
        line_end_pos = (127+img_text_menu_size[0]/2, 279);
        pygame.draw.line(window, (255, 255, 255), line_start_pos, line_end_pos);

        line_start_pos = (127-img_text_menu_size[0]/2, 355);
        line_end_pos = (127+img_text_menu_size[0]/2, 355);
        pygame.draw.line(window, (255, 255, 255), line_start_pos, line_end_pos);

        menu_outline_rect = (15, 223, 222, 186);
        pygame.draw.rect(window, (255, 255, 255), menu_outline_rect, 2);




        player_turn = self.game.get_player_turn();
        if(player_turn != None):
            font = pygame.font.SysFont("", size=25);
            img_txt_player_turn = font.render("C'est à Antoine de jouer !", True, (255, 255, 255));

            image_size = img_txt_player_turn.get_size();
            window.blit(img_txt_player_turn, (970-image_size[0]/2, 600));


        #Pour le debug
        '''for x in range(0, 15):
            for y in range(0, 15):
                board_rect = (self.BOARD_PADDING+x*case_size, self.BOARD_PADDING+y*case_size, case_size, case_size);
                pygame.draw.rect(window, (255, 255, 255), board_rect);'''



        pygame.display.flip();


    def set_pause(self, pause):

        game_status = self.game.get_game_status();
        if(game_status == GameStatus.NotStarted or game_status == GameStatus.Finished):
            return;

        if(pause == True):
            self.game.set_game_status(GameStatus.Paused);
            self.bttn_pause.set_text("Reprendre la partie");

        elif(pause == False):
            self.game.set_game_status(GameStatus.InProgress);
            self.game.loop_timer();
            self.bttn_pause.set_text("Mettre en pause");


    def event(self, e):

        if(e.type == pygame.MOUSEBUTTONUP):

            for button in self.l_button_to_draw:

                mouse_x = e.pos[0];
                mouse_y = e.pos[1];

                if(button.in_bounds(mouse_x, mouse_y)):

                    if(button.get_text() == "Commencer la partie"):
                        self.game.start_game();

                    elif(button.get_text() == "Retour au menu principal"):
                        self.interface.change_page(0);

                    elif(button.get_text() == "Mettre en pause"):
                        self.set_pause(True);

                    elif(button.get_text() == "Reprendre la partie"):
                        self.set_pause(False);

                    elif(button.get_text() == "Piocher de nouvelles lettres"):
                        pass;


        elif(e.type == pygame.MOUSEMOTION):

            for button in self.l_button_to_draw:

                mouse_x = e.pos[0];
                mouse_y = e.pos[1];

                if(button.in_bounds(mouse_x, mouse_y)):
                    button.highlight(0, (23, 192, 187));
                else:
                    button.remove_highlighting();
