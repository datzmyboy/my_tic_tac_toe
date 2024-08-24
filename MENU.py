import pygame
from pygame.font import SysFont

# Initialize Pygame
pygame.init()

class Menu:
    def __init__(self,game):
        self.game = game
        self.run_display = True
        self.window_size = (600, 700)
        self.screen = pygame.display.set_mode(self.window_size)
        # pygame.display.set_caption("MAIN")
        self.font_title = pygame.font.SysFont(None, 80)
        self.font_player = pygame.font.SysFont(None, 20)
        #(X , Y ,Width of pixels, Height of pixels)
        self.player2box = (self.window_size[0] / 2 - 75, self.window_size[1] / 2 - 100, 150, 50)
        self.player1box = (self.window_size[0] / 2 - 75, self.window_size[1] / 2 + 20, 150, 50)
        self.is_pressed_box1 = False
        self.is_pressed_box2 = False

    def draw_objects(self):
        # Render the text "MENU"
        text_surface = self.font_title.render("MY_TICTACTOE", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.window_size[0] / 2, self.window_size[1] / 2 - 200))
        # Blit the text surface onto the screen at the center
        self.screen.blit(text_surface, text_rect)
        self.activate_box()
        self.draw_box()
        pygame.display.update()  # Update the display

    def draw_box(self):
        text = "PLAYER 1"
        text2 = "PLAYER 2"
        pygame.draw.rect(self.screen, (255, 0, 255), self.player2box, 5)
        pygame.draw.rect(self.screen, (255, 0, 255), self.player1box, 5)
        # for box 1
        text_surface = self.font_player.render(text, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(self.player2box[0] + self.player2box[2] / 2, self.player2box[1] + self.player2box[3] / 2))
        # box 2
        text_surface2 = self.font_player.render(text2, True, (255, 0, 0))
        text_rect2 = text_surface.get_rect(center=(self.player1box[0] + self.player1box[2] / 2, self.player1box[1] + self.player1box[3] / 2))

        self.screen.blit(text_surface, text_rect)
        self.screen.blit(text_surface2, text_rect2)
    # this method is responsible for coloring the boxes if the cursor is hovering on it
    def activate_box(self):
        a, b = pygame.mouse.get_pos()
        box_x, box_y, box_w, box_h = self.player2box
        box1_x, box1_y, box1_w, box1_h = self.player1box

        if box_x <= a <= box_x + box_w and box_y <= b <= box_y + box_h:
            pygame.draw.rect(self.screen, (0, 180, 180), self.player2box)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), self.player2box)

        if box1_x <= a <= box1_x + box1_w and box1_y <= b <= box1_y + box1_h:
            pygame.draw.rect(self.screen, (0, 180, 180), self.player1box)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), self.player1box)

    def clicked_boxes(self, event):
    # box will change to true if pressed
        a, b = pygame.mouse.get_pos()
        playerbox2 = pygame.Rect(self.player2box)
        playerbox1 = pygame.Rect(self.player1box)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if playerbox1.collidepoint(a, b):
                self.is_pressed_box1 = True
                self.is_pressed_box2 = False  # Reset other button state
            elif playerbox2.collidepoint(a, b):
                self.is_pressed_box2 = True
                self.is_pressed_box1 = False  # Reset other button state

    def end_game(self):
        self.run_display = False
        self.game.running = False
        self.game.playing = False
        self.game.game2.playing2 = False
        self.game.game2.running2 = False

    def end_game2(self):
        self.run_display = False
        self.game.running = False
        self.game.playing = False
        self.game.game2.playing2 = False
        self.game.game2.running2 = False

    def set_caption(self,text):
        pygame.display.set_caption(text)

    def display_menu(self):
        self.set_caption("Main")
        self.run_display = True
        # self.game.reset_game()
        while self.run_display:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked_boxes(event)
                    if self.is_pressed_box1:
                        self.run_display = False
                        self.game.playing = True
                        print("bye bye")
                        print("game on")
                        print("player 2 game on")
                    elif self.is_pressed_box2:
                        print("player 1 game on ")
                        self.run_display = False
                        self.game.game2.playing2 = True
            self.screen.fill((0, 0, 0))
            self.draw_objects()
            pygame.display.update()

    # Create an instance of the Menu class and draw the text

#
# m = Menu()
# m.display_menu()