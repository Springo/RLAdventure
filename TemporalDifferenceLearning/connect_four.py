import sys
import random
import pygame
import players

pygame.init()

# Screen settings
screen_width = 640
screen_height = 640
screen_size = screen_width, screen_height

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
hud_font = pygame.font.SysFont("centurygothic", 24)

# Game meta settings
mouse_rel = False
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# Images
red_disc_image = pygame.image.load("sprites/red_disc.png").convert_alpha()
yellow_disc_image = pygame.image.load("sprites/yellow_disc.png").convert_alpha()


# Color transformations
def invert(color):
    return 255 - color[0], 255 - color[1], 255 - color[2]


def darken(color):
    return color[0] // 2, color[1] // 2, color[2] // 2


# Font display
def display_text(Surface, text, coords, font="centurygothic", font_size=24, color=black, justification="center"):
    font_obj = pygame.font.SysFont(font, font_size)
    text_surface = font_obj.render(text, True, color)
    if justification == "center":
        text_rect = text_surface.get_rect(center=(coords[0], coords[1]))
    else:
        text_rect = text_surface.get_rect(x=coords[0], y=coords[1])
    Surface.blit(text_surface, text_rect)


class Board:
    def __init__(self):
        self.grid = [[0] * 7 for _ in range(6)]
        self.heights = [5] * 7

    def input_move(self, player, move):
        if (player != 1 and player != 2) or (move < 0 or move > 6) or (self.heights[move] < 0):
            return -1
        self.grid[self.heights[move]][move] = player
        self.heights[move] -= 1
        return 0

    def mouse_over(self, Rect):
        mouse = pygame.mouse.get_pos()
        if Rect[0] < mouse[0] < Rect[0] + Rect[2] and Rect[1] < mouse[1] < Rect[1] + Rect[3]:
            return True
        return False

    def check_mouse_over(self, Rect):
        spacing_x = Rect[2] / 8.0
        for j in range(len(self.grid[0])):
            center_x = Rect[0] + int(spacing_x * (j + 1))
            column_rect = [int(center_x - (spacing_x / 2.0)), Rect[1], spacing_x, Rect[3]]
            if self.mouse_over(column_rect):
                return j
        return -1

    def display(self, Surface, Rect):
        pygame.draw.rect(Surface, (0, 0, 150), Rect, 0)
        spacing_x = Rect[2] / 8.0
        spacing_y = Rect[3] / 7.0

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                center_loc = (Rect[0] + int(spacing_x * (j+1)), Rect[1] + int(spacing_y * (i+1)))
                if self.grid[i][j] == 1:
                    image_rect = red_disc_image.get_rect(center=center_loc)
                    Surface.blit(red_disc_image, image_rect)
                elif self.grid[i][j] == 2:
                    image_rect = yellow_disc_image.get_rect(center=center_loc)
                    Surface.blit(yellow_disc_image, image_rect)
                else:
                    pygame.draw.circle(Surface, white, center_loc, 32)

        for j in range(len(self.grid[0])):
            center_x = Rect[0] + int(spacing_x * (j + 1))
            column_rect = [int(center_x - (spacing_x / 2.0)), Rect[1], spacing_x, Rect[3]]
            if self.mouse_over(column_rect):
                s = pygame.Surface((column_rect[2], column_rect[3]))
                s.set_alpha(128)
                s.fill((255, 255, 255))
                Surface.blit(s, (column_rect[0], column_rect[1]))


if __name__ == "__main__":
    # Create meta information
    game_over = False
    turn = 1

    # Create board
    board = Board()
    board_dim = [0, 100, screen_width, screen_height - 100]

    # Create players
    player_1 = players.HumanPlayer("Kevin")
    player_2 = players.HumanPlayer("Bob")

    # Create texts
    game_text = "{} to move.".format(player_1.name)

    # Begin game loop
    last_frame_click = False
    while True:
        # Check if exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # === WORLD MECHANICS ===

        if not game_over:
            if turn == 1:
                move = player_1.get_move()
            elif turn == 2:
                move = player_2.get_move()

        if move != -1:
            check = board.input_move(turn, move)
            if check == 0:
                turn = 3 - turn
                if turn == 1:
                    game_text = "{} to move.".format(player_1.name)
                elif turn == 2:
                    game_text = "{} to move.".format(player_2.name)

        # === USER MECHANICS ===

        # mouse events
        mouse_click = pygame.mouse.get_pressed()

        mouse_rel = False
        if mouse_click[0] == 1:
            last_frame_click = True
        elif last_frame_click:
            last_frame_click = False
            mouse_rel = True

        if mouse_rel:
            if not game_over:
                board_click = board.check_mouse_over(board_dim)
                if board_click != -1:
                    if turn == 1:
                        player_1.send_move(board_click)
                    elif turn == 2:
                        player_2.send_move(board_click)

        # === DRAW SCREEN ELEMENTS ===

        # background
        screen.fill(white)

        # board
        board.display(screen, board_dim)

        # text
        display_text(screen, game_text, (screen_width // 2, 50), font="centurygothic", font_size=24, color=black,
                         justification="center")

        # display results
        pygame.display.flip()

        # pass time
        clock.tick(30)
