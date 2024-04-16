import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

VOCAB_SIZE = 10000
MAX_LEN = 250
model_path = r'C:\Users\hp\OneDrive\Desktop\major API\extension\reviewanalyzer\sentiment_analysis.keras'
tokenizer_path = r'C:\Users\hp\OneDrive\Desktop\major API\extension\reviewanalyzer\tokenizer.pickle'

def load_tokenizer(tokenizer_path):
    with open(tokenizer_path, 'rb') as handle:  
        tokenizer = pickle.load(handle)
    return tokenizer

def load_sentiment_model(model_path):
    model = load_model(model_path)
    return model

def encode_text(tokenizer, text_or_dict):   
    if isinstance(text_or_dict, dict):
        text = text_or_dict.get('body', '')
    else:
        text = text_or_dict

    tokens = tf.keras.preprocessing.text.text_to_word_sequence(text)
    encoded = tokenizer.texts_to_sequences([tokens])
    padded = tf.keras.preprocessing.sequence.pad_sequences(encoded, maxlen=MAX_LEN, padding='post')
    return padded


def analyze_comments(comments):
    print("Analyzing comments:", comments)
    tokenizer = load_tokenizer(tokenizer_path)
    print("loading tokenizer")
    model = load_sentiment_model(model_path)
    print("loading model...")
    positive_count = 0
    negative_count = 0

    for comment in comments:
        encoded_comment = encode_text(tokenizer, comment)
        prediction = np.argmax(model.predict(encoded_comment))

        if prediction == 0:
            negative_count += 1
        else:
            positive_count += 1

    total_comments = len(comments)
    positive_percentage = (positive_count / total_comments) * 100
    negative_percentage = (negative_count / total_comments) * 100

    return positive_percentage, negative_percentage

# Example usage
'''
comments = ['Great product!', 'Not satisfied with the quality.', 'Highly recommended.','amazinggg']
positive_percentage, negative_percentage = analyze_comments(comments)
print(f"Positive comments: {positive_percentage:.2f}%")
print(f"Negative comments: {negative_percentage:.2f}%")
'''