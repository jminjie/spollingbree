#!/usr/bin/env python
import tensorflow as tf
import time
from rnn_gru_model import RnnGRUModel

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

    def probability_of_letter(self, logits, letter):
        return (tf.squeeze(logits)[self.ids_from_chars(letter).numpy()]).numpy()

    def is_plausible(self, word):
        return self.evaluate_word(word) > 20

    def evaluate_word(self, word, show_work=False):
        # Seed the model with '**'
        seed_chars = tf.constant(['**'])
        input_chars = tf.strings.unicode_split(seed_chars, 'UTF-8')
        input_ids = self.ids_from_chars(input_chars).to_tensor()
        states = None

        # get the initial probability distribution
        predicted_logits, states = self.model(inputs=input_ids, states=states, return_state=True)
        predicted_logits = predicted_logits[:, -1, :]/self.temperature

        total_prob = 0
        for letter in word:
            # check the log probability of the letter given current state
            probability = self.probability_of_letter(predicted_logits, letter)
            total_prob += probability
            if show_work:
                print("Probability of", letter, "=", probability)

            # feed this letter into the model
            this_char = tf.constant([letter])        
            input_char = tf.strings.unicode_split(this_char, 'UTF-8')
            this_input_id = self.ids_from_chars(input_char).to_tensor()
            predicted_logits, states = self.model(inputs=this_input_id, states=states,
                    return_state=True)
            predicted_logits = predicted_logits[:, -1, :]/self.temperature

        # check the log probability of '*' given current state
        probability = self.probability_of_letter(predicted_logits, '*')
        # TODO This assumes that the probability of the word is the product of
        # the probability of each letter.
        # The problem is that I'm not really training the RNN to generate
        # probabilities for each letter. In other words the log likelihoods in
        # the logits is not real, just directionally correct
        total_prob += probability
        if show_work:
            print("Probability of * =", probability)

        # TODO normalize by length
        # TODO actually, shouldn't the model do this automatically if it's well trained?
        return total_prob
