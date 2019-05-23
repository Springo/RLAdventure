import sys, pygame

pygame.init()

width = 640
height = 480
size = width, height

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

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

    def display_health(self, Surface, Rect):
        health_ratio = max(0.0, self.health / self.max_health)
        health_balance = health_ratio * 255
        bar_color = (255 - health_balance, health_balance, 0)
        pygame.draw.rect(Surface, black, Rect, 0)
        if self.health > 0:
            pygame.draw.rect(Surface, bar_color, [Rect[0], Rect[1], Rect[2] * health_ratio, Rect[3]], 0)
        pygame.draw.rect(Surface, black, Rect, 1)


if __name__ == "__main__":
    # Create health bars
    health_1 = HealthBar()

    while True:
        # Check if exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # === ACTIVATE MECHANICS ===
        health_1.change_health(-1)

        # === DRAW SCREEN ELEMENTS ===

        # background
        screen.fill(white)

        # health bars
        health_1.display_health(screen, [5, 5, 200, 25])

        # display results
        pygame.display.flip()
        clock.tick(30)
