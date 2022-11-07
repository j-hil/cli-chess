# Initial thoughts

Looking to create a chess application in the command line. If successful AI
games would be nice *much* later on, but for now just manual (i.e. 2 players).

## Functionality

We'll have 3 core aspects:
- [X] A game state, where all the information is stored. It should also include a score
    based on the usual 1, 3, 3, 5, 9 system.
- [X] A render function which will translate the game state into something
    visually pleasing.
- [X] A UI for the changing the game state.


## Cosmetics

Pieces should be ASCII based for maximum compatibility. For 1 and 2 player modes use
vertical and horizontal respectively.
```
: Welcome to J-Chess. Use the arrow keys to navigate, space to select, and 'q' to quit.
:
:    PLAYER ONE                a   b   c   d   e   f   g   h
:                            +---+---+---+---+---+---+---+---+
:    SCORE=99              8 | H | J | I | Q | K | I | J | H | 8
:    i, i, i, i, I, J        +---+---+---+---+---+---+---+---+
:    i, i, i, i, I, J      7 |   | i | i | i | i | i | i | i | 7
:    i, i, i, i,             +---+---+---+---+---+---+---+---+
:                          6 |   |   |   |   |   |   |   |   | 6
:                            +---+---+---+---+---+---+---+---+
:                          5 |   |   |   |   |   |   |   |   | 5
:                            +---+---+---+---+---+---+---+---+
:                          4 |   |   |   |   |   |   |   |   | 4
:                            +---+---+---+---+---+---+---+---+
:                          3 |   |   |   |   |   |   |   |   | 3
:                            +---+---+---+---+---+---+---+---+
:                          2 | i | i | i | i | i | i | i | i | 2
:                            +---+---+---+---+---+---+---+---+
:                          1 | H | J | I | Q | K | I | J | H | 1
:                            +---+---+---+---+---+---+---+---+
:                              a   b   c   d   e   f   g   h
```