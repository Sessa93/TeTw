#Author Andrea Sessa, 2016

from collections import deque

class User:
    def __init__(self, name):
        self.name = name
        self.last_tweets = deque(maxlen=20)
