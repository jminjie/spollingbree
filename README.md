# Spolling Bree

Spolling Bree is a version of the NYT Spelling Bee game that only accpets fake
words that are plausible.

## Model
Originally plausibility was rated by a simple statistical model
trained on trigrams from every English word.

The current model is machine learning based, and uses a character based RNN
with GRUs trained locally on English words.

## Demo
Play the live demo at [bee.jminjie.com](https://bee.jminjie.com).

## Development
To deploy at `localhost:8998`, run `python3 server.py debug`
