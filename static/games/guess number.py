import random
while True:

    print('Это игра "угадай число", я загадал число случайное число из твоего диапазона. Попробуй отгадать это число с помощью моих подсказок за 7 попыток!\n')
    while True:
        try:
            meme2 = int(input('введи минимальное значение загадонного числа: '))

            meme3 = int(input('хорошо, теперь введи максимальное значение: '))
            break
        except ValueError:
            print("это должно быть число!")

    meme = random.randint(meme2, meme3)

    attempts = 0
    max_attempts = 7

    while True:
        try:
            meme1 = int(input('Введите ваше число: '))
            attempts += 1
        except ValueError:
            print('число надо а не букву!')
            continue

        if meme1 == meme:
            print(f'Подзравляю! Ты угадал число c {attempts} попытки\n')
            break
        elif meme1 > meme:
            print('меньше')
        elif meme1 < meme:
            print('больше')

        if attempts >= max_attempts:
            print(f'\nВы проиграли! Загаданное число было {meme}.')
            break

    play_again = input('еще раз? (да/нет): ').strip().lower()

    if play_again != 'да':
        print('окей')
        break