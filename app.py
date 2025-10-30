from flask import Flask, render_template, request, redirect, url_for, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# You can replace or extend this list with words from your original hangman.py
WORDS = ["python", "hangman", "developer", "intelligence", "machine", "learning", "flask"]

MAX_ATTEMPTS = 6

def start_new_game():
    word = random.choice(WORDS)
    session['word'] = word
    session['guessed'] = []
    session['wrong'] = []
    session['attempts_left'] = MAX_ATTEMPTS

def display_word(word, guessed):
    return ' '.join([c if c in guessed else '_' for c in word])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    start_new_game()
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'word' not in session:
        start_new_game()

    word = session['word']
    guessed = session.get('guessed', [])
    wrong = session.get('wrong', [])
    attempts_left = session.get('attempts_left', MAX_ATTEMPTS)

    message = None

    if request.method == 'POST':
        guess = request.form.get('guess', '').strip().lower()
        if not guess or len(guess) != 1 or not guess.isalpha():
            message = "Please enter a single letter."
        elif guess in guessed or guess in wrong:
            message = f"You already tried '{guess}'."
        else:
            if guess in word:
                guessed.append(guess)
                session['guessed'] = guessed
                message = f"Good guess: '{guess}'"
            else:
                wrong.append(guess)
                session['wrong'] = wrong
                session['attempts_left'] = attempts_left - 1
                attempts_left = session['attempts_left']
                message = f"Wrong guess: '{guess}'"

    finished = all(c in guessed for c in word)
    lost = attempts_left <= 0 and not finished

    return render_template('game.html',
                           word_display=display_word(word, guessed),
                           guessed=guessed,
                           wrong=wrong,
                           attempts_left=attempts_left,
                           finished=finished,
                           lost=lost,
                           secret_word=word if (finished or lost) else None,
                           message=message)

if __name__ == '__main__':
    app.run(debug=True)

