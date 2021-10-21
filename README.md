# Catur

**Catur** is a chess AI which uses a neural network as it's evaluation function

**catur** is malay for chess

# Getting started

```
python play.py
```


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


# Improvements

This method uses a supervised learning approach so it will only be as good as the data  and the features used.

Reinforcement Learning techniques might be better for this kind of task.

As the goal shifts from "learn a function to convert the board state to an evaluation" to "Learn a policy that makes you win your opponent"

