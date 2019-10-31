
"""
Tagging Service

"""

import tensorflow as tf
import json
import numpy as np
import keras
import os

print(os.getcwd())



def encode_text(text, vocab, sequence_length):
    text = list(text)
    encoded = [vocab.get(c, 0) for c in text]
    if len(encoded) < sequence_length:
        encoded += [0] * (sequence_length - len(encoded))
    if len(encoded) > sequence_length:
        encoded = encoded[:sequence_length]
    return np.array([encoded])


class CharacterBasedNNClassifier:
    sequence_length = 256

    def __init__(self, model_path, vocab, sequence_length=256):
        self.model = tf.keras.models.load_model(model_path)
        self.vocab = vocab
        self.sequence_length = sequence_length

    
    def predict(self, text):
        p = self.model.predict(text, batch_size=1)
        return p[0]



class SentimentClassifier():
    sequence_length = 256

    def __init__(self, model_json_path, model_weights_path, vocab, sequence_length=256):
        with open(model_json_path) as json_f:
            self.model = tf.keras.models.model_from_json(json_f.read())
            self.model.load_weights(model_weights_path)

        self.vocab = vocab
        self.sequence_length = sequence_length

    
    def predict(self, text):
        p = self.model.predict(text, batch_size=1)
        return p[0]


class BaseTaggingService:

    def __init__(self):
        self.sequence_length = 256
        self.vocab = json.load(open("res/vocab.json"))
        self.aggressive_vocab = json.load(open("res/aggressive.json"))
        self.sentiment_clf = SentimentClassifier("res/sentiment_model.json", "res/sentiment_model.h5", self.vocab)
        self.contact_clf = CharacterBasedNNClassifier("res/contact.h5", self.vocab)
        self.aggressive_clf = CharacterBasedNNClassifier("res/aggressive.h5", self.aggressive_vocab, 128)


    def predict(self, text):
        sent = ['pos', 'neg', 'nat']

        text128 = encode_text(text, self.aggressive_vocab, 128)
        text = encode_text(text, self.vocab, self.sequence_length)

        result = {
            'sentiment': sent[np.argmax(self.sentiment_clf.predict(text))],
            'is_contact': self.contact_clf.predict(text)[1],
            'is_aggressive': self.aggressive_clf.predict(text128)[0]
        }   

        return result