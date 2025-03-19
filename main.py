from classes import Dice, Person, Gender, Player, Match
import pygame
import random

# Inicializace pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dice Game")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

bet = 100

# Vytvoření hráčů
host_player = Player("PC", Gender.male)
guest_player = Player("You", Gender.female)

# Vytvoření zápasu
match = Match(host_player, guest_player)

# Načtení obrázků kostek
dices_img = [pygame.image.load(f'img/kostka{i}.png') for i in range(1, 7)]

# Třída pro vizuální reprezentaci kostky
class DiceSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.value = 1  # Výchozí hodnota kostky
        self.image = dices_img[self.value - 1]
        self.rect = self.image.get_rect(center=(x, y))

    def update_value(self, value):
        self.value = value
        self.image = dices_img[self.value - 1]  # Aktualizace obrázku

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Přidání černého rámečku


def shuffle(dice_sprites, frames=10, delay=90):
    for i in range(frames):
        for dice in dice_sprites[:2]:  # První dvě kostky
            dice.update_value(random.randint(1, 6))
        screen.fill(WHITE)
        for dice in dice_sprites:
            dice.draw(screen)
        shuffle_text()
        pygame.display.flip()
        pygame.time.delay(delay)


def shuffle_player(dice_sprites, frames=10, delay=150):
    for i in range(frames + 5):  # Třetí kostka se míchá déle
        dice_sprites[2].update_value(random.randint(1, 6))
        screen.fill(WHITE)
        for dice in dice_sprites:
            dice.draw(screen)
        shuffle_text()
        pygame.display.flip()
        pygame.time.delay(delay)


# Funkce pro překreslení obrazovky
def redraw_screen(dice_sprites, won):
    screen.fill(WHITE)
    for dice in dice_sprites:
        dice.draw(screen)
    draw_text(won)
    pygame.display.flip()


# Funkce pro vykreslení uživatelského rozhraní
def draw_text(won):
    # Zobrazení skóre
    font = pygame.font.Font(None, 50)
    score_text = font.render(f"{host_player.nickname}: {match.hp_points} - {guest_player.nickname}: {match.gp_points}",
                             True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 50))

    round_score_text(won)

    coins_text()

    # Zobrazení pokynů pro hráče
    instruction_surface = font.render(instruction_text, True, BLACK)
    screen.blit(instruction_surface, (WIDTH // 2 - instruction_surface.get_width() // 2, HEIGHT - 100))

    # Vykreslení tlačítek
    rules_button.draw(screen)
    reset_button.draw(screen)


def shuffle_text():
    font = pygame.font.Font(None, 50)
    text = font.render(f"....SHUFFLING.... ", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))

def round_score_text(won):
    font = pygame.font.Font(None, 40)
    if won == 2:
        text = font.render("You WON!", True, GREEN)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 110))
    elif won == 1:
        text = font.render("You LOST...", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 110))
    else:
        pass

def coins_text():
    font = pygame.font.Font(None, 40)
    text = font.render(f"Coins: {guest_player.coins}", True, BLACK)
    screen.blit(text, (30, 400))
    bet_text = font.render(f"Bet coins: {bet}", True, BLACK)
    screen.blit(bet_text, (30, 450))

# Tlačítko pro zobrazení pravidel
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()


# Funkce pro zobrazení pravidel
def show_rules():
    rules = [
        "Host is playing with 2 dices, you play with 1.",
        "If the number on your dice is between the numbers on host's dices, you win!",
        "You can increase your bet with UP arrow and decrease it with DOWN arrow.",
        "You can play by pressing the spacebar.",
        "The game end after you loose all your coins!!"
        "Your chances to win are lower than 50%, so good luck!"
    ]
    screen.fill(WHITE)
    font = pygame.font.Font(None, 30)
    y_offset = 150
    for rule in rules:
        rule_surface = font.render(rule, True, BLACK)
        screen.blit(rule_surface, (WIDTH // 2 - rule_surface.get_width() // 2, y_offset))
        y_offset += 40
    pygame.display.flip()
    pygame.time.delay(9000)  # Pravidla se zobrazí na 5 sekund

def reset_game():
    global match
    match = Match(host_player, guest_player)

def end_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 80)
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

# Vytvoření objektů kostek
host_dice1 = DiceSprite(WIDTH // 3, HEIGHT // 3)
host_dice2 = DiceSprite(2 * WIDTH // 3, HEIGHT // 3)
guest_dice = DiceSprite(WIDTH // 2, 2 * HEIGHT // 3)

dice_sprites = [host_dice1, host_dice2, guest_dice]


# Vytvoření tlačítka pravidel
rules_button = Button(WIDTH - 150, HEIGHT - 50, 140, 40, "Rules", show_rules)
reset_button = Button(WIDTH - 300, HEIGHT - 50, 140, 40, "Restart", reset_game)

# Hlavní smyčka hry
running = True
current_roll = 0  # Sledování aktuálního hodu
instruction_text = "You are playing! Press spacebar."  # Počáteční instrukce

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if bet < guest_player.coins:
                    bet += 100
                    draw_text(match.n)
            if event.key == pygame.K_DOWN:
                if bet >= 200:
                    bet -= 100
                    draw_text(match.n)
            if event.key == pygame.K_SPACE:
                if current_roll == 0:
                    match.play(int(bet))  # Použití metody play pro provedení hodu a vyhodnocení
                    shuffle(dice_sprites)  # Zamíchání kostek před hodem

                    host_dice1.update_value(match.get_hp1())
                    host_dice2.update_value(match.get_hp2())
                    shuffle_player(dice_sprites)
                    guest_dice.update_value(match.get_gp())
                    current_roll = 0  # Resetuje cyklus hodů
                    bet = 100
        elif event.type == pygame.MOUSEBUTTONDOWN:
            rules_button.click(event.pos)
            reset_button.click(event.pos)

    redraw_screen(dice_sprites, match.n)

    pygame.display.flip()
    if guest_player.coins < 100:
        pygame.time.delay(1000)
        end_screen()
        running = False

pygame.quit()


