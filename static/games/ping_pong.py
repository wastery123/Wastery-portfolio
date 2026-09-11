import pygame
import sys
import random
import asyncio

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Мой первый Пинг-Понг")
clock = pygame.time.Clock()

paddle_width = 15
paddle_height = 100

left_paddle = pygame.Rect(50, height // 2 - paddle_height // 2, paddle_width, paddle_height)
right_paddle = pygame.Rect(width - 50 - paddle_width, height // 2 - paddle_height // 2, paddle_width, paddle_height)
ball = pygame.Rect(width // 2 - 7, height // 2 - 7, 15, 15)

ball_speed_x = 5
ball_speed_y = 5
score_left = 0
score_right = 0
game_font = pygame.font.Font(None, 74)

async def main():
    global ball_speed_x, ball_speed_y, score_left, score_right

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= 7
        if keys[pygame.K_s] and left_paddle.bottom < height:
            left_paddle.y += 7

        if right_paddle.centery < ball.centery and right_paddle.bottom < height:
            right_paddle.y += 5
        if right_paddle.centery > ball.centery and right_paddle.top > 0:
            right_paddle.y -= 5

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= height:
            ball_speed_y *= -1

        if ball.colliderect(left_paddle) and ball_speed_x < 0:
            ball_speed_x *= -1
        if ball.colliderect(right_paddle) and ball_speed_x > 0:
            ball_speed_x *= -1

        if ball.left <= 0:
            score_right += 1
            ball.x = width // 2 - 7
            ball.y = height // 2 - 7
            ball_speed_x *= -1
        if ball.right >= width:
            score_left += 1
            ball.x = width // 2 - 7
            ball.y = height // 2 - 7
            ball_speed_x *= -1

        screen.fill((0, 0, 0))

        text_left = game_font.render(str(score_left), True, (255, 255, 255))
        text_right = game_font.render(str(score_right), True, (255, 255, 255))
        screen.blit(text_left, (width // 2 - 100, 20))
        screen.blit(text_right, (width // 2 + 50, 20))

        # Рисуем ракетки и мяч
        pygame.draw.rect(screen, (255, 255, 255), left_paddle)
        pygame.draw.rect(screen, (255, 255, 255), right_paddle)
        pygame.draw.rect(screen, (255, 255, 255), ball)

        pygame.display.flip()
        clock.tick(60)
        
        await asyncio.sleep(0) 

asyncio.run(main())
