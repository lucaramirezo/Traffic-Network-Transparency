import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LeakyReLU
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard

# Read the CSV files
x_train = pd.read_csv('x_train.csv')
y_train = pd.read_csv('y_train.csv')
x_val = pd.read_csv('x_val.csv')
y_val = pd.read_csv('y_val.csv')

# Convert DataFrames to numpy arrays
x_train = x_train.values
y_train = y_train.values
x_val = x_val.values
y_val = y_val.values

# Model configuration
hidden_neurons = 32
output_neurons = y_train.shape[1]  # Number of output neurons should match the number of classes in y_train
input_dim = x_train.shape[1]  # Input dimension should match the number of features in x_train
adam_optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001, clipnorm=1.0)

# Create the model
model = Sequential()

# Input layer with LeakyReLU activation
model.add(Dense(hidden_neurons, input_dim=input_dim, kernel_initializer='he_uniform', bias_initializer='zeros'))
model.add(LeakyReLU(alpha=0.01))

# Add hidden layers with LeakyReLU activation
for _ in range(10):
    model.add(Dense(hidden_neurons, kernel_initializer='he_uniform', bias_initializer='zeros'))
    model.add(LeakyReLU(alpha=0.01))

# Output layer
model.add(Dense(output_neurons, activation='softmax', kernel_initializer='he_uniform', bias_initializer='zeros'))

# Compile the model
model.compile(optimizer=adam_optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Callbacks
checkpoint = ModelCheckpoint('new_bestmodelv1.h5', verbose=1, monitor='val_accuracy', save_best_only=True, mode='auto')
tensorboard_callback = TensorBoard(log_dir='./logs', histogram_freq=1)

# Train the model
history = model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    epochs=20,
    batch_size=140,
    callbacks=[checkpoint, tensorboard_callback],
    verbose=1
)

# Model summary
model.summary()


#%%
