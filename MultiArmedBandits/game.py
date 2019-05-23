import sys, pygame

pygame.init()

# Screen settings
width = 640
height = 480
size = width, height

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
button_font = pygame.font.SysFont("centurygothic", 18)

# Game meta settings
mouse_rel = False
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


# Color transformations
def invert(color):
    return 255 - color[0], 255 - color[1], 255 - color[2]


def darken(color):
    return color[0] // 2, color[1] // 2, color[2] // 2


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
    # Create health bars
    health_1 = HealthBar(1000)

    # Create buttons
    button_1 = Button([100, 100, 100, 50], (255, 0, 0), "Test")

    last_frame_click = False
    while True:
        # Check if exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # === WORLD MECHANICS ===

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
                health_1.change_health(-10)

        # === DRAW SCREEN ELEMENTS ===

        # background
        screen.fill(white)

        # health bars
        health_1.display(screen, [5, 5, 200, 25])

        # buttons
        button_1.display(screen, gap=10)

        # display results
        pygame.display.flip()
        clock.tick(30)
