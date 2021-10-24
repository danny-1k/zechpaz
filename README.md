# Zechpaz

**Zechpaz** is an attempt to make a chess AI that uses a neural network as it's evaluation function.

Obviously, It's stupid as f.

what I mean by stupid is that it doesn't seem to have a goal.
Though it can capture opponent pieces


# Playing the shit

for a human vs AI game
```
python play.py
```

for an AI vs AI game

```
python play_self.py
```

# Method
The data is built on the idea that every move in a game of chess contibutes to the final outcome of the game(assuming every move is optimal).

For every datapoint, the feature is an array of size (6,8,8) (6 for the number of pieces and 8,8 for the position of the pieces on the board ).

The label is 1 if white wins and 0 if black wins.

I found that adding draws created a huge data imbalance and made the model overfit on draws.

# Training from scratch

### Data collection & generation
data collection & generation is in 4 steps:

1. Get data -> `python  data/download_data.py`


2. Split the pgn files into games -> `python data/splitter.py`


3. Transform the pgns into txt files for easier processing -> `python data/create_txts.py`


4. Generate dataset -> `python data/gen_data.py`

You can check the distribution of the data with the `data/get_data_dist.py` script



### Finally, training 

- Train the classifier -> `python train_classifier.py`


# What could be done to improve this
- Convnets would be faster and probably have better results.
- Reinforcement Learning
- Better board representation.
- Sequence models for making predictions based on past states (If done properly might remove the need for search algorithms)
