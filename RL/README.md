# Marvel Snap Agent
Marvel Snap belongs to the strategy card game genre. This genre presents several unqiue challenges when trying to train an agent to perform well at the game. Firstly, the game is an imperfect information game. You do not know which cards your opponent has on their hand, let alone in their deck (although human players can often infer this after seeing some cards, this is another challenging thing to learn). The game also consists of two non-trivial stages, namely the **Deck-Building stage** and the **Battle stage** [^1].

## Versions
### V1
**STATUS: WIP**
The locations are always the same, and the deck is fixed. This leads to a vastly reduced state-space and also converts the problem to a one-stage game, which can be solved using conventional imperfect information reinforcement learning techniques. We can further simplify by only giving the power at the three different locations, as well as the players own hand as information to the network.

### V2
**STATUS: N/A**
Same as V1, however now we feed all the information of the board to the agent. This means that we give the id and position of all cards on the board, the total power etc. The state space is now way bigger, which will prove more challenging and it will likely take longer for the model to converge to a minima.

### V3
**STATUS: N/A**

Same as V2, but the deck is now a random selection (it is still pre-selected and not trained), either by picking 12 random cards from the pool of cards, or by defining several decks and picking between them. This should help simulate the rock-paper-scissors element of the game, where some decks beat some often, while losing to others often.

### V4
**STATUS: N/A**
The deck building stage is now a part of the model. Locations are now also random. This leads to an insanely large state-space.

## References
[^1]: Mastering Strategy Card Game (Legends of Code and Magic) via End-to-End Policy and Optimistic Smooth Fictitious Play, https://arxiv.org/pdf/2303.04096.pdf
[^2]: Mastering Strategy Card Game (Hearthstone) with Improved Techniques, https://arxiv.org/pdf/2303.05197.pdf