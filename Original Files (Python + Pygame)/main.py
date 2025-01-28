import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700
PLAY_AREA = 450

BLACK, WHITE, RED = (0,0,0), (255,255,255), (200, 0, 50)
GREY = (45,45,45)

SNAKE_SIZE = 50

FPS = 8
TIME_DELAY = 0

snake_x = 250
snake_y = 300

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

snake = [
    pygame.Rect(snake_x, snake_y, SNAKE_SIZE, SNAKE_SIZE)
]

clock = pygame.time.Clock()

font = pygame.font.Font(None, 40)

score = 0

direction = None

def generate_food(snake):
    possible_coordinates = []
    for i in range(0, SCREEN_WIDTH - PLAY_AREA, SNAKE_SIZE):
        possible_coordinates.append(i)

    random_food_x = random.choice(possible_coordinates)
    random_food_y = random.choice(possible_coordinates)

    food = random_food_x, random_food_y

    snake_coordinates = []
    for snake_check in snake:
        snake_check_x = snake_check.x
        snake_check_y = snake_check.y
        snake_coordinate = snake_check_x, snake_check_y
        snake_coordinates.append(snake_coordinate)

    check = True

    while check:
        if food not in snake_coordinates:
            check = False
        else:
            random_food_x = random.choice(possible_coordinates)
            random_food_y = random.choice(possible_coordinates)

            food = random_food_x, random_food_y

    return food

food = generate_food(snake)

mouse_buttons = [
    # Left
    pygame.Rect((SCREEN_WIDTH / 2 - SNAKE_SIZE / 2) - SNAKE_SIZE*1.5, (PLAY_AREA + (SCREEN_HEIGHT - PLAY_AREA) / 2) - SNAKE_SIZE / 2, SNAKE_SIZE, SNAKE_SIZE),
    # up
    pygame.Rect((SCREEN_WIDTH / 2 - SNAKE_SIZE / 2), (PLAY_AREA + (SCREEN_HEIGHT - PLAY_AREA) / 2) - SNAKE_SIZE * 1.5 - SNAKE_SIZE / 2, SNAKE_SIZE, SNAKE_SIZE),
    # Right
    pygame.Rect((SCREEN_WIDTH / 2 - SNAKE_SIZE / 2) + SNAKE_SIZE * 1.5,(PLAY_AREA + (SCREEN_HEIGHT - PLAY_AREA) / 2) - SNAKE_SIZE / 2, SNAKE_SIZE, SNAKE_SIZE),
    # down
    pygame.Rect((SCREEN_WIDTH / 2 - SNAKE_SIZE / 2), (PLAY_AREA + (SCREEN_HEIGHT - PLAY_AREA) / 2) + SNAKE_SIZE * 1.5 - SNAKE_SIZE / 2, SNAKE_SIZE,SNAKE_SIZE)
]

new_game = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
            # check left direction check
            if event.button == 1 and mouse_click.colliderect(mouse_buttons[0]) and direction != "right":
                direction = "left"
            # check up direction click
            if event.button == 1 and mouse_click.colliderect(mouse_buttons[1]) and direction != "down":
                direction = "up"
            # check right direction click
            if event.button == 1 and mouse_click.colliderect(mouse_buttons[2]) and direction != "left":
                direction = "right"
            # check down direction click
            if event.button == 1 and mouse_click.colliderect(mouse_buttons[3]) and direction != "up":
                direction = "down"


    if new_game:
        direction = None
        snake_x = 250
        snake_y = 400
        snake = [
            pygame.Rect(snake_x, snake_y, SNAKE_SIZE, SNAKE_SIZE)
        ]
        new_game = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != "down":
        direction = "up"
    elif keys[pygame.K_DOWN] and direction != "up":
        direction = "down"
    elif keys[pygame.K_RIGHT] and direction != "left":
        direction = "right"
    elif keys[pygame.K_LEFT] and direction != "right":
        direction = "left"

    score_text = f"Score: {score}"
    score_surface = font.render(score_text, True, WHITE)

    if direction:
        snake_head = snake[0].copy()
        if direction == "up":
            if snake_head.y - SNAKE_SIZE < 0:
                snake_head.y = PLAY_AREA - SNAKE_SIZE
            else:
                snake_head.y -= SNAKE_SIZE
            pygame.time.delay(TIME_DELAY)
        if direction == "down":
            if snake_head.y + SNAKE_SIZE > PLAY_AREA - SNAKE_SIZE:
                snake_head.y = 0
            else:
                snake_head.y += SNAKE_SIZE
            pygame.time.delay(TIME_DELAY)
        if direction == "right":
            if snake_head.x  + SNAKE_SIZE > PLAY_AREA - SNAKE_SIZE:
                snake_head.x = 0
            else:
                snake_head.x += SNAKE_SIZE
            pygame.time.delay(TIME_DELAY)
        if direction == "left":
            if snake_head.x - SNAKE_SIZE < 0:
                snake_head.x = PLAY_AREA - SNAKE_SIZE
            else:
                snake_head.x -= SNAKE_SIZE
            pygame.time.delay(TIME_DELAY)

        snake.insert(0, snake_head)

        pass_once = True

        for section in snake:
            if pass_once:
                pass
                pass_once = False
            else:
                if snake_head.x == section.x and snake_head.y == section.y:
                    new_game = True
                    score = 0

        if snake_head.x == food[0] and snake_head.y == food[1]:
            food = generate_food(snake)
            score += 1
        else:
            snake.pop()

    screen.fill(BLACK)

    pygame.draw.rect(screen, RED, (food[0], food[1], SNAKE_SIZE, SNAKE_SIZE))

    for section in snake:
        pygame.draw.rect(screen, WHITE, section)

    pygame.draw.rect(screen, GREY, (PLAY_AREA, 0, SCREEN_WIDTH - PLAY_AREA, SCREEN_HEIGHT))
    pygame.draw.rect(screen, GREY, (0, PLAY_AREA, SCREEN_WIDTH, SCREEN_HEIGHT - PLAY_AREA))

    for button in mouse_buttons:
        pygame.draw.rect(screen, WHITE, button)

    screen.blit(score_surface, (PLAY_AREA + 20, 10))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()