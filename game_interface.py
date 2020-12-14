from enum import IntEnum
import pygame
import os

from game import GameStatus, get_played_time_formatted
from shape import Shape
from button import Button
from message import Message, Alignment
from player import Player


class Page(IntEnum):
    Game = 0,
    Save = 1

class GameInterface():

    BOARD_SIZE = 550;
    BOARD_PADDING = 6;

    def __init__(self, interface, game):

        print("Constructor GameInterface");

        self.l_button_to_draw_by_page = [[], []];
        self.l_easel_case_rectangle = [];
        self.l_img_letter = [];
        self.l_message = [];

        self.letter_moving_mode = False;
        self.letter_moving_index = -1;

        self.joker_choice_mode = False;
        self.l_joker_letter_choice_rect = [];

        self.exit_after_save_window = False;

        self.interface = interface;
        self.game = game;

        self.page = Page.Game;

        self.init_game_page();
        self.init_save_page();

        self.load_images();

    def init_game_page(self):

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        self.bttn_pick_new_letters = Button();
        self.bttn_pick_new_letters.set_text("Piocher de nouvelles lettres");
        self.bttn_pick_new_letters.set_text_size(24);
        self.bttn_pick_new_letters.set_color((255, 255, 255));
        self.bttn_pick_new_letters.set_pos((interface_width/2, 670));
        self.bttn_pick_new_letters.set_underline(True);

        self.bttn_next_round = Button();

        if(self.game.get_game_taken_up()):
            self.bttn_next_round.set_text("Reprendre la partie");
        else:
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

        page = Page.Game;
        self.l_button_to_draw_by_page[page].append(self.bttn_pick_new_letters);
        self.l_button_to_draw_by_page[page].append(self.bttn_next_round);
        self.l_button_to_draw_by_page[page].append(self.bttn_pause);
        self.l_button_to_draw_by_page[page].append(bttn_display_help);
        self.l_button_to_draw_by_page[page].append(bttn_return_to_menu);

        self.message_placed_word = Message();
        self.message_scrabble = Message();
        self.message_pick_stack = Message();
        self.message_end_game = Message();

        self.l_message.append(self.message_placed_word);
        self.l_message.append(self.message_scrabble);
        self.l_message.append(self.message_pick_stack);
        self.l_message.append(self.message_end_game);

    def init_save_page(self):

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        bttn_save = Button("Sauvegarder la partie");
        bttn_save.set_color((0, 0, 0));
        bttn_save.set_background_color((255, 255, 255));
        bttn_save.set_pos((interface_width/2, 330));
        bttn_save.set_padding(10);
        bttn_save.set_text_size(24);
        bttn_save.set_border(True);
        bttn_save.set_border_color((0, 224, 73));
        bttn_save.set_border_thickness(3);

        bttn_dont_save = Button("Quitter sans sauvegarder");
        bttn_dont_save.set_color((0, 0, 0));
        bttn_dont_save.set_background_color((255, 255, 255));
        bttn_dont_save.set_pos((interface_width/2, 440));
        bttn_dont_save.set_padding(10);
        bttn_dont_save.set_text_size(24);
        bttn_dont_save.set_border(True);
        bttn_dont_save.set_border_color((0, 224, 73));
        bttn_dont_save.set_border_thickness(3);

        bttn_cancel = Button("Retour au jeu");
        bttn_cancel.set_color((0, 0, 0));
        bttn_cancel.set_background_color((255, 255, 255));
        bttn_cancel.set_pos((interface_width/2, 500));
        bttn_cancel.set_padding(10);
        bttn_cancel.set_text_size(24);
        bttn_cancel.set_border(True);
        bttn_cancel.set_border_color((0, 224, 73));
        bttn_cancel.set_border_thickness(3);



        page = Page.Save;
        self.l_button_to_draw_by_page[page].append(bttn_save);
        self.l_button_to_draw_by_page[page].append(bttn_cancel);
        self.l_button_to_draw_by_page[page].append(bttn_dont_save);


    def load_images(self):

        self.scrabble_board = pygame.image.load(os.path.join("Images", "scrabble_board.png"));
        self.scrabble_board = pygame.transform.scale(self.scrabble_board, (self.BOARD_SIZE, self.BOARD_SIZE));

        for i in range(26):
            img_letter_name = "letter_" + chr(65+i) + ".png"
            img_letter_path = os.path.join("Images", "Letters", img_letter_name);

            img_letter = pygame.image.load(img_letter_path);

            case_size = int((self.BOARD_SIZE-self.BOARD_PADDING*2)/15);

            self.l_img_letter.append(img_letter);

        img_joker_path = os.path.join("Images", "Letters", "joker.png");
        img_joker = pygame.image.load(img_joker_path);

        self.l_img_letter.append(img_joker);

        self.img_loop = pygame.image.load(os.path.join("Images", "loop.png"));
        self.img_background_save = pygame.image.load(os.path.join("Images", "background_save.png"));


    def draw(self, window):

        if(self.page == Page.Game):
            self.draw_game_page(window);
        elif(self.page == Page.Save):
            self.draw_save_page(window);

    def draw_game_page(self, window):

        case_size = (self.BOARD_SIZE-self.BOARD_PADDING*2)/15

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        background_rect = (0, 0, interface_width, interface_height);
        pygame.draw.rect(window, (46, 40, 42), background_rect);



        #PART DRAW BOARD

        board_x = interface_width/2-self.BOARD_SIZE/2;
        board_y = 21;

        window.blit(self.scrabble_board, (board_x, board_y));

        game_board = self.game.get_game_board();

        for case_x in range(15):
            for case_y in range(15):

                letter_index = game_board[case_x][case_y];
                if(letter_index != -1):
                    img_letter = self.l_img_letter[letter_index];

                    img_letter_size = int(case_size);
                    img_letter = pygame.transform.scale(img_letter, (img_letter_size, img_letter_size))

                    img_letter_x = board_x + self.BOARD_PADDING + case_x*case_size+1;
                    img_letter_y = board_y + self.BOARD_PADDING + case_y*case_size+2;

                    window.blit(img_letter, (img_letter_x, img_letter_y));


        #PART DRAW EASEL

        del self.l_easel_case_rectangle[:];

        easel_width = self.BOARD_SIZE/1.3;
        easel_height = easel_width/7;

        letter_case_size = int(easel_width/7)

        font = pygame.font.SysFont("", size=20);
        for i in range(7):
            x = interface_width/2-easel_width/2+(i*letter_case_size)+(i/1.88)*2;
            y = 585

            letter_case_rect = (x, y, letter_case_size, letter_case_size);

            letter_case_rectangle = Shape();
            letter_case_rectangle.new_rectangle(window, (255, 255, 255), letter_case_rect, 2);
            letter_case_rectangle.draw();

            self.l_easel_case_rectangle.append(letter_case_rectangle);     #Pour avoir rapidement la dimension et la position de chaque case du chevalet au moment de gérer les évênements

            image_index_letter = font.render(str(i+1), True, (255, 255, 255));

            img_index_letter_size = font.size(str(i+1));
            img_x = x+letter_case_size/2-img_index_letter_size[0]/2;
            img_y = y+letter_case_size/2-img_index_letter_size[1]/2;

            window.blit(image_index_letter, (img_x, img_y));

            #On affiche les lettres dans les cases
            player_turn = self.game.get_player_turn();
            if(player_turn != None):
                player_easel = player_turn.get_easel();
                letter_index = player_easel.get_l_letter()[i];

                if(letter_index != -1):
                    img_letter = self.l_img_letter[letter_index];
                    img_letter = pygame.transform.scale(img_letter, (letter_case_size-2, letter_case_size-2));

                    pygame.draw.rect(window, (0, 0, 0), letter_case_rect, 3);

                    #On réduit légèrement la taille des lettres pour qu'elles rentrent dans les cases sans effacer les contours
                    letter_case_rect = (x+1, y+1, letter_case_size-2, letter_case_size-2);
                    window.blit(img_letter, letter_case_rect);



            #Si il y a des lettres qui ont été désigné pour être échangé alors on marque ces lettres avec un signe
            l_easel_case_to_renew = self.game.get_l_easel_case_to_renew();
            if(i in l_easel_case_to_renew):

                img_loop_size = int(case_size/1.8)
                img_loop = pygame.transform.scale(self.img_loop, (img_loop_size, img_loop_size));

                img_loop_x = letter_case_rect[0]+letter_case_rect[3]-img_loop_size-4;
                img_loop_y = letter_case_rect[1]+3;

                window.blit(img_loop, (img_loop_x, img_loop_y));


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

        for button in self.l_button_to_draw_by_page[self.page]:
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

        played_time = self.game.get_played_time();
        text_time_played = get_played_time_formatted(played_time);

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


        #DRAW MOVING LETTER

        if(self.letter_moving_index != -1):
            img_letter_moving = self.l_img_letter[self.letter_moving_index];
            img_letter_moving_size = int(case_size);

            img_letter_moving = pygame.transform.scale(img_letter_moving, (img_letter_moving_size, img_letter_moving_size));

            mouse_pos = pygame.mouse.get_pos();
            img_letter_moving_x = mouse_pos[0]-img_letter_moving_size/2
            img_letter_moving_y = mouse_pos[1]-img_letter_moving_size/2

            window.blit(img_letter_moving, (img_letter_moving_x, img_letter_moving_y));


        #DRAW JOKER CHOICE

        if(self.joker_choice_mode):

            space_between_letter = 18;
            img_letter_size = 35

            background_width = img_letter_size*10+space_between_letter*8+60;
            background_x = interface_width/2-background_width/2;

            pygame.draw.rect(window, (255, 255, 255), (background_x, 160, background_width, 300));
            pygame.draw.rect(window, (0, 0, 0), (background_x, 160, background_width, 300), 3);

            font = pygame.font.SysFont("", size=40);
            img_text_choice_joker = font.render("*** Choix du joker ***", True, (0, 0, 0));

            img_text_choice_joker_size = img_text_choice_joker.get_size();
            img_text_choice_joker_x = interface_width/2-img_text_choice_joker_size[0]/2;

            window.blit(img_text_choice_joker, (img_text_choice_joker_x, 200));

            self.l_joker_letter_choice_rect.clear();

            y_min = 250;
            for y_i in range(3):

                if(y_i < 2):
                    line_width = img_letter_size*10+space_between_letter*9;
                else:
                    line_width = img_letter_size*7+space_between_letter*6;

                img_letter_y = y_min + y_i*60;
                x_min = interface_width/2-line_width/2;
                for x_i in range(10):

                    img_index = y_i*10+x_i;
                    if(img_index == 26):
                        break;


                    img_letter = self.l_img_letter[img_index];
                    img_letter = pygame.transform.scale(img_letter, (img_letter_size, img_letter_size));

                    img_letter_x = x_min+x_i*(space_between_letter+img_letter_size);
                    if(y_i == 2):
                        img_letter_x += img_letter_size;

                    letter_frame_rect = (img_letter_x-2, img_letter_y-2, img_letter_size+4, img_letter_size+4);

                    letter_frame_srect = Shape();
                    letter_frame_srect.new_rectangle(window, (0, 0, 0), letter_frame_rect, 2);

                    letter_frame_srect.draw();

                    self.l_joker_letter_choice_rect.append(letter_frame_srect);

                    window.blit(img_letter, (img_letter_x, img_letter_y));



        #DRAW PART PLAYER TURN

        player_turn = self.game.get_player_turn();
        if(player_turn != None):
            font = pygame.font.SysFont("", size=25);

            txt_player_turn = "C'est à " + player_turn.get_name() + " de jouer !";
            img_txt_player_turn = font.render(txt_player_turn, True, (255, 255, 255));

            image_size = img_txt_player_turn.get_size();
            window.blit(img_txt_player_turn, (970-image_size[0]/2, 600));

        for message in self.l_message:
            message.draw(window);


        #Pour le debug
        '''for x in range(0, 15):
            for y in range(0, 15):
                board_rect = (self.BOARD_PADDING+x*case_size, self.BOARD_PADDING+y*case_size, case_size, case_size);
                pygame.draw.rect(window, (255, 255, 255), board_rect);'''



        pygame.display.flip();

    def draw_save_page(self, window):

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        img_background_save = pygame.transform.scale(self.img_background_save, (interface_width, interface_height));
        window.blit(img_background_save, (0, 0));

        font = pygame.font.SysFont("", size=38);
        img_save_title = font.render("Voulez vous sauvegarder avant de quitter ?", True, (255, 255, 255));

        img_save_title_size = img_save_title.get_size();
        img_save_title_x = interface_width/2 - img_save_title_size[0]/2;

        window.blit(img_save_title, (img_save_title_x, 200));

        for button in self.l_button_to_draw_by_page[self.page]:
            button.draw(window);

        pygame.display.flip();


    def set_pause(self, pause):

        game_status = self.game.get_game_status();
        if(game_status == GameStatus.NotStarted or game_status == GameStatus.Finished):
            return;

        if(pause == True):
            self.game.set_game_status(GameStatus.Paused);
            self.bttn_pause.set_text("Reprendre la partie");

            self.game.stop_timer();
            print("loop");

        elif(pause == False):
            self.game.set_game_status(GameStatus.InProgress);
            self.bttn_pause.set_text("Mettre en pause");

            self.game.start_timer();

    def show_message_placed_word(self, word, value, player_name):

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        if(value != 0):
            title_text = "Le joueur " + player_name + " a posé le mot " + word;
            subtitle_text = "Il remporte " + str(value) + " points !";
        else:
            title_text = "Le joueur " + player_name + " a posé le mot " + word;
            subtitle_text = "Ce mot n'est pas valable, il ne remporte aucun point";

        self.message_placed_word.set_text_title(title_text);
        self.message_placed_word.set_text_subtitle(subtitle_text);
        self.message_placed_word.set_horizontal_alignment(Alignment.Center);
        self.message_placed_word.set_text_title_size(40);
        self.message_placed_word.set_text_subtitle_size(32);
        self.message_placed_word.set_space_between_titles(20);
        self.message_placed_word.set_color_title((0, 0, 0));
        self.message_placed_word.set_color_subtitle((0, 0, 0));
        self.message_placed_word.set_border_color((0, 0, 0));
        self.message_placed_word.set_border_thickness(4);

        self.message_placed_word.set_pos((interface_width/2, 200));

        self.message_placed_word.show(3);

    def show_message_scrabble(self, player_name):

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        title_text = "Le joueur " + player_name + " a fait un scrabble !!!";
        subtitle_text = "Il remporte 50 points bonus !";

        self.message_scrabble.set_text_title(title_text);
        self.message_scrabble.set_text_subtitle(subtitle_text);
        self.message_scrabble.set_horizontal_alignment(Alignment.Center);
        self.message_scrabble.set_text_title_size(40);
        self.message_scrabble.set_text_subtitle_size(32);
        self.message_scrabble.set_space_between_titles(20);
        self.message_scrabble.set_color_title((0, 0, 0));
        self.message_scrabble.set_color_subtitle((0, 0, 0));
        self.message_scrabble.set_border_color((0, 0, 0));
        self.message_scrabble.set_border_thickness(4);

        self.message_scrabble.set_pos((interface_width/2, 200));

        self.message_placed_word.add_queued_message(self.message_scrabble, 3);

    def show_message_pick_stack(self, player_name, l_letter_picked, n_letter_remained):

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        title_text = "Le joueur " + player_name + " a pioché les lettres " + "".join(l_letter_picked); print(title_text)
        subtitle_text = "Il reste " + str(n_letter_remained)+ " lettres dans la pioche";

        self.message_pick_stack.set_text_title(title_text);
        self.message_pick_stack.set_text_subtitle(subtitle_text);
        self.message_pick_stack.set_horizontal_alignment(Alignment.Center);
        self.message_pick_stack.set_text_title_size(40);
        self.message_pick_stack.set_text_subtitle_size(32);
        self.message_pick_stack.set_space_between_titles(20);
        self.message_pick_stack.set_color_title((0, 0, 0));
        self.message_pick_stack.set_color_subtitle((0, 0, 0));
        self.message_pick_stack.set_border_color((0, 0, 0));
        self.message_pick_stack.set_border_thickness(4);

        self.message_pick_stack.set_pos((interface_width/2, 200));

        self.message_pick_stack.show(3);

    def show_message_save_loaded(self):

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        title_text = "Partie chargée avec succès !"

        self.message_pick_stack.set_text_title(title_text);
        self.message_pick_stack.set_horizontal_alignment(Alignment.Center);
        self.message_pick_stack.set_text_title_size(40);
        self.message_pick_stack.set_color_title((0, 0, 0));
        self.message_pick_stack.set_border_color((0, 0, 0));
        self.message_pick_stack.set_border_thickness(4);
        self.message_pick_stack.set_padding(14);

        self.message_pick_stack.set_pos((interface_width/2, 200));

        self.message_pick_stack.show(3);

    def show_message_end_game(self, winner_name, winner_score):

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        if(winner_name != ""):
            title_text = "Victoire de " + winner_name + " !!!";
            subtitle_text = "Il remporte la partie avec " + str(winner_score) + " points";
        else:
            title_text = "Egalité !";
            subtitle_text = "Les deux joueurs égalisent avec " + str(winner_score) + " points";

        self.message_end_game.set_text_title(title_text);
        self.message_end_game.set_text_subtitle(subtitle_text);
        self.message_end_game.set_horizontal_alignment(Alignment.Center);
        self.message_end_game.set_text_title_size(40);
        self.message_end_game.set_text_subtitle_size(32);
        self.message_end_game.set_space_between_titles(20);
        self.message_end_game.set_color_title((0, 0, 0));
        self.message_end_game.set_color_subtitle((0, 0, 0));
        self.message_end_game.set_border_color((0, 0, 0));
        self.message_end_game.set_border_thickness(4);
        self.message_end_game.set_padding(17);

        self.message_end_game.set_pos((interface_width/2, 200));

        self.message_placed_word.add_queued_message(self.message_end_game, 12);

    def event(self, e):

        interface_width = self.interface.GAME_WINDOW_WIDTH;
        interface_height = self.interface.GAME_WINDOW_HEIGHT;

        if(e.type == pygame.QUIT):
            self.page = Page.Save;
            self.exit_after_save_window = True;

        elif(e.type == pygame.MOUSEBUTTONUP):

            mouse_x = e.pos[0];
            mouse_y = e.pos[1];

            for button in self.l_button_to_draw_by_page[self.page]:

                #Gestion du click sur les boutons
                if(button.in_bounds(mouse_x, mouse_y)):

                    if(self.page == Page.Game):

                        if(button.get_text() == "Commencer la partie" or button.get_text() == "Reprendre la partie"):

                            game_status = self.game.get_game_status();
                            if(game_status == GameStatus.Paused):
                                self.set_pause(False);
                            else:
                                self.game.start_game();
                                self.bttn_next_round.set_text("Passer au tour suivant");

                        elif(button.get_text() == "Retour au menu principal"):
                            self.page = Page.Save;

                        elif(button.get_text() == "Mettre en pause"):
                            self.set_pause(True);

                        elif(button.get_text() == "Piocher de nouvelles lettres"):

                            game_status = self.game.get_game_status();
                            if(game_status == GameStatus.InProgress):

                                self.bttn_next_round.set_text("Valider et piocher");
                                self.bttn_pick_new_letters.set_text("Annuler");

                                self.game.set_picking_mode(True);

                        elif(button.get_text() == "Valider et piocher"):

                            self.bttn_next_round.set_text("Passer au tour suivant");
                            self.bttn_pick_new_letters.set_text("Piocher de nouvelles lettres");

                            self.game.next_round();

                        elif(button.get_text() == "Annuler"):

                            self.bttn_next_round.set_text("Passer au tour suivant");
                            self.bttn_pick_new_letters.set_text("Piocher de nouvelles lettres");

                            self.game.set_picking_mode(False);

                            l_easel_case_to_renew = self.game.get_l_easel_case_to_renew();
                            l_easel_case_to_renew.clear();

                        elif(button.get_text() == "Passer au tour suivant"):
                            self.game.next_round();

                            game_status = self.game.get_game_status();
                            if(game_status == GameStatus.Finished):
                                self.bttn_next_round.set_text("Refaire une partie ?");

                        elif(button.get_text() == "Refaire une partie ?"):

                            menu_interface = self.interface.get_menu_interface();

                            l_player_to_reset = self.game.get_l_player();

                            l_player = [];
                            for player in l_player_to_reset:

                                player_name = player.get_name();
                                player = Player(player_name);
                                l_player.append(player);

                            menu_interface.replay_game(l_player);

                    elif(self.page == Page.Save):

                        if(button.get_text() == "Retour au jeu"):
                            self.page = Page.Game;
                            self.exit_after_save_window = False;

                        elif(button.get_text() == "Quitter sans sauvegarder"):

                            menu_interface = self.interface.get_menu_interface();
                            menu_interface.change_page(0);

                        elif(button.get_text() == "Sauvegarder la partie"):
                            self.game.save_game();

                            menu_interface = self.interface.get_menu_interface();
                            menu_interface.change_page(0);



                    if(button.get_text() == "Sauvegarder la partie" or button.get_text() == "Quitter sans sauvegarder"):

                        if(self.exit_after_save_window):
                            controller = self.interface.get_controller();
                            controller.quit();
                        else:
                            self.interface.change_page(0);


                #Gestion du click au niveau du chevalet
                for i in range(len(self.l_easel_case_rectangle)):

                    easel_case_rectangle = self.l_easel_case_rectangle[i];

                    if(easel_case_rectangle.in_bounds(mouse_x, mouse_y)):

                        if(self.game.get_picking_mode()):

                            l_easel_case_to_renew = self.game.get_l_easel_case_to_renew();

                            if(not(i in l_easel_case_to_renew)):
                                l_easel_case_to_renew.append(i);
                            else:
                                l_easel_case_to_renew.remove(i);

                        else:

                            if(self.letter_moving_mode != True):

                                self.letter_moving_mode = True;

                                player = self.game.get_player_turn();

                                easel = player.get_easel();
                                easel_l_letter = easel.get_l_letter();

                                self.letter_moving_index = easel_l_letter[i];
                                self.easel_start_case_index = i;
                                easel_l_letter[i] = -1;

                            else:

                                self.letter_moving_mode = False;

                                player = self.game.get_player_turn();

                                easel = player.get_easel();
                                easel_l_letter = easel.get_l_letter();

                                easel_l_letter[self.easel_start_case_index] = easel_l_letter[i];
                                easel_l_letter[i] = self.letter_moving_index;
                                self.letter_moving_index = -1;


                #Gestion du click au niveau du plateau de jeu
                case_size = (self.BOARD_SIZE-self.BOARD_PADDING*2)/15;
                for x_i in range(15):
                    for y_i in range(15):

                        board_x = interface_width/2-self.BOARD_SIZE/2;
                        board_y = 21;

                        case_x = board_x + self.BOARD_PADDING + x_i*case_size+1;
                        case_y = board_y + self.BOARD_PADDING + y_i*case_size+2;

                        letter_case_rectangle = Shape();
                        letter_case_rectangle.new_rectangle(None, (255, 255, 255), (case_x, case_y, case_size, case_size));

                        if(letter_case_rectangle.in_bounds(mouse_x, mouse_y)):

                            if(self.letter_moving_index != -1):

                                letter_placed = self.game.add_letter_to_game_board(x_i, y_i, self.letter_moving_index);
                                if(letter_placed):

                                    if(self.letter_moving_index == 26):
                                        self.joker_choice_mode = True;

                                        l_joker_pos = self.game.get_l_joker_pos();
                                        l_joker_pos.append((x_i, y_i));

                                    self.letter_moving_mode = False;
                                    self.letter_moving_index = -1;


        elif(e.type == pygame.MOUSEBUTTONDOWN):

            mouse_x = e.pos[0];
            mouse_y = e.pos[1];

            if(self.joker_choice_mode):

                for button in self.l_button_to_draw_by_page[self.page]:

                    for letter_index in range(len(self.l_joker_letter_choice_rect)):
                        letter_choice_rect = self.l_joker_letter_choice_rect[letter_index];

                        if(letter_choice_rect.in_bounds(mouse_x, mouse_y)):

                            self.joker_choice_mode = False;

                            game_board = self.game.get_game_board();
                            l_joker_pos = self.game.get_l_joker_pos();

                            last_joker_pos = l_joker_pos[-1];
                            game_board[last_joker_pos[0]][last_joker_pos[1]] = letter_index;


        elif(e.type == pygame.MOUSEMOTION):

            mouse_x = e.pos[0];
            mouse_y = e.pos[1];

            for button in self.l_button_to_draw_by_page[self.page]:

                if(button.in_bounds(mouse_x, mouse_y)):
                    button.highlight(0, (23, 192, 187));
                else:
                    button.remove_highlighting();

    def change_page(self, page):
        self.page = page;

    def get_game_instance(self):
        return self.game;

    def set_game_instance(self, game_instance):
        self.game = game_instance;
