A simple heuristic solver for Wordle.

## Principle
Given a list of possible words, all words are broken into their substrings $S$ (with repetition), and each word $w$ is assigned a likelihood score $L(w)$:
$$ L(w) = \sum_{s_j\in \textrm{substrings}(w)}{\log(\#\{x\in S \vert x=s_j\})}$$
This generalizes the basic approach of computing the log-likelihood of the word seen as an i.i.d. sample of letters, which I tried first.
Then, the list of all words is sorted by decreasing count of distinct letters, then by descreasing likelihood score.

With this approach we can solve all but 18 of the 4630 in the original wordlist of Wordle, a 99,61% success rate! On average it takes 3.78 trials to find the solution.

## Solving with known target
You can test how the heuristic finds a given target with the function
```python
resolve(target)
```
By default the function will print each attempted word

## Interactive solver
To solve the real thing, use the Game object as follows, repeating until solved:
```python
game = Game()
guess = game.propose_word()
print(guess)
game.feedback(guess, [0,1,2,0,0])
```
For the feedback, 0 is used for an incorrect letter (grey), 1 for a misplaced letter (orange), and 2 for a correct letter (green). You can also use the enumeration Clue.WRONG, Clue.MISPLACED, and Clue.RIGHT.

## Custom list of words
By default the list of words is wordle.txt, containing eligible 5-letter words on wordle. The repo also provides fr.txt for 5-letter words in French, and en.txt for a larger list of english words. You can provide you own file as *lexicon_filename* in *resolve* or *Game*.
