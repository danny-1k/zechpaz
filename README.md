# Catur

**Catur** is a neural network trained on chess data
This is an attempt to make a chess ai with a neural-net based evaluation function

**catur** is malay for chess

# Getting started

```
python play.py
```


# Training from scratch

### Data collection & generation
data collection & generation is in 4 steps:

1. Get data -> `python download_data.py`


2. Split the pgn files into games -> `python splitter.py`


3. Transform the pgns into txt files for easier processing -> `python create_txts.py`


4. Generate dataset -> `python gen_data.py`

You can check the distribution of the data with the `get_data_dist.py` script



### Finally, training 

- Train the feature extractor -> `python train_ae.py`
- Train the classifier -> `python train_classifier.py`
