# Initial thoughts

Looking to create a chess application in the command line. If successful AI
games would be nice *much* later on, but for now just manual (i.e. 2 players).

## Functionality

We'll have 3 core aspects:
1. A game state, where all the information is stored. It should also include a score
    based on the usual 1, 3, 3, 5, 9 system.
2. A render function which will translate the game state into something
    visually pleasing.
3. A UI for the changing the game state.

## Cosmetics

Pieces should be ASCII based for maximum compatibility. For 1 and 2 player modes use
vertical and horizontal respectively.
```
:      a   b   c   d   e   f   g   h
:    +---+---+---+---+---+---+---+---+       1 player mode.
:  8 | H | $ | I | Q | K | I | $ | H | 8     * i = pawn
:    +---+---+---+---+---+---+---+---+       * $ = knight
:  7 | i | i | i | i | i | i | i | i | 7     * I = bishop
:    +---+---+---+---+---+---+---+---+       * H = rook
:  6 |   |   |   |   |   |   |   |   | 6     * Q = queen
:    +---+---+---+---+---+---+---+---+       * K = king
:  5 |   |   |   |   |   |   |   |   | 5
:    +---+---+---+---+---+---+---+---+
:  4 |   |   |   |   |   |   |   |   | 4
:    +---+---+---+---+---+---+---+---+
:  3 |   |   |   |   |   |   |   |   | 3
:    +---+---+---+---+---+---+---+---+
:  2 | i | i | i | i | i | i | i | i | 2
:    +---+---+---+---+---+---+---+---+
:  1 | H | $ | I | Q | K | I | $ | H | 1
:    +---+---+---+---+---+---+---+---+
:      a   b   c   d   e   f   g   h
```