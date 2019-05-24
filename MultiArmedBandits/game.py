import sys
import pygame
import players

pygame.init()

# Screen settings
screen_width = 640
screen_height = 480
screen_size = screen_width, screen_height

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
button_font = pygame.font.SysFont("centurygothic", 18)
hud_font = pygame.font.SysFont("centurygothic", 24)

# Game meta settings
mouse_rel = False
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()


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


# Object classes
class HealthBar:
    def __init__(self, max_health=100):
        self.max_health = max_health
        self.health = max_health

    def set_health(self, amount):
        self.health = amount

    def change_health(self, amount):
        self.health += amount

    def get_health(self):
        return self.health

    def display(self, Surface, Rect):
        health_ratio = max(0.0, self.health / self.max_health)
        health_red = min(255, int(510 - health_ratio * 510))
        health_green = min(255, int(health_ratio * 510))
        bar_color = (health_red, health_green, 0)
        pygame.draw.rect(Surface, black, Rect, 0)
        if self.health > 0:
            pygame.draw.rect(Surface, bar_color, [Rect[0], Rect[1], Rect[2] * health_ratio, Rect[3]], 0)
        pygame.draw.rect(Surface, black, Rect, 1)


class Button:
    def __init__(self, Rect, color, text=None):
        self.bounds = Rect
        self.x = Rect[0]
        self.y = Rect[1]
        self.width = Rect[2]
        self.height = Rect[3]
        self.color = color
        self.text = text

    def mouse_over(self):
        mouse = pygame.mouse.get_pos()
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            return True
        return False

    def display(self, Surface, gap=5):
        click = pygame.mouse.get_pressed()
        hover = self.mouse_over()

        dark_color = darken(self.color)
        invert_color = invert(self.color)
        invert_dark_color = darken(invert_color)
        invert_darker_color = darken(invert_dark_color)
        small_bounds = [self.x + gap, self.y + gap, self.width - 2 * gap, self.height - 2 * gap]
        if hover:
            if click[0]:
                pygame.draw.rect(Surface, invert_darker_color, self.bounds, 0)
                pygame.draw.rect(Surface, invert_dark_color, small_bounds, 0)
            else:
                pygame.draw.rect(Surface, invert_dark_color, self.bounds, 0)
                pygame.draw.rect(Surface, invert_color, small_bounds, 0)
        else:
            pygame.draw.rect(Surface, dark_color, self.bounds, 0)
            pygame.draw.rect(Surface, self.color, small_bounds, 0)
        pygame.draw.rect(Surface, black, self.bounds, 1)
        pygame.draw.rect(Surface, black, small_bounds, 1)
        pygame.draw.line(Surface, black, (self.x, self.y), (self.x + gap, self.y + gap))
        pygame.draw.line(Surface, black, (self.x + self.width, self.y), (self.x + self.width - gap, self.y + gap))
        pygame.draw.line(Surface, black, (self.x, self.y + self.height), (self.x + gap, self.y + self.height - gap))
        pygame.draw.line(Surface, black, (self.x + self.width, self.y + self.height),
                         (self.x + self.width - gap, self.y + self.height - gap))

        if self.text is not None:
            text_surface = button_font.render(self.text, True, black)
            text_rect = text_surface.get_rect(center=(self.x + (self.width // 2), self.y + (self.height // 2)))
            screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    # Create players
    player_1 = players.HumanPlayer("Kevin")
    player_2 = players.RandomPlayer("Bimbo")
    move_1 = 0
    move_2 = 0

    # Create health bars
    health_1 = HealthBar(1000)
    health_2 = HealthBar(1000)

    # Create buttons
    button_1 = Button([100, 100, 100, 50], (255, 0, 0), "Attack")
    p1_button_color = (200, 200, 200)
    if isinstance(player_1, players.HumanPlayer):
        p1_button_color = (255, 0, 0)
    p2_button_color = (200, 200, 200)
    if isinstance(player_2, players.HumanPlayer):
        p2_button_color = (255, 0, 0)

    p1_attack_buttons = [Button([(i + 1) * (screen_width // 7) - 25, screen_height - 150, 50, 50], p1_button_color) for
                         i in range(6)]
    p2_attack_buttons = [Button([(i + 1) * (screen_width // 7) - 25, 100, 50, 50], p2_button_color) for
                         i in range(6)]

    last_frame_click = False
    while True:
        # Check if exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # === WORLD MECHANICS ===

        if move_1 == 0:
            move_1 = player_1.get_move()
        if move_2 == 0:
            move_2 = player_2.get_move()

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
            if button_1.mouse_over():
                health_1.change_health(-50)

        # === DRAW SCREEN ELEMENTS ===

        # background
        screen.fill(white)

        # text
        display_text(screen, "Player 2: {}".format(player_2.name), (8, 5), font_size=24, justification="corner")
        display_text(screen, "Player 1: {}".format(player_1.name), (8, screen_height - 60), justification="corner")

        # health bars
        health_2.display(screen, [5, 35, screen_width - 10, 25])
        health_1.display(screen, [5, screen_height - 30, screen_width - 10, 25])

        # buttons
        for button in p1_attack_buttons:
            button.display(screen)
        for button in p2_attack_buttons:
            button.display(screen)

        # display results
        pygame.display.flip()
        clock.tick(30)
