#!/usr/bin/env python
import tensorflow as tf
import time
from rnn_gru_model import RnnGRUModel
import math

# Model wrapper which provides utilities for running the model to generate
# plausible words and doing word plausibility evaluation using the learned or
# loaded weights
class RnnWordPlausibilityEvaluator:
    def __init__(self, logger,
            model=None,
            ids_from_chars=tf.keras.models.load_model('ids_from_chars'),
            chars_from_ids=tf.keras.models.load_model('chars_from_ids'),
            temperature=0.5):
        self.logger = logger
        self.ids_from_chars = ids_from_chars
        self.chars_from_ids = chars_from_ids

        self.softmax = tf.keras.layers.Softmax()

        if not model:
            # load the saved weights
            self.model = RnnGRUModel()
            self.model.load_weights("base_model_saved_weights")
        else:
            self.model = model

        self.temperature = temperature

    def generate_one_step(self, inputs, states=None):
        # Convert strings to token IDs.
        input_chars = tf.strings.unicode_split(inputs, 'UTF-8')
        input_ids = self.ids_from_chars(input_chars).to_tensor()

        # Run the model.
        # predicted_logits.shape is [batch, char, next_char_logits]
        predicted_logits, states = self.model(inputs=input_ids, states=states,
                return_state=True)
        # Only use the last prediction.
        predicted_logits = predicted_logits[:, -1, :]
        predicted_logits = predicted_logits/self.temperature

        # Sample the output logits to generate token IDs.
        predicted_ids = tf.random.categorical(predicted_logits, num_samples=1)
        predicted_ids = tf.squeeze(predicted_ids, axis=-1)

        # Convert from token ids to characters
        predicted_chars = self.chars_from_ids(predicted_ids)

        # Return the characters and model state.
        return predicted_chars, states

    def p_of_letter(self, normalized_probs, letter):
        return (tf.squeeze(normalized_probs)[self.ids_from_chars(letter).numpy()]).numpy()

    def is_plausible(self, word, show_work=False):
        threshold = 0.3 + 0.2 * max((len(word) - 5), 0)
        score = self.evaluate_word(word, show_work)
        if show_work:
            print("score for {0}={1}, threshold={2}".format(word, score, threshold))
        return score >= threshold

    def evaluate_word(self, word, show_work=False):
        states = None
        score = 0

        # feed '_' into the model
        seed_char = tf.constant(['_'])        
        input_seed_char = tf.strings.unicode_split(seed_char, 'UTF-8')
        this_input_id = self.ids_from_chars(input_seed_char).to_tensor()
        predicted_logits, states = self.model(inputs=this_input_id, states=states,
                return_state=True)

        word = word + '*'
        penalty = 0
        for char in word:
            # get the probability of current char
            predicted_logits = predicted_logits[:, -1, :]
            normalized_probs =  self.softmax(predicted_logits).numpy()
            char_prob = self.p_of_letter(normalized_probs, char)

            # update score and penalty
            score += char_prob
            if show_work:
                print("prob of", char, "=", char_prob)
            if char_prob < 0.001:
                penalty += 10
            elif char_prob < 0.01:
                penalty += 1

            # feed current char into model
            this_char = tf.constant([char])
            input_char = tf.strings.unicode_split(this_char, 'UTF-8')
            this_input_id = self.ids_from_chars(input_char).to_tensor()
            predicted_logits, states = self.model(inputs=this_input_id, states=states,
                    return_state=True)

        if show_work:
            print("penalty=", penalty)
        if penalty > 0:
            score /= (penalty + 1)

        return score
