import json
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

""" Reads all the intents from the json file. """
with open('intents.json') as file:
    data = json.load(file)

""" Global variables """
TRAINING_SENTENCES = []
TRAINING_LABELS = []
LABELS = []
RESPONSES = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        TRAINING_SENTENCES.append(pattern)
        TRAINING_LABELS.append(intent['tag'])
    RESPONSES.append(intent['responses'])

    if intent['tag'] not in LABELS:
        LABELS.append(intent['tag'])

num_classes = len(LABELS)

label_encoder = LabelEncoder()
label_encoder.fit(TRAINING_LABELS)
TRAINING_LABELS = label_encoder.transform(TRAINING_LABELS)

vocab_size = 10000
embedding_dim = 24
max_len = 20
oov_token = '<OOV>'

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(TRAINING_SENTENCES)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(TRAINING_SENTENCES)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(GlobalAveragePooling1D())
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

epochs = 500
history = model.fit(padded_sequences, np.array(TRAINING_LABELS), epochs=epochs)

model.save("chat_model")

import pickle

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
with open('label_encoder.pickle', 'wb') as ecn_file:
    pickle.dump(label_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)