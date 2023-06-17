import pygame
import random
import math
from pygame import mixer

mixer.init()
pygame.init()

scale_factor = 1.5
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Space Shooter Game")

background = pygame.transform.scale(pygame.image.load("./images/background.png").convert(), (1500, 1200))
player_image = pygame.image.load("./images/arcade.png").convert_alpha()

enemy_image = []
enemy_x = []
enemy_y = []
enemy_speed_x = []
enemy_speed_y = []

no_of_enemy = 8

for i in range(no_of_enemy):
    enemy_image.append(pygame.image.load("./images/enemy.png").convert_alpha())
    enemy_x.append(random.randint(0, 936))
    enemy_y.append(random.randint(30, 150))
    enemy_speed_x.append(-1)
    enemy_speed_y.append(150)

score = 0
score_sound = mixer.Sound("./audio/point.mp3")

bullet_image = pygame.image.load("./images/bullet.png").convert_alpha()
bullets = []

space_x = 450
space_y = 600
change_x = 0
running = True
game_started = False
game_over = False

font = pygame.font.SysFont("Arial", 32, "bold")

def score_text():
    image_gameover = font.render(f"Score: {score}", True, "white")
    screen.blit(image_gameover, (10, 10))

font_gameover = pygame.font.SysFont("Arial", 66, "bold")

def show_game_over():
    image = font_gameover.render("GAME OVER!!", True, "red")
    screen.blit(image, (260, 150))

font_restart = pygame.font.SysFont("Arial", 32, "bold")

def display_restart_message():
    message = font_restart.render("Press R to RESTART", True, "green")
    screen.blit(message, (300, 350))

font_game_start = pygame.font.SysFont("Arial", 54, "bold")

def display_game_start_message():
    message = font_game_start.render("Press Enter to START", True, "green")
    screen.blit(message, (250, 350))

# New function for displaying instructions
font_instructions = pygame.font.SysFont("Arial", 24)

instruction_page = True

def display_instructions():
    instructions = [
        "Instructions:",
        "1. Move spaceship left: Press the A key",
        "2. Move spaceship right: Press the D key",
        "3. Fire bullets: Press and hold the mouse key",
        "4. Go to next page: Press the RIGHT ARROW KEY(K_RIGHT)"
    ]

    # Render and display instructions
    for i, text in enumerate(instructions):
        instruction = font_instructions.render(text, True, "white")
        screen.blit(instruction, (250, 200 + (i * 50)))

def start_game():
    global game_started
    game_started = True
    mixer.music.load("./audio/background.mp3")
    mixer.music.play(-1)

def restart_game():
    global score, bullets, space_x, change_x, game_started, game_over

    score = 0
    bullets = []
    space_x = 450
    change_x = 0
    game_started = False
    game_over = False

    for i in range(no_of_enemy):
        enemy_x[i] = random.randint(0, 936)
        enemy_y[i] = random.randint(30, 150)

bullet_delay = 0
bullet_delay_limit = 25
fire_bullet = False

while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if instruction_page:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    instruction_page = False

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    change_x = -3
                if event.key == pygame.K_d:
                    change_x = 3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and change_x == -3:
                    change_x = 0
                if event.key == pygame.K_d and change_x == 3:
                    change_x = 0

                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if not game_started:
                        start_game()

            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    fire_bullet = True
                    bullet_sound = mixer.Sound("./audio/bullet_shoting.mp3")
                    bullet_sound.play()

            if event.type == pygame.MOUSEBUTTONUP:
                if not game_over:
                    fire_bullet = False

    if not instruction_page:
        if game_started:
            if not game_over:
                space_x += change_x
                if space_x <= 0:
                    space_x = 0
                elif space_x >= 936:
                    space_x = 936

            if fire_bullet and not game_over:
                bullet_delay += 1
                if bullet_delay >= bullet_delay_limit:
                    bullets.append([space_x + 16, 580])
                    bullet_delay = 0

            for i in range(no_of_enemy):
                if enemy_y[i] > 590:
                    for j in range(no_of_enemy):
                        enemy_y[j] = 2000
                    game_over = True
                    break
                enemy_x[i] += enemy_speed_x[i]
                if enemy_x[i] <= 0 or enemy_x[i] >= 936:
                    enemy_speed_x[i] *= -1
                    enemy_y[i] += enemy_speed_y[i]

                for bullet in bullets:
                    bullet_x = bullet[0]
                    bullet_y = bullet[1]
                    distance = math.sqrt(math.pow(bullet_x - enemy_x[i], 2) + math.pow(bullet_y - enemy_y[i], 2))
                    if distance < 29:
                        bullets.remove(bullet)
                        enemy_x[i] = random.randint(0, 936)
                        enemy_y[i] = random.randint(30, 150)
                        old_score = score
                        score += 1
                        if score != old_score:
                            score_sound.play()

                # Check if enemy collides with spaceship
                if enemy_x[i] - 64 <= space_x <= enemy_x[i] + 64 and enemy_y[i] + 64 >= space_y >= enemy_y[i]:
                    game_over = True
                    break

                screen.blit(enemy_image[i], (enemy_x[i], enemy_y[i]))

            for bullet in bullets:
                if not game_over:
                    bullet[1] -= 8
                    if bullet[1] <= 0:
                        bullets.remove(bullet)
                    else:
                        screen.blit(bullet_image, (bullet[0], bullet[1]))

            screen.blit(player_image, (space_x, space_y))
            score_text()

            if game_over:
                show_game_over()
                display_restart_message()

        else:
            display_game_start_message()

    else:
        display_instructions()

    pygame.display.update()



