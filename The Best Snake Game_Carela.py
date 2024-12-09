import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20  
FOOD_SIZE = BLOCK_SIZE  

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0) 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)  
large_font = pygame.font.SysFont("Arial", 30)

high_score = 0


def random_color():
    """Generate a random RGB color."""
    return [random.randint(0, 255) for _ in range(3)]


def show_message_centered(lines, font, colors):
    """Display a list of messages centered on the screen with customizable colors."""
    screen.fill(BLACK)
    y_offset = HEIGHT // 4
    for line, color in zip(lines, colors):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 40
    pygame.display.flip()


def instruction_screen():
    """Display the instruction screen before the game starts."""
    show_message_centered(
        ["Welcome to The Best Snake Game", "by Kamil Carela",
         "Use the arrow keys to move the snake.",
         "Press SPACE to start the game."],
        font, [WHITE, WHITE, WHITE, WHITE]
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    return

def game_loop():
    global high_score 

    snake = [[100, 50], [80, 50], [60, 50]] 
    direction = 'RIGHT'
    change_to = direction
    food_pos = [random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE),
                random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)]
    food_spawn = True
    score = 0
    snake_color = random_color()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to

        head = snake[0]
        if direction == 'UP':
            new_head = [head[0], head[1] - BLOCK_SIZE]
        elif direction == 'DOWN':
            new_head = [head[0], head[1] + BLOCK_SIZE]
        elif direction == 'LEFT':
            new_head = [head[0] - BLOCK_SIZE, head[1]]
        elif direction == 'RIGHT':
            new_head = [head[0] + BLOCK_SIZE, head[1]]

        snake.insert(0, new_head)

        if (abs(snake[0][0] - food_pos[0]) < BLOCK_SIZE and
                abs(snake[0][1] - food_pos[1]) < BLOCK_SIZE):
            score += 1
            food_spawn = False
            snake_color = random_color()
        else:
            snake.pop()  

        if not food_spawn:
            food_pos = [random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE),
                        random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)]
            food_spawn = True

        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
                snake[0][1] < 0 or snake[0][1] >= HEIGHT):
            running = False
        for block in snake[1:]:
            if snake[0] == block:
                running = False

        screen.fill(BLACK)
        for block in snake:
            pygame.draw.rect(screen, snake_color, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], FOOD_SIZE, FOOD_SIZE))
        score_text = font.render(f"Score: {score}  High Score: {high_score}", True, WHITE)
        screen.blit(score_text, [10, 10])

        pygame.display.flip()

        clock.tick(10 + score)  

    new_high_score = False
    if score > high_score:
        high_score = score
        new_high_score = True

    lines = ["YOU DIED", "Game Over",
             f"Final Score: {score}", f"High Score: {high_score}",
             "Press R to Restart or Q to Quit"]
    colors = [RED, RED, WHITE, WHITE, WHITE]
    if new_high_score:
        lines.insert(3, "New High Score!")  
        colors.insert(3, YELLOW)  

    show_message_centered(lines, large_font, colors)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  
                    return
                elif event.key == pygame.K_q:  
                    pygame.quit()
                    sys.exit()

instruction_screen()
while True:
    game_loop()
