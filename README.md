A simple heuristic solver for Wordle.

##Solving with known target
You can test how the heuristic finds a given target with the function
```python
resolve(target)
```
By default the function will print each attempted word, along with the number of compatible words at each round.

##Interactive solver
To solve the real thing, first use the Game object as follows, until solved:
```python
game = Game()
guess = game.propose_word()
print(guess)
game.feedback(guess, [0,1,2,0,0])
```
For the feedback, 0 is used for an incorrect letter (grey), 1 for a misplaced letter (orange), and 2 for a correct letter (green). You can also use the enumeration Clue.WRONG, Clue.MISPLACED, and Clue.RIGHT.

##Custom list of words
By default the list of words is en.txt, containing 5-letter words in English. The repo also provides fr.txt for 5-letter words in French. You can provide you own file as *lexicon_filename* in *resolve* or *Game*.
