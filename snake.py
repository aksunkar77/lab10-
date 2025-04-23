# Snake Game with PostgreSQL integration

import pygame
import psycopg2
import sys
import random
from datetime import datetime

def connect_db():
    return psycopg2.connect(
        host="localhost",
        dbname="phonebook_db",
        user="postgres",
        password="Aksu"
    )

def get_user(username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM game_user WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        return user[0]
    else:
        cur.execute("INSERT INTO game_user (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id


def save_score(user_id, level, score):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_score (user_id, level, score) VALUES (%s, %s, %s)", (user_id, level, score))
    conn.commit()
    conn.close()

#game code
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)


WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)


snake_block = 20
snake_speed = 15


def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

def game_loop(username):
    user_id = get_user(username)

    game_over = False
    game_close = False

    x = 300
    y = 200
    dx = 0
    dy = 0

    snake = []
    length = 1

    food_x = round(random.randrange(0, 600 - snake_block) / 20.0) * 20.0
    food_y = round(random.randrange(0, 400 - snake_block) / 20.0) * 20.0

    level = 1
    score = 0

    while not game_over:
        while game_close:
            screen.fill(WHITE)
            msg = font.render("Game Over! Press Q to Quit or R to Restart", True, RED)
            screen.blit(msg, [50, 180])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        save_score(user_id, level, score)
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop(username)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score(user_id, level, score)
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -snake_block
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = snake_block
                    dy = 0
                elif event.key == pygame.K_UP:
                    dy = -snake_block
                    dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = snake_block
                    dx = 0
                elif event.key == pygame.K_p:
                    save_score(user_id, level, score)
                    print("Paused and saved")

        x += dx
        y += dy

        if x >= 600 or x < 0 or y >= 400 or y < 0:
            game_close = True

        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food_x, food_y, snake_block, snake_block])
        snake_head = [x, y]
        snake.append(snake_head)
        if len(snake) > length:
            del snake[0]

        for segment in snake[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake)
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, [10, 10])

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, 600 - snake_block) / 20.0) * 20.0
            food_y = round(random.randrange(0, 400 - snake_block) / 20.0) * 20.0
            length += 1
            score += 10

        clock.tick(snake_speed + level)

    pygame.quit()
    sys.exit()

#starting
username = input("Enter your username: ")
game_loop(username)
