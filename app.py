from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
boggle_game = Boggle()
app.config['SECRET_KEY'] = 'asdfasdfsdfsdfsdf'


@app.route('/')
def game_board():

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    numplays = session.get('numplays', 0)
    return render_template('index.html', board=board, highscore=highscore, numplays=numplays)


@app.route('/check-word')
def check_word():
    """take the word from the params of our axios GET request and check it against the board we have saved in session"""

    word = request.args['word']
    board = session['board']
    response_string = boggle_game.check_valid_word(board, word)
    # this var will be one of three strings: 'ok', 'not-a-word', 'not-on-board'

    return jsonify({'response': response_string})


@app.route('/end-game', methods=['POST'])
def end_game():
    """get the axios post score from the endgame function and update highscore in session"""
    score = request.json['score']

    # get current highscore from session, if no high score saved in session set vairable to zero
    highscore = session.get('highscore', 0)
    numplays = session.get('numplays', 0)

    # update highscore in session
    session['highscore'] = max(score, highscore)
    session['numplays'] = numplays + 1

    return 'game over'
