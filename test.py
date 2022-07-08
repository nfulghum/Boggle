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
