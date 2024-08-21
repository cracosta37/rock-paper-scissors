import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

import constants as c

data_from_record122 = pd.read_csv('Data/rps-record122.csv')
data_from_record_dtclf = pd.read_csv('Data/rps-record_dtclf')

labels_list = []
inputs = np.empty((0, c.NUMBER_OF_INPUTS))

for i in range(len(data_from_record122)):
    if data_from_record122.iloc[i]['round'] >= c.NUMBER_OF_INPUTS:
        labels_list.append([data_from_record122.iloc[i]['p1']])
        inputs = np.vstack([inputs, data_from_record122.iloc[i-c.NUMBER_OF_INPUTS:i]['p1']])

for i in range(len(data_from_record_dtclf)):
    if data_from_record_dtclf.iloc[i]['n'] >= c.NUMBER_OF_INPUTS:
        labels_list.append([data_from_record_dtclf.iloc[i]['p1']])
        inputs = np.vstack([inputs, data_from_record_dtclf.iloc[i-c.NUMBER_OF_INPUTS:i]['p1']])

labels = np.array(labels_list)

inputs_train, inputs_test, labels_train, labels_test = train_test_split(
    inputs, labels, test_size=0.3, random_state=42
)

model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(c.NUMBER_OF_INPUTS,)),  # hidden layer (1)
    keras.layers.Dense(3, activation='softmax')  # output layer (2)
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(inputs_train, labels_train, epochs=10)

test_loss, test_acc = model.evaluate(inputs_test,  labels_test, verbose=1) 

print('Test accuracy:', test_acc)