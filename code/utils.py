import os
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import keras.backend as K
from train_config import *

def triplet_loss(anchor, positive, negative, alpha=0.2):
    pos_dist = tf.reduce_sum(tf.square(anchor - positive), axis=1)
    neg_dist = tf.reduce_sum(tf.square(anchor - negative), axis=1)
    
    basic_loss = pos_dist - neg_dist + alpha
    loss = tf.maximum(basic_loss, 0.0)
    
    return tf.reduce_mean(loss)

def save_result(history):
    accuracy = history.history['accuracy']
    loss = history.history['loss']
    precision = history.history['precision']
    recall = history.history['recall']

    val_accuracy = history.history['val_accuracy']
    val_loss = history.history['val_loss']
    val_precision = history.history['val_precision']
    val_recall = history.history['val_recall']

    epochs = range(1,len(accuracy)+1)
    epoch_list = list(epochs)

    df = pd.DataFrame({'epoch': epoch_list, 'train_accuracy': accuracy, 'train_loss': loss, 'train_precision': precision, 'train_recall': recall, 'validation_accuracy': val_accuracy, 'validation_loss': val_loss, 'validation_precision': val_precision, 'validation_recall': val_recall},
                            columns=['epoch', 'train_accuracy', 'train_loss', 'train_precision', 'train_recall', 'validation_accuracy', 'validation_loss', 'validation_precision', 'validation_recall'])
    df.to_csv(os.path.join(RESULT_FILE_PATH, 'result.csv'), index=False, encoding='euc-kr')

    plt.plot(epochs, accuracy, 'b', label='Training accuracy')
    plt.plot(epochs, val_accuracy, 'r', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.savefig(os.path.join(RESULT_FILE_PATH, 'accuracy.png'))
    plt.cla()

    plt.plot(epochs, loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.savefig(os.path.join(RESULT_FILE_PATH, 'loss.png'))
    plt.cla()

    K.clear_session()