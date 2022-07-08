from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    # write test for every view function / feature
    def setUp(self):
        """do before every test"""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_game_board(self):
        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text=True)

            self.assertIn('Score: 0', html)
            self.assertIn('Times Played: 0', html)
            self.assertIn('High Score: 0', html)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('numplays'))

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["T", "A", "T", "T", "T"],
                                 ["C", "R", "C", "K", "T"],
                                 ["C", "U", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=truck')
        self.assertEqual(response.json['response'], 'ok')

    def test_not_on_board(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["T", "A", "T", "T", "T"],
                                 ["C", "R", "C", "K", "T"],
                                 ["C", "U", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=board')
        self.assertEqual(response.json['response'], 'not-on-board')

    def test_not_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["T", "A", "T", "T", "T"],
                                 ["C", "R", "C", "K", "T"],
                                 ["C", "U", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=tasdfsadf')
        self.assertEqual(response.json['response'], 'not-word')
