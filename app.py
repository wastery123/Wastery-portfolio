from flask import Flask, render_template, request, redirect
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/play_pong')
def play_pong():
    return render_template('pong_game.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('username')
    text = request.form.get('usertext')
    with open('/tmp/messages.txt', 'a', encoding='utf-8') as file:
        file.write(f"Имя: {name} | Отзыв: {text}\n------------------------------\n")
    return redirect('/projects')

@app.route('/play_guess')
def play_guess():
    secret = request.args.get('secret', type=int)
    attempts = request.args.get('attempts', type=int, default=0)
    message = request.args.get('message', default='Компьютер загадал число от 1 до 100. Угадай его!')
    game_over = request.args.get('game_over', default='False') == 'True'
    
    if not secret:
        secret = random.randint(1, 100)
        return redirect(f'/play_guess?secret={secret}&attempts=0&message=Компьютер загадал число от 1 до 100. Угадай его!')

    return render_template('guess_game.html', secret=secret, attempts=attempts, message=message, game_over=game_over)

@app.route('/check_number', methods=['POST'])
def check_number():
    try:
        user_guess = int(request.form.get('user_number'))
        secret = request.form.get('secret', type=int)
        attempts = request.form.get('attempts', type=int, default=0) + 1
        game_over = False
        
        if user_guess == secret:
            message = f'Поздравляю! Вы угадали число за {attempts} попыток!'
            game_over = True
        elif user_guess < secret:
            message = f'Загаданное число БОЛЬШЕ, чем {user_guess}!'
        else:
            message = f'Загаданное число МЕНЬШЕ, чем {user_guess}!'
            
        if attempts >= 7 and not game_over:
            message = f'Попытки кончились! Вы проиграли. Было загадано число {secret}.'
            game_over = True
            
    except (ValueError, TypeError):
        secret = request.form.get('secret', type=int)
        attempts = request.form.get('attempts', type=int, default=0)
        message = 'Пожалуйста, введите корректное число!'
        game_over = False

    return render_template('guess_game.html', secret=secret, attempts=attempts, message=message, game_over=game_over)

if __name__ == '__main__':
    app.run(debug=True)