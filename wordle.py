import enum
from multiprocessing import Pool
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


def substrings(word):
    return [word[i:j] for i in range(len(word)) for j in range(i + 1, len(word) + 1)]


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
    def __init__(self, lexicon_filename="wordle.txt"):
        self.word_list = get_lexicon(lexicon_filename)
        self._sort_word_list()

    def feedback(self, word, feedback):
        feedback = list(map(Clue, feedback))
        compatible_words = []
        for w in self.word_list:
            if feedback == compare(word, w):
                compatible_words.append(w)
        self.word_list = compatible_words

    def loglikelihood(self, word):
        return np.sum(np.log(list(map(self.cntr.get, substrings(word)))))

    def _sort_word_list(self):
        self.cntr = Counter()
        for word in self.word_list:
            self.cntr.update(substrings(word))
        self.word_list.sort(
            reverse=True,
            key=lambda x: (len(set(x)), self.loglikelihood(x)),
        )

    def propose_word(self):
        if len(self.word_list) == 0:
            raise ValueError("There are no compatible words!")
        self._sort_word_list()
        return self.word_list[0]


def resolve(target, lexicon_filename="wordle.txt", max_attempts=6, verbose=False):
    game = Game(lexicon_filename=lexicon_filename)
    attempts = []
    for _ in range(max_attempts):
        guess = game.propose_word()
        attempts.append(guess)
        if verbose:
            num_words = len(game.word_list)
            print("guess is", guess, "chosen from", num_words, "words")
        if guess == target:
            break
        feedback = compare(guess, target)
        game.feedback(guess, feedback)
    return attempts


def resolve_all(
    lexicon_filename="wordle.txt", output_filename="results.csv", num_cpu=12
):
    word_list = get_lexicon(lexicon_filename)
    p = Pool(num_cpu)
    results = p.map(resolve, word_list)
    with open(output_filename, "a") as f:
        f.writelines(list(map(lambda x: ",".join(x) + "\n", results)))
    print("Complete!")
