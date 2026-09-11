from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'wastery_secret_key_miku_dev_terminal'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('username')
    text = request.form.get('usertext')
    
    with open('messages.txt', 'a', encoding='utf-8') as file:
        file.write(f"Имя: {name} | Отзыв: {text}\n")
        file.write("-" * 30 + "\n")
        
    print(f"--- ПОЛУЧЕН НОВЫЙ ОТЗЫВ ОТ {name}! ---")
    
    return redirect('/projects')

import random

# Страница самой онлайн-игры
@app.route('/play_guess')
def play_guess():
    # Если игра только началась и числа в памяти нет — генерируем его
    if 'secret_number' not in session:
        session['secret_number'] = random.randint(1, 100) # пока зафиксируем от 1 до 100
        session['attempts'] = 0
        session['message'] = 'Компьютер загадал число от 1 до 100. Угадай его!'
        session['game_over'] = False

    return render_template('guess_game.html', 
                           message=session['message'], 
                           attempts=session['attempts'],
                           game_over=session['game_over'])

@app.route('/check_number', methods=['POST'])
def check_number():
    try:
        user_guess = int(request.form.get('user_number'))
        session['attempts'] += 1
        
        if user_guess == session['secret_number']:
            session['message'] = f'Поздравляю! Вы угадали число за {session["attempts"]} попыток!'
            session['game_over'] = True
        elif user_guess < session['secret_number']:
            session['message'] = f'Загаданное число БОЛЬШЕ, чем {user_guess}!'
        else:
            session['message'] = f'Загаданное число МЕНЬШЕ, чем {user_guess}!'

        if session['attempts'] >= 7 and not session['game_over']:
            session['message'] = f'Попытки кончились! Вы проиграли. Было загадано число {session["secret_number"]}.'
            session['game_over'] = True
            
    except ValueError:
        session['message'] = 'Пожалуйста, введите корректное число!'

    return redirect('/play_guess')

@app.route('/reset_guess')
def reset_guess():
    session.pop('secret_number', None)
    return redirect('/play_guess')

@app.route('/play_pong')
def play_pong():
    return render_template('pong_game.html')

if __name__ == '__main__':
    app.run(debug=True)