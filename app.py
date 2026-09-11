from flask import Flask, render_template, request, redirect

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

@app.route('/play_guess')
def play_guess():
    return render_template('guess_game.html')

@app.route('/msg_success')
def msg_success():
    return render_template('msg_success.html')

@app.route('/msg_error')
def msg_error():
    return render_template('msg_error.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        name = request.form.get('username')
        text = request.form.get('usertext')
        
        if not name or not text:
            return redirect('/msg_error')
            
        path = '/home/wastery/Wastery-portfolio/messages.txt'
        
        with open(path, 'a', encoding='utf-8') as file:
            file.write(f"Имя: {name} | Отзыв: {text}\n------------------------------\n")
            
        return redirect('/msg_success')
        
    except Exception:
        return redirect('/msg_error')

if __name__ == '__main__':
    app.run(debug=True)
