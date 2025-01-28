import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

import constants as c

data_from_record122 = pd.read_csv('data/rps-record122.csv')
data_from_record_dtclf = pd.read_csv('data/rps-record_dtclf.csv')

# Data transformation

labels_list = []
inputs = np.empty((0, 2*c.NUMBER_OF_INPUTS))

for i in range(len(data_from_record122)):
    if data_from_record122.iloc[i]['round'] >= c.NUMBER_OF_INPUTS:
        p1_data = data_from_record122.iloc[i-c.NUMBER_OF_INPUTS:i]['p1'].values
        p2_data = data_from_record122.iloc[i-c.NUMBER_OF_INPUTS:i]['p2'].values
  
        combined_input = np.hstack([p1_data, p2_data])
        
        inputs = np.vstack([inputs, combined_input])
        labels_list.append(data_from_record122.iloc[i]['p1'])

for i in range(len(data_from_record_dtclf)):
    if data_from_record_dtclf.iloc[i]['n'] >= c.NUMBER_OF_INPUTS:
        p1_data = data_from_record_dtclf.iloc[i-c.NUMBER_OF_INPUTS:i]['p1'].values
        p2_data = data_from_record_dtclf.iloc[i-c.NUMBER_OF_INPUTS:i]['p2'].values
  
        combined_input = np.hstack([p1_data, p2_data])
        
        inputs = np.vstack([inputs, combined_input])
        labels_list.append(data_from_record_dtclf.iloc[i]['p1'])

labels = np.array(labels_list)

# NN model

inputs_train, inputs_test, labels_train, labels_test = train_test_split(
    inputs, labels, test_size=0.2, random_state=42
)

model = keras.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(2*c.NUMBER_OF_INPUTS,)),
    keras.layers.Dropout(0.1),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dropout(0.1),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dropout(0.1),
    keras.layers.Dense(3, activation='softmax')
])

optimizer = keras.optimizers.Adam(learning_rate=0.005)

model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

training_history = model.fit(inputs_train, labels_train, epochs=500, batch_size=2**6, validation_split=0.2, class_weight={0: 1, 1: 1, 2: 1})

# Evaluation of the model

plt.plot(training_history.history['loss'], label='Training Loss')
plt.plot(training_history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.savefig('plots/loss.png') 
plt.show() 

plt.plot(training_history.history['accuracy'], label='Training accuracy')
plt.plot(training_history.history['val_accuracy'], label='Validation accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('plots/accuracy.png') 
plt.show() 

print('Test')

test_loss, test_acc = model.evaluate(inputs_test,  labels_test, verbose=1)

# joblib.dump(model, 'model.pkl')