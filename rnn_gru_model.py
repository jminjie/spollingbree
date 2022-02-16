#!/usr/bin/env python
import tensorflow as tf

# The base RNN model for word plausibility generation and evaluation
class RnnGRUModel(tf.keras.Model):
    def __init__(self):
        super().__init__(self)
        self.vocab_size = 29
        self.embedding_dim = 256
        self.rnn_units = 300

        self.embedding = tf.keras.layers.Embedding(self.vocab_size, self.embedding_dim)
        self.gru = tf.keras.layers.GRU(self.rnn_units,
                return_sequences=True,
                return_state=True)
        self.dense = tf.keras.layers.Dense(self.vocab_size)

    def call(self, inputs, states=None, return_state=False, training=False):
        x = inputs
        x = self.embedding(x, training=training)
        if states is None:
            states = self.gru.get_initial_state(x)
        x, states = self.gru(x, initial_state=states, training=training)
        x = self.dense(x, training=training)

        if return_state:
            return x, states
        else:
            return x
