import sys
import random
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
damage_font = pygame.font.SysFont("centurygothic", 24, bold=True)
hud_font = pygame.font.SysFont("centurygothic", 24)

# Game meta settings
mouse_rel = False
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# Images
weapon_image_dir = ["sword.png", "axe.png", "bow.png", "wand.png", "bomb.png", "poison.png"]
weapon_images = []
for img in weapon_image_dir:
    weapon_images.append(pygame.image.load("sprites/{}".format(img)).convert_alpha())
weapon_names = ["Sword", "Axe", "Bow", "Wand", "Bomb", "Poison"]


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
    def __init__(self, Rect, color, text=None, image=None):
        self.bounds = Rect
        self.x = Rect[0]
        self.y = Rect[1]
        self.width = Rect[2]
        self.height = Rect[3]
        self.color = color
        self.text = text
        self.image = image

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

        if self.image is not None:
            image_rect = self.image.get_rect(center=(self.x + (self.width // 2), self.y + (self.height // 2)))
            screen.blit(self.image, image_rect)

        if self.text is not None:
            text_surface = button_font.render(self.text, True, black)
            text_rect = text_surface.get_rect(center=(self.x + (self.width // 2), self.y + (self.height // 2)))
            screen.blit(text_surface, text_rect)


class DamageSplash:
    def __init__(self, Rect, text=None):
        self.bounds = Rect
        self.x = Rect[0]
        self.y = Rect[1]
        self.width = Rect[2]
        self.height = Rect[3]
        self.text = text

    def display(self, Surface):
        pygame.draw.ellipse(Surface, (255, 255, 0), self.bounds, 0)
        pygame.draw.ellipse(Surface, (255, 0, 0), self.bounds, 1)
        if self.text is not None:
            text_surface = damage_font.render(self.text, True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(self.x + (self.width // 2), self.y + (self.height // 2)))
            screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    # Create meta information
    battle_timer = 0
    damage_show = False
    game_over = False

    # Create players
    #player_1 = players.HumanPlayer("Kevin")
    #player_1 = players.RandomPlayer("Bimbo")
    #player_1 = players.GreedyPlayer("Scrooge")
    player_1 = players.AnnealingGreedyPlayer("Theodore", 2)
    #player_2 = players.RandomPlayer("Bimbo")
    #player_2 = players.GreedyPlayer("Scrooge")
    #player_2 = players.GreedyPlayer("Donald", 0.01)
    #player_2 = players.GreedyPlayer("Hillary", 0.1)
    #player_2 = players.AnnealingGreedyPlayer("Theodore", 2)
    player_2 = players.UCBPlayer("Ellen", 1)
    move_1 = 0
    move_2 = 0

    # Create weapons
    weapon_damages = [random.uniform(5, 15) for _ in range(6)]
    p1_weapons = weapon_damages[:]
    random.shuffle(p1_weapons)
    p2_weapons = weapon_damages[:]
    random.shuffle(p2_weapons)
    print(p2_weapons)
    print(p1_weapons)

    # Create health bars
    health_1 = HealthBar(1000)
    health_2 = HealthBar(1000)

    # Create texts
    battle_text_1 = "Waiting for {} to make a move...".format(player_1.name)
    battle_text_2 = "Waiting for {} to make a move...".format(player_2.name)
    center_text = ""

    # Create damage splashes
    damage_splash_1 = DamageSplash([screen_width // 2 - 50, screen_height - 210, 100, 50])
    damage_splash_2 = DamageSplash([screen_width // 2 - 50, 160, 100, 50])


    # Create buttons
    button_1 = Button([100, 100, 100, 50], (255, 0, 0), "Attack")
    p1_button_color = (200, 200, 200)
    if isinstance(player_1, players.HumanPlayer):
        p1_button_color = (255, 0, 0)
    p2_button_color = (200, 200, 200)
    if isinstance(player_2, players.HumanPlayer):
        p2_button_color = (255, 0, 0)

    p1_attack_buttons = [Button([(i + 1) * (screen_width // 7) - 25, screen_height - 150, 50, 50], p1_button_color,
                        image=weapon_images[i]) for i in range(6)]
    p2_attack_buttons = [Button([(i + 1) * (screen_width // 7) - 25, 100, 50, 50], p2_button_color,
                        image=weapon_images[i]) for i in range(6)]

    # Begin game loop
    last_frame_click = False
    while True:
        # Check if exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # === WORLD MECHANICS ===

        if not game_over:
            if move_1 == 0:
                move_1 = player_1.get_move()
            if move_2 == 0:
                move_2 = player_2.get_move()
            if move_1 != 0 and battle_timer <= 0:
                battle_text_1 = "{} has chosen {}".format(player_1.name, weapon_names[move_1 - 1])
            if move_2 != 0 and battle_timer <= 0:
                battle_text_2 = "{} has chosen {}".format(player_2.name, weapon_names[move_2 - 1])

        if game_over:
            battle_text_1 = ""
            battle_text_2 = ""

        if move_1 != 0 and move_2 != 0:
            battle_timer = 30
            battle_text_1 = "{} has used {}!".format(player_1.name, weapon_names[move_1 - 1])
            battle_text_2 = "{} has used {}!".format(player_2.name, weapon_names[move_2 - 1])
            #print("Moves have been made: {} {}".format(move_1, move_2))
            damage_1 = round(max(0.0, p1_weapons[move_1 - 1] + random.gauss(0, 3)))
            damage_2 = round(max(0.0, p2_weapons[move_2 - 1] + random.gauss(0, 3)))
            health_2.change_health(-damage_1)
            health_1.change_health(-damage_2)
            damage_splash_1.text = "{}!".format(damage_2)
            damage_splash_2.text = "{}!".format(damage_1)
            #print("Damage to player 1: {}".format(damage_2))
            #print("Damage to player 2: {}".format(damage_1))
            player_1.send_feedback(damage_1)
            player_2.send_feedback(damage_2)
            move_1 = 0
            move_2 = 0
            damage_show = True

        if battle_timer == 1:
            if move_1 == 0:
                battle_text_1 = "Waiting for {} to make a move...".format(player_1.name)
            if move_2 == 0:
                battle_text_2 = "Waiting for {} to make a move...".format(player_2.name)
            damage_show = False

        if health_1.get_health() <= 0 and health_2.get_health() > 0:
            game_over = True
            center_text = "{} wins!!!".format(player_2.name)
        elif health_2.get_health() <= 0 and health_1.get_health() > 0:
            game_over = True
            center_text = "{} wins!!!".format(player_1.name)
        elif health_1.get_health() <= 0 and health_2.get_health() <= 0:
            game_over = True
            center_text = "It's a tie!"


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
                for i in range(len(p1_attack_buttons)):
                    if p1_attack_buttons[i].mouse_over():
                        player_1.send_move(i + 1)
                for i in range(len(p2_attack_buttons)):
                    if p2_attack_buttons[i].mouse_over():
                        player_2.send_move(i + 1)

        # === DRAW SCREEN ELEMENTS ===

        # background
        screen.fill(white)

        # text
        display_text(screen, "Player 2: {}".format(player_2.name), (8, 5), font_size=24, justification="corner")
        display_text(screen, "Player 1: {}".format(player_1.name), (8, screen_height - 60), justification="corner")
        display_text(screen, battle_text_2, (screen_width // 2, 75), font_size=24)
        display_text(screen, battle_text_1, (screen_width // 2, screen_height - 75), font_size=24)

        # damage splashes
        if damage_show:
            damage_splash_1.display(screen)
            damage_splash_2.display(screen)

        # health bars
        health_2.display(screen, [5, 35, screen_width - 10, 25])
        health_1.display(screen, [5, screen_height - 30, screen_width - 10, 25])

        # buttons
        for button in p1_attack_buttons:
            button.display(screen)
        for button in p2_attack_buttons:
            button.display(screen)

        # end text
        if game_over:
            display_text(screen, center_text, (screen_width // 2, screen_height // 2), font_size=48)

        # display results
        pygame.display.flip()

        # pass time
        clock.tick(30)
        if battle_timer > 0:
            battle_timer -= 1
