import pygame
import sys
import random
import asyncio # Импортируем асинхронность

# 1. Инициализация и настройки (БЕЗ отступов, в самом начале)
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

# 2. Объявляем асинхронную функцию
async def main():
    # Говорим функции использовать глобальные переменные скоростей и счета
    global ball_speed_x, ball_speed_y, score_left, score_right

    # НАЧИНАЕТСЯ ИГРОВОЙ ЦИКЛ (все строки ниже сдвинуты вправо!)
    while True:
        # Проверка закрытия окна
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Считываем нажатия клавиш (теперь это внутри цикла!) ---
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= 7
        if keys[pygame.K_s] and left_paddle.bottom < height:
            left_paddle.y += 7

        # --- ИИ Правой ракетки ---
        if right_paddle.centery < ball.centery and right_paddle.bottom < height:
            right_paddle.y += 5
        if right_paddle.centery > ball.centery and right_paddle.top > 0:
            right_paddle.y -= 5

        # --- Движение мяча и физика границ ---
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= height:
            ball_speed_y *= -1

        # Физика отскока от ракеток
        if ball.colliderect(left_paddle) and ball_speed_x < 0:
            ball_speed_x *= -1
        if ball.colliderect(right_paddle) and ball_speed_x > 0:
            ball_speed_x *= -1

        # Подсчет очков при вылете за экран
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

        # --- Отрисовка графики ---
        screen.fill((0, 0, 0)) # Очищаем экран в черный

        # Рендерим и выводим счет
        text_left = game_font.render(str(score_left), True, (255, 255, 255))
        text_right = game_font.render(str(score_right), True, (255, 255, 255))
        screen.blit(text_left, (width // 2 - 100, 20))
        screen.blit(text_right, (width // 2 + 50, 20))

        # Рисуем ракетки и мяч
        pygame.draw.rect(screen, (255, 255, 255), left_paddle)
        pygame.draw.rect(screen, (255, 255, 255), right_paddle)
        pygame.draw.rect(screen, (255, 255, 255), ball)

        pygame.display.flip() # Обновляем экран
        clock.tick(60)        # Держим 60 FPS
        
        # ВАЖНО: Асинхронная пауза в самом конце цикла while!
        await asyncio.sleep(0) 

# 3. ЗАПУСК ВСЕЙ ПРОГРАММЫ (БЕЗ отступов, в самом конце файла)
asyncio.run(main())
