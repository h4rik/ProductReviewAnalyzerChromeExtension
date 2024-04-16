import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, LSTM, Dense, Dropout 
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import pandas as pd

print(tf.__version__)
# Parameters    
VOCAB_SIZE = 10000
MAX_LEN = 250
EMBEDDING_DIM = 100
MODEL_PATH = r'C:\Users\hp\OneDrive\Desktop\ml model\sentiment_analysis_newonelstm100.keras'
TOKENIZER_PATH = r'C:\Users\hp\OneDrive\Desktop\ml model\tokenizerlstm100.pickle'

file_path = r'C:\Users\hp\OneDrive\Desktop\data.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')
df_shuffled = data.sample(frac=1).reset_index(drop=True)
 
texts = []
labels = [] 

for _, row in df_shuffled.iterrows():
    texts.append(row.iloc[-1])
    label = row.iloc[0]
    labels.append(0 if label == 0 else 1 if label == 2 else 2)


texts = np.array(texts)
labels = np.array(labels)

# Check if tokenizer exists, if not, recreate it
if os.path.exists(TOKENIZER_PATH):
    print("Loading existing tokenizer...")
    with open(TOKENIZER_PATH, 'rb') as handle:
        tokenizer = pickle.load(handle)
else:
    print("Creating new tokenizer...")
    # Tokenize and pad the sequences
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=VOCAB_SIZE)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, maxlen=MAX_LEN, value=VOCAB_SIZE-1, padding='post')
    with open(TOKENIZER_PATH, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Split data into training and test sets (you might want to do this in a more balanced way)
train_data = padded_sequences[:-5000]
test_data = padded_sequences[-5000:]
train_labels = labels[:-5000]
test_labels = labels[-5000:]

# Check if saved model exists
if os.path.exists(MODEL_PATH):
    print("Loading saved model...")
    model = load_model(MODEL_PATH)
else:
    print("Training a new model...")
    # Define the model
    model = Sequential([
    Embedding(input_dim=VOCAB_SIZE, output_dim=EMBEDDING_DIM),
        Conv1D(filters=64, kernel_size=5, activation='relu'),
        MaxPooling1D(pool_size=4),
        LSTM(100, return_sequences=True),
        Dropout(0.2),
        LSTM(100),
        Dense(1, activation='sigmoid')  # Assuming binary classification for simplicity
    ])

  # Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_data, train_labels, epochs=15 , batch_size=128, validation_split=0.2)
# Save the trained model
model.save(MODEL_PATH)

#with open("model.pkl","wb") as file:
#  pickle.dump((model , tokenizer),file)

# Evaluate on test data
loss, accuracy = model.evaluate(test_data, test_labels)
print(f"Test accuracy: {accuracy * 100:.2f}%")

# Interactive loop for predictions
def encode_text(text):
    tokens = tf.keras.preprocessing.text.text_to_word_sequence(text)
    tokens = [tokenizer.word_index[word] if word in tokenizer.word_index else 0 for word in tokens]
    return pad_sequences([tokens], maxlen=MAX_LEN, padding='post', value=VOCAB_SIZE-1)

while True:
    user_input = input("Enter a sentence for sentiment analysis (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    encoded_input = encode_text(user_input)
    prediction = np.argmax(model.predict(encoded_input))

    if prediction == 0:
        print("Sentiment: Negative")
    elif prediction == 1:
        print("Sentiment: Neutral")
    else:
        print("Sentiment: Positive")
            