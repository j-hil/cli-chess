# The Game State

I believe the best way to approach this is to create a `GameState` class which itself
contains a list of `Piece`s. Each `Piece` will contain information regarding  it's
position, color, etc and all other info about the `GameState` should be constructable
from this.

I can see two approaches for the `Piece` class:
1. Make it an `ABC` and create individual classes for the `King`, `Queen`, etc
2. Give `Piece` an `piece_type` attribute and have the behavior of the methods depend
    on this attribute.

Option 1 would produce more boilerplate but less complex conditional code. It would also
be contained within one file and would make the `GameState` code easier to implement.

Hence I'll go with option 1 for now.
