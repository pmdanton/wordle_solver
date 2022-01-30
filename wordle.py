import enum
from typing import Counter

import numpy as np


class Clue(enum.Enum):
    WRONG = 0
    MISPLACED = 1
    RIGHT = 2


def get_lexicon(filename="wordle.txt"):
    with open(filename) as f:
        word_list = f.readlines()

    return list(map(str.strip, word_list))


def compare(guess, target):
    guess = list(guess)
    target = list(target)
    result = [Clue.WRONG] * len(guess)
    for idx, (g, t) in enumerate(zip(guess, target)):
        if g == t:
            result[idx] = Clue.RIGHT
            target[idx] = "."
    for idx, g in enumerate(guess):
        if result[idx] != Clue.RIGHT and g in target:
            result[idx] = Clue.MISPLACED
            target[target.index(g)] = "."
    return result


class Game:
    def __init__(self, lexicon_filename="en.txt"):
        self.word_list = get_lexicon(lexicon_filename)
        self.cntr = Counter("".join(self.word_list))
        self._sort_word_list()

    def feedback(self, word, feedback):
        feedback = list(map(Clue, feedback))
        compatible_words = []
        for w in self.word_list:
            if feedback == compare(word, w):
                compatible_words.append(w)
        self.word_list = compatible_words

    def loglikelihood(self, word):
        return np.sum(np.log(list(map(self.cntr.get, word))))

    def _sort_word_list(self):
        self.word_list.sort(
            reverse=True,
            key=lambda x: (len(set(x)), self.loglikelihood(x)),
        )

    def propose_word(self):
        if len(self.word_list) == 0:
            raise ValueError("There are no compatible words!")
        self._sort_word_list()
        return self.word_list[0]


def resolve(target, lexicon_filename="wordle.txt", max_attempts=100, verbose=True):
    game = Game(lexicon_filename=lexicon_filename)
    for k in range(max_attempts):
        guess = game.propose_word()
        if verbose:
            num_words = len(game.word_list)
            print("guess is", guess, "chosen from", num_words, "words")
        if guess == target:
            return k + 1
        feedback = compare(guess, target)
        game.feedback(guess, feedback)
    return 0


def resolve_all(lexicon_filename, output_filename="results.csv"):
    word_list = get_lexicon(lexicon_filename)
    with open(output_filename, "a") as f:
        for target in word_list:
            num_steps = resolve(target, word_list, verbose=False)
            f.write(target + "," + str(num_steps) + "\n")
    print("Complete!")
