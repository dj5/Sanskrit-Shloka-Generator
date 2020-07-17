from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import numpy as np
from get_data import get_data_sanskrit
import matplotlib.pyplot as plt

VOCAB_SIZE = 600
maxlen = None
oov_token = "<OOV>"
padding = "pre"
total_words = None
epochs = 100


class Callback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if logs["acc"]>0.99:
            print("Accuracy reached 99%")
            self.model.stop_training=True


def tokenize(sanskrit):
    global total_words, maxlen
    tokenizer_san = Tokenizer(num_words=VOCAB_SIZE, oov_token=oov_token)
    tokenizer_san.fit_on_texts(sanskrit)    # fit tokenizer on whole corpus
    total_words = len(tokenizer_san.word_index) + 1     # all words in corpus + 1 for Out Of the Vocab word
    input_sequences = []
    for line in sanskrit:
        token_list = tokenizer_san.texts_to_sequences([line])[0]    # convert each line of corpus to sequences
        for i in range(1, len(token_list)):
            n_gram_seq = token_list[:i + 1]
            input_sequences.append(n_gram_seq)
    maxlen = max([len(x) for x in input_sequences])     # length of longest sequence
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=maxlen, padding="pre"))
    xs = input_sequences[:, :-1]        # input sequence
    labels = input_sequences[:, -1]     # Output sequence
    ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)
    return xs, ys, tokenizer_san


def build_model(xs, ys):
    callback = Callback()     # initialize callback

    model_san = tf.keras.Sequential([                       # Two layer Bidirectional LSTM model
        tf.keras.layers.Embedding(total_words, 150, input_length=maxlen - 1),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(150, return_sequences=True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(150)),

        tf.keras.layers.Dense(total_words, activation="softmax")
    ])
    model_san.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["acc"])
    history = model_san.fit(xs, ys, epochs=epochs, callbacks=[callback])
    return model_san, history


def generate(tokenizer_san, model_san, seed_text):
    output_word = ""
    while "॥" not in output_word:   # generate next words till '॥'
        token_list = tokenizer_san.texts_to_sequences([seed_text])[0]   # convert seed_text to sequence
        token_list = pad_sequences([token_list], maxlen=maxlen - 1, padding="pre")
        predicted = model_san.predict_classes(token_list)   # predict next token

        for word, index in tokenizer_san.word_index.items():    # find word for the predicted index
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text


def plot_acc_loss(history):
    # Function to plot loss and accuracy for every epoch
    loss = history.history["loss"]
    acc = history.history["acc"]
    epochs = range(len(acc))
    plt.plot(epochs,loss)
    plt.title("loss")
    plt.figure()
    plt.plot(epochs,acc)
    plt.title("Accuracy")
    plt.show()


def main():
    sanskrit = get_data_sanskrit()
    print(len(sanskrit))
    xs, ys, tokenizer = tokenize(sanskrit)
    model, history = build_model(xs, ys)
    plot_acc_loss(history)
    # input_strings = "कामधेनुगुना विद्या", "देहिनोऽस्मिन्यथा देहे", "न जायते म्रियते", "वासांसि जीर्णानि", "नैनं छिन्दन्ति", "जातस्य हि", "सुखदुःखे समे", "कर्मण्येवाधिकारस्ते", "नात्यन्तं सरलैर्भाव्यं", "श्लोकेन वा", "प्रलये भिन्नमर्यादा", "जन्ममृत्यू", "कालः", "स्वस्तिप्रजाभ्यः", "सर्वं परवशं", "प्रथमे नार्जिता"
    # for seed_text in input_strings:
    #     print("Input: " + seed_text)
    #     print("Output: " + generate(tokenizer, model, seed_text))
    seed_text = input()
    print("Input: "+seed_text)
    print("Output: "+generate(tokenizer, model, seed_text))




if __name__ == '__main__':
    main()
