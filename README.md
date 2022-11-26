# AlphaSnap

Attempt at creating an intelligent agent for playing the mobile game **Marvel Snap**

# Step 1 - Reverse Engineering the game
To be able to train the agent, we need an environment where it can easily interact with the game. As no public API exists for the game, we have to recreate it. It needs to include the core functions of the game, as well as all[^1] cards and locations.

## A quick overview of the game
Each player brings a deck of 12 preselected, unique cards (hereafter referred to as a *deck*). The game has 3 locations, places where players can play cards. After six turns, whichever player is winning the majority of the locations (2 or more), wins the game.

### The beginning of the game
Each player draws three cards from their deck. The first (leftmost) of the three locations is revealed. The following turn, location 2 is revealed and on turn 3, the last (and rightmost) location is revealed.

### A turn
*The Play Phase*: Unless specified otherwise, each player is given energy equal to the turn number (i.e. 1 energy on turn 1, 2 energy on turn 2 etc.). They are allowed to play as many cards as they want, split between as many locations as they want, from their hand, as long as they have the energy to play them. The cards are played face down on the board, and each player cannot see where the other player has played their cards this turn or how many cards they have played this turn, until we enter the reveal phase.

*The Reveal Phase*: N/A


### In case of a draw
In case of a draw (players have the same amount of poewr at 1 location, while winning one each), whoever has the most total power wins. If the total power across all locations is equal, the game is declared a draw[^2].

*Example*: location 1 is a draw, with each player having 15 power. Location 2 is won by player 1, 17 to 9. Player 2 won location 3, 15 to 3. As player 2's total power is 39 compared to player 1's total power of 35, player two is declared the winner.

## The Cards

## The Locations
A location has space for four cards for each player. Each location also has a special effect. This effect can increase/decrease the power of the cards there on one occasion or over time, further restrict what types of cards or how many can be player, affect the power at other locations and more. For a full list of all location see[^3].


# Step 2 - Creating & training the agent
N/A


[^1]: Some cards/locations might prove very difficult to implement. If this is the case, ignoring the card will probably not affect the agents performance drastically if the card is not part of the current meta.
[^2]: https://marvelsnap.io/article/7-hidden-rules-that-will-cost-you-cubes-9
[^3]: https://marvelsnap.io/database/locations/
