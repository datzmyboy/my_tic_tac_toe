import pygame
from pygame.font import SysFont
from MENU import Menu
import random
# Initialize Pygame
pygame.init()


class Game:
    def __init__(self):
        self.window_size = (600, 700)
        self.screen = pygame.display.set_mode(self.window_size)
        # pygame.display.set_caption("2 Players")
        self.font = pygame.font.SysFont(None, 150)
        self.color_to_use = None
        self.hud_font = pygame.font.SysFont(None,100)
        self.game_state_font = pygame.font.SysFont(None,40)
        self.winner_font = pygame.font.SysFont(None,30)
        self.box1 = (0, 0, 200, 200)
        self.box2 = (200, 0, 200, 200)
        self.box3 = (400, 0, 200, 200)
        self.box4 = (0, 200, 200, 200)
        self.box5 = (200, 200, 200, 200)
        self.box6 = (400, 200, 200, 200)
        self.box7 = (0, 400, 200, 200)
        self.box8 = (200, 400, 200, 200)
        self.box9 = (400, 400, 200, 200)
        self.hud = (0, 600, 600, 100)
        self.box_states = [None] * 9  # Use None for empty, 'X' for X, 'O' for O
        self.x_turn = True  # X starts first
        self.row_1 = [" ", " ", " "]
        self.row_2 = [" ", " ", " "]
        self.row_3 = [" ", " ", " "]
        self.list_of_rows = [self.row_1, self.row_2, self.row_3]
        self.x_score = 0
        self.o_score = 0

        self.game_over_bool = False
        self.draw =  False
        self.current_symbol = "X"
        self.win_text = self.game_state_font.render(f"Player {self.current_symbol} wins", True, (0, 0, 0))

        self.running, self.playing = True, False
        self.menu = Menu(self)
        self.game2 = Game2(self.menu)
        self.game2.menu = self.menu

    def set_caption(self,text):
        pygame.display.set_caption(text)

    def main_loop(self):
       self.set_caption("2 Players")
       while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.menu.end_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over_bool or self.draw:
                        self.reset_game()
                    else:
                        self.is_pressed_function(event)
                self.back_screen(event)
            self.screen.fill((0, 0, 0))
            self.draw_boxes()
            self.activate_box()
            self.draw_on_the_boxes()
            self.blit_hud()

            pygame.display.update()
    # once back key is pressed it will go back to the main screen
    def back_screen(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.playing = False
                self.menu.run_display = True
                self.reset_game()
                self.x_score = 0
                self.o_score = 0
                print("all set")
    # blits the scores, players turn, who is the winner
    def blit_hud(self):
        hud_rect = pygame.Rect(self.hud)
        pygame.draw.rect(self.screen, (255, 255, 0), self.hud)

        x_score_text = self.hud_font.render(f"X: {self.x_score}", True, (0, 0, 0))
        o_score_text = self.hud_font.render(f"O: {self.o_score}", True, (0, 0, 0))

        screen_width, screen_height = self.window_size
        self.screen.blit(x_score_text, (10, screen_height - 90))
        self.screen.blit(o_score_text, (screen_width - o_score_text.get_width() - 10, screen_height - 90))

        player_state_text = self.game_state_font.render(f"Player {self.current_symbol} turn", True,(0,0,0))

        if self.draw:
            draw_text = self.game_state_font.render(f"DRAW", True, (0, 0, 0))
            self.screen.blit(draw_text, (screen_width // 2 - 40, screen_height - 90))

        #  blits who is the winner from the game_over_bool variable
        elif self.game_over_bool:
            win_text = self.game_state_font.render(f"Player {self.current_symbol} wins", True, (0, 0, 0))
            self.screen.blit(win_text, (screen_width // 2 - 85, screen_height - 90))

        else:
            if self.x_turn:
                player_state_text = self.game_state_font.render(f"Player X turn", True, (0, 0, 0))
            else:
                player_state_text = self.game_state_font.render(f"Player O turn", True, (0, 0, 0))
            self.screen.blit(player_state_text, (screen_width // 2 - 85, screen_height - 90))

    def update_score(self):
        if self.current_symbol == "X":
            self.x_score += 1
        elif self.current_symbol == "O":
            self.o_score += 1

    def draw_boxes(self):
        # elements in these lits are coordinates of each box
        for box in [self.box1, self.box2, self.box3, self.box4, self.box5, self.box6, self.box7, self.box8, self.box9]:
            pygame.draw.rect(self.screen, (255, 255, 255), box, 3)

    # colors the boxes if the mouse is hovering on it
    def activate_box(self):
        a, b = pygame.mouse.get_pos() # returns the current pos of mouse cursor x and y as a tuple
        for box in [self.box1, self.box2, self.box3, self.box4, self.box5, self.box6, self.box7, self.box8, self.box9]:
            box_x, box_y, box_w, box_h = box # x_coords , y_coords, width , height = box as a tuple
            if box_x <= a <= box_x + box_w and box_y <= b <= box_y + box_h:# checks if a is greater or equal box_x. ensures that mouse's x-coordinate (a) is less than or equal to the right edge of the box. Ensure the mouse's y-coordinate (b) is greater than or equal to the top edge of the box Ensure the mouse's y-coordinate (b) is less than or equal to the bottom edge of the box
                #if (box_x <= a and a <= box_x + box_w) and (box_y <= b and b <= box_y + box_h): how to write it in more understandable way.
                pygame.draw.rect(self.screen, (180, 180, 180), box) # if condtion is true color will change

    # checks if a box is pressed
    def is_pressed_function(self, event):
        a, b = pygame.mouse.get_pos()
        for i, box in enumerate([self.box1, self.box2, self.box3, self.box4, self.box5, self.box6, self.box7, self.box8, self.box9]):
            box_rect = pygame.Rect(box)
            if event.type == pygame.MOUSEBUTTONDOWN and box_rect.collidepoint(a, b) and self.box_states[i] is None:
                if self.x_turn:
                    self.color_to_use = (255,0,0)
                    self.current_symbol = "X"       # this part determines the current symbol if selfx_turn is true or not
                    self.box_states[i] = 'X'
                    self.update_backend(i, 'x')
                else:
                    self.color_to_use = (0, 0, 255)
                    self.current_symbol = "O"
                    self.box_states[i] = 'O'
                    self.update_backend(i, 'o')
                self.x_turn = not self.x_turn  # Switch turn from true to false or false to true
                self.check_winner()
    # this draws the symbol on each boxes if it meets the conditions
    def draw_on_the_boxes(self):
        for i, box in enumerate([self.box1, self.box2, self.box3, self.box4, self.box5, self.box6, self.box7, self.box8, self.box9]):
            if self.box_states[i] is not None: # this means that if the element in the list box_states is not none (x or o) do the condtions under
                if self.box_states[i] == 'X':
                    color = (255, 0, 0)  # Red for 'X'
                else:
                    color = (0, 0, 255)  # Blue for 'O'
                # the symbol x or O
                text_surface = self.font.render(self.box_states[i], True, color)
                # Calculate the center position for the text in the current box
                text_rect = text_surface.get_rect(center=(box[0] + box[2] // 2, box[1] + box[3] // 2)) # the coordinates
                # Blit the text surface onto the screen at the calculated position
                self.screen.blit(text_surface, text_rect)

    def update_backend(self, box_index, symbol):
        row, col = divmod(box_index, 3) # this returns quotient and the remainder. 3 because it is 3 x 3
        self.list_of_rows[row][col] = symbol
        self.print_board()

    def print_board(self):
        # Determine which player's turn it is
        if self.x_turn:     # for reference purposes only
            player = '1'
            symbol = 'X'
        else:
            self.current_symbol = "O"
            player = '2'
            symbol = 'O'
        # Print which player made the move and what symbol they placed
        print("Player " + player + " placed " + symbol)
        # Loop through each row in the list of rows
        for row in self.list_of_rows:
            # Print the row
            print(f'{row} <<<<<<<')

    def check_winner(self):
        if winner_for_row(self.row_1, self.row_2, self.row_3): # i made a separate function outside the class just for checking who is the winner
            self.game_over_bool = True
            self.update_score()
            print("Game over!")

        elif winner_for_columns(self.row_1, self.row_2, self.row_3):
            self.game_over_bool = True
            self.update_score()

            print("Game over!")

        elif winner_for_diagonal(self.row_1, self.row_2, self.row_3):
            self.game_over_bool = True
            self.update_score()
            print("Game over!")
        else:
            # Check for draw
            draw_detected = True  # Assume the game is a draw initially
            # Iterate through each row in the list of rows
            for row in self.list_of_rows:
                # Iterate through each cell in the current row
                for cell in row:
                    # Check if the current cell is a space
                    if cell == " ":
                        # If any cell is a space, the game is not a draw
                        draw_detected = False
                        # No need to check further, exit the inner loop
                        break
                # If draw_detected is already False, no need to check further, exit the outer loop
                if not draw_detected:
                    break
            # If draw_detected is still True, then all cells are occupied, and it is a draw
            if draw_detected:
                self.draw = True


    def reset_game(self):
        self.box_states = [None] * 9
        self.row_1 = [" ", " ", " "]
        self.row_2 = [" ", " ", " "]
        self.row_3 = [" ", " ", " "]
        self.list_of_rows = [self.row_1, self.row_2, self.row_3]
        self.x_turn = True
        self.game_over_bool = False
        self.draw = False
        self.current_symbol = "X"
# FOR THE UI FEATURES
#################################################################


def winner_for_row(row_1, row_2, row_3):
    for row in [row_1, row_2, row_3]:
        if row[0] == row[1] == row[2] and row[0] != " ":
            print(f"Player {row[0]} wins!")
            return True
    return False

def winner_for_columns(row_1, row_2, row_3):
    for col in range(3):
        if row_1[col] == row_2[col] == row_3[col] and row_1[col] != " ":
            print(f"Player {row_1[col]} wins!")
            return True
    return False

def winner_for_diagonal(row_1, row_2, row_3):
    if row_1[0] == row_2[1] == row_3[2] and row_1[0] != " ":
        print(f"Player {row_1[0]} wins!")
        return True
    if row_1[2] == row_2[1] == row_3[0] and row_1[2] != " ":
        print(f"Player {row_1[2]} wins!")
        return True
    return False


class Game2:
    def __init__(self,menu):
        self.window_size = (600, 700)
        self.screen = pygame.display.set_mode(self.window_size)
        # pygame.display.set_caption("1 Player")
        self.font = pygame.font.SysFont(None, 150)
        self.color_to_use = None
        self.hud_font = pygame.font.SysFont(None, 100)
        self.game_state_font = pygame.font.SysFont(None, 40)
        self.winner_font = pygame.font.SysFont(None, 30)
        self.box1 = (0, 0, 200, 200)
        self.box2 = (200, 0, 200, 200)
        self.box3 = (400, 0, 200, 200)
        self.box4 = (0, 200, 200, 200)
        self.box5 = (200, 200, 200, 200)
        self.box6 = (400, 200, 200, 200)
        self.box7 = (0, 400, 200, 200)
        self.box8 = (200, 400, 200, 200)
        self.box9 = (400, 400, 200, 200)
        self.hud = (0, 600, 600, 100)
        self.box_states = [None] * 9  # Use None for empty, 'X' for X, 'O' for O
        self.row_1 = [" ", " ", " "]
        self.row_2 = [" ", " ", " "]
        self.row_3 = [" ", " ", " "]
        self.list_of_rows = [self.row_1, self.row_2, self.row_3]
        self.x_score = 0
        self.o_score = 0
        self.draw = False
        self.game_over_bool = False
        # self.win_text = self.game_state_font.render(f"Player {self.current_symbol} wins", True, (0, 0, 0))

        self.player = self.Player(self)
        self.ai = self.AI(self)

        self.ai_turn = False
        self.player_turn = False
        self.menu = menu
        self.running2, self.playing2 = True, False
        self.collided = False
    def set_caption(self,text):
        pygame.display.set_caption(text)
    def main_loop2(self):
        self.set_caption('1 Player')
        self.who_go_first()
        while self.playing2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu.end_game2()
                if self.ai_turn:
                    self.ai.ai_press_function()
                    self.ai_turn = False
                    self.player_turn = True
                    print(f" the value of ai {self.ai_turn}")
                    print(f"the value of player {self.player_turn}")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player_turn:
                        self.player.is_pressed_function(event)
                        if self.collided:
                            self.player_turn = False
                            self.ai_turn = True
                            self.collided = False
                self.back_screen(event)
            self.screen.fill((0, 0, 0))
            self.draw_boxes()
            self.activate_box()
            self.draw_on_the_boxes()
            self.blit_hud()

            pygame.display.update()
    def back_screen(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.playing2 = False
                self.menu.run_display = True
                self.reset_game()
                self.x_score = 0
                self.o_score = 0
    def who_go_first(self):
        who_go_first = random.choice(["X", "O"])
        if who_go_first == "X":
            self.player_turn = True
            print("player first")
        else:
            self.ai_turn = True
            print("ai first")

    def blit_hud(self):
        pygame.draw.rect(self.screen, (255, 255, 0), (0, 600, 600, 100))
        x_score_text = self.hud_font.render(f"X: {self.x_score}", True, (0, 0, 0))
        o_score_text = self.hud_font.render(f"O: {self.o_score}", True, (0, 0, 0))
        self.screen.blit(x_score_text, (10, 610))
        self.screen.blit(o_score_text, (400, 610))

        if self.game_over_bool:
            if self.player_turn:
                game_over_text = self.game_state_font.render("PLAYER X WINS", True, (0, 0, 0))
                self.screen.blit(game_over_text, (180, 610))
            elif self.ai_turn:
                game_over_text = self.game_state_font.render("PLAYER 0 WINS", True, (0, 0, 0))
                self.screen.blit(game_over_text, (180, 610))

        elif self.draw:
            draw_text = self.game_state_font.render("IT'S A DRAW", True, (0, 0, 0))
            self.screen.blit(draw_text, (200, 610))
        elif self.player_turn:
            player_turn_text = self.game_state_font.render("PLAYER X TURN", True, (0, 0, 0))
            self.screen.blit(player_turn_text, (170, 610))
        else:
            player_turn_text = self.game_state_font.render("AI O TURN", True, (0, 0, 0))
            self.screen.blit(player_turn_text, (200, 610))




    def draw_boxes(self):
        for box in [self.box1, self.box2, self.box3, self.box4, self.box5, self.box6, self.box7, self.box8, self.box9]:
            pygame.draw.rect(self.screen, (255, 255, 255), box, 3)

    def activate_box(self):
        a, b = pygame.mouse.get_pos()
        for box in [self.box1, self.box2, self.box3, self.box4, self.box5, self.box6, self.box7, self.box8, self.box9]:
            box_x, box_y, box_w, box_h = box
            if box_x <= a <= box_x + box_w and box_y <= b <= box_y + box_h:
                pygame.draw.rect(self.screen, (180, 180, 180), box)

    def draw_on_the_boxes(self):
        for i, box in enumerate([self.box1, self.box2, self.box3, self.box4, self.box5, self.box6, self.box7, self.box8, self.box9]):
            if self.box_states[i] is not None:
                if self.box_states[i] == 'X':
                    color = (255, 0, 0)
                elif self.box_states[i] == 'O':
                    color = (0, 0, 255)
                text_surface = self.font.render(self.box_states[i], True, color)
                # Calculate the center position for the text in the current box
                text_rect = text_surface.get_rect(center=(box[0] + box[2] // 2, box[1] + box[3] // 2))
                # Blit the text surface onto the screen at the calculated position
                self.screen.blit(text_surface, text_rect)

    def update_backend(self, box_index, symbol):
        row, col = divmod(box_index, 3)  # this returns quotient and the remainder. 3 because it is 3 x 3
        self.list_of_rows[row][col] = symbol
        self.print_board()

    def print_board(self):
        # Print which player made the move and what symbol they placed
        print("Player " + "X")
        # Loop through each row in the list of rows
        for row in self.list_of_rows:
            # Print the row
            print(row)

    def check_winner(self):
        # Check rows, columns, and diagonals
        for row in self.list_of_rows:
            if row[0] == row[1] == row[2] and row[0] != " ":
                self.game_over_bool = True
                self.update_score()
                self.blit_hud()
                return True

        for col in range(3):
            if self.list_of_rows[0][col] == self.list_of_rows[1][col] == self.list_of_rows[2][col] and  self.list_of_rows[0][col] != " ":
                self.game_over_bool = True
                self.update_score()
                self.blit_hud()
                return True

        if self.list_of_rows[0][0] == self.list_of_rows[1][1] == self.list_of_rows[2][2] and self.list_of_rows[0][ 0] != " ":
            self.game_over_bool = True
            self.update_score()
            self.blit_hud()
            return True

        if self.list_of_rows[0][2] == self.list_of_rows[1][1] == self.list_of_rows[2][0] and self.list_of_rows[0][ 2] != " ":
            self.game_over_bool = True
            self.update_score()
            self.blit_hud()
            return True

        # Check for draw
        if all(all(cell != " " for cell in row) for row in self.list_of_rows):
            self.draw = True
            self.blit_hud()
            # self.game_over()
            print(self.draw)
            print("draw")
            return True
        return False
    def game_over(self):
        self.draw_on_the_boxes()
        pygame.display.update()
        pygame.time.delay(2000)
        self.reset_game()
        print("thank you for playing")
    def reset_game(self):
        self.box_states = [None] * 9
        self.row_1 = [" ", " ", " "]
        self.row_2 = [" ", " ", " "]
        self.row_3 = [" ", " ", " "]
        self.list_of_rows = [self.row_1, self.row_2, self.row_3]
        self.draw = False
        self.game_over_bool = False

    def update_score(self):
        if self.player_turn:
            self.x_score+=1
        elif self.ai_turn:
            self.o_score +=1

    class Player:
        def __init__(self,game):
            self.game = game
            self.symbol = "X"

        def is_pressed_function(self, event):
            a, b = pygame.mouse.get_pos()
            for i, box in enumerate( [self.game.box1, self.game.box2, self.game.box3, self.game.box4, self.game.box5, self.game.box6, self.game.box7, self.game.box8, self.game.box9]):
                box_rect = pygame.Rect(box)
                if event.type == pygame.MOUSEBUTTONDOWN and box_rect.collidepoint(a, b) and self.game.box_states[i] is None:
                        self.game.box_states[i] = 'X'
                        self.game.update_backend(i, 'X')
                        self.game.collided = True
                        if self.game.check_winner():
                            self.game.game_over()
                            return


    class AI:
        def __init__(self,game):
            self.game = game
            self.symbol = "O"


        def ai_choice(self):
            # Check if all boxes are filled
            if all(box_state is not None for box_state in self.game.box_states):
                return None  # All boxes are filled, return None or handle this case as needed
            vacant = True
            while vacant:
                ai_choice = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
                if self.game.box_states[ai_choice] is None:
                    vacant = False
            return ai_choice

        def ai_press_function(self):
            pygame.time.delay(1000)
            print("AI thinking")
            ai_choice_value = self.ai_choice()  # Get AI's choice of box index
            self.game.box_states[ai_choice_value] = 'O'
            self.game.update_backend(ai_choice_value, 'O')  # Update the backend data
            if self.game.check_winner():
                self.game.game_over()
                return
