import pygame
import time
import random

pygame.init()
pygame.mixer.init()

# Warna
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by dwikadio')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)

game_sound = pygame.mixer.Sound("cottagecore-17463.mp3")
eat_sound_1 = pygame.mixer.Sound("eating-sound-effect-36186.mp3")
eat_sound_2 = pygame.mixer.Sound("heavy_swallow.mp3")
crash_sound = pygame.mixer.Sound("bang-crash-103775.mp3")


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(dis, red, [obstacle[0], obstacle[1], snake_block, snake_block])


def gameLoop(big_foodx=None, big_foody=None):
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    score = 0

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    def generate_big_food():
        nonlocal big_foodx, big_foody
        big_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        big_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    def generate_obstacles(num_obstacles):
        obstacles = []
        for _ in range(num_obstacles):
            obstacle_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            obstacle_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            obstacles.append([obstacle_x, obstacle_y])
        return obstacles

    big_food_exists = False
    big_food_counter = 0
    obstacles = generate_obstacles(10)

    while not game_over:
        game_sound.play()

        while game_close:
            dis.fill(blue)
            message("You Shit! Press C-Play Again or Q-Quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change

        if x1 >= dis_width:
            x1 = 0
        elif x1 < 0:
            x1 = dis_width - snake_block

        if y1 >= dis_height:
            y1 = 0
        elif y1 < 0:
            y1 = dis_height - snake_block

        dis.fill(blue)

        # Menggambar rintangan
        draw_obstacles(obstacles)

        if not big_food_exists:
            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        else:
            pygame.draw.rect(dis, yellow, [big_foodx, big_foody, snake_block * 2, snake_block * 2])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_List.append(snake_head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_head:
                game_close = True
                crash_sound.play()

        # Cek apakah snake menabrak rintangan
        for obstacle in obstacles:
            if obstacle == snake_head:
                game_close = True
                crash_sound.play()

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            score += 1
            eat_sound_1.play()
            if score % 10 == 0:
                big_food_exists = True
                big_food_counter = 0
                generate_big_food()
            else:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

            Length_of_snake += 1

        if big_food_exists and x1 == big_foodx and y1 == big_foody:
            big_food_exists = False
            big_food_counter = 0
            score += 5
            Length_of_snake += 5
            eat_sound_2.play()

        big_food_counter += 1
        if big_food_counter > 100:
            big_food_exists = False

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
