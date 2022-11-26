# AlphaSnap

Attempt at creating an intelligent agent for playing the mobile game **Marvel Snap**

## Step 1 - Reverse Engineering the game
To be able to train the agent, we need an environment where it can easily interact with the game. As no public API exists for the game, we have to recreate it. It needs to include the core functions of the game, as well as all (relevant[^1]) cards and locations

## Step 2 - Creating & training the agent



[^1]: Some cards might prove very difficult to implement. If this is the case, ignoring the card will probably not affect the agents performance drastically if the card is not part of the current meta.
