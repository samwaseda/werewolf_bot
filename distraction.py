import numpy as np
from difflib import SequenceMatcher


class Distraction:
    def __init__(self, number_of_options=10):
        self.current_word = None
        self.number_of_options = number_of_options
        with open('words.txt', 'r') as f:
            self.all_words = f.read().split('\n')

    @staticmethod
    def sort(word):
        return ''.join(sorted(word))

    @staticmethod
    def similarity(a, b) -> bool:
        return SequenceMatcher(None, a, b).ratio()

    def ask_question(self) -> tuple:
        if self.current_word is None:
            self.current_word = np.random.choice(self.all_words)
        values = np.array([
            self.similarity(self.sort(self.current_word), self.sort(w))
            for w in self.all_words
        ])
        candidate_words = np.random.permutation(
            np.array(self.all_words)[np.argsort(values)[-self.number_of_options:]]
        )
        cw_random = ''.join(np.random.permutation(list(self.current_word)))
        return cw_random, candidate_words

    def answer(self, word) -> bool:
        results = self.sort(self.current_word) == self.sort(word)
        self.current_word = None
        return results
