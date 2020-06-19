import sys
import os
import numpy as np
import h5py
import pandas as pd
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import keras
sys.stderr = stderr
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation

    # for each game (draw), we have 60 balls numbered from 1 to 60 inside a bowl. Then, 6 of them are chosen and the result is shown. eg: 14-31-32-05-59-41
    # for this purpose, we will try to predict just the first number

# functions

def training(m,t):

    # load the data from all the games
    # m is the number of training examples ;
    # t is the number of test examples
    # the output is extracting just the first number of the each game.

    
    trainingData = r'dataset645.csv'
    data = pd.read_csv(trainingData)

    dataset = {}

    X_train = np.zeros((4,m-t))
    Y_train = np.zeros((60,m-t))
    X_test = np.zeros((4,t))
    Y_test = np.zeros((60,t))
 
    X_train[0][:] = data.values[0][0:m-t]   #number of the game
    X_train[1][:] = data.values[3][:m-t]    # day of the game
    X_train[2][:] = data.values[4][0:m-t]   # month of the game
    X_train[3][:] = data.values[5][0:m-t]   #year of the game
    X_train = X_train.T;

    X_test[0][:] = data.values[0][m-t:m]
    X_test[1][:] = data.values[3][m-t:m]
    X_test[2][:] = data.values[4][m-t:m]
    X_test[3][:] = data.values[5][m-t:m]
    X_test = X_test.T;
    
    Y_train = data.values[7][0:m-t];    #the number of the first ball of the game
    Y_train = Y_train.T;
    Y_train = Y_train.astype(int)
    Y_train = keras.utils.to_categorical(Y_train, num_classes=61)   #turn it into on hot vector

    Y_test = data.values[7][m-t:m];
    Y_test = Y_test.T;
    Y_test = Y_test.astype(int)
    Y_test = keras.utils.to_categorical(Y_test, num_classes=61)
                

    dataset["X_train"] = X_train
    dataset["X_test"] = X_test
    dataset["Y_train"] = Y_train
    dataset["Y_test"] = Y_test
    
    return dataset

def predict(m, testNumber, epoch, batch_size, v):

    # m is the number of training examples ;
    # testNumber is the number of test examples
    # epoch for epochs;
    #  bat for batches;
    # v for verbose in model fit:
    # 0 = no progress is shown; 
    # 1 = progress bar; 
    # 2 = shows just the final loss and accuracy for each epoch

    #testing the model, I run: m1, l1, c1, y1 = predict(1900, 10, 10, 32,2);

    output = training(m, testNumber);

    i_shape = output["X_train"].shape[1] #input shape
    o_shape = output["Y_train"].shape[1] #output shape

    x_train = output['X_train']
    y_train = output['Y_train']
    x_test = output['X_test']
    y_test = output['Y_test']

    model = Sequential()
    model.add(Dense(150, activation='relu', input_dim=i_shape))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(80, activation='relu'))
    model.add(Dense(o_shape, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=epoch, batch_size=batch_size, verbose=v, validation_split=0.1, shuffle=True)

    loss_and_metrics = model.evaluate(x_test, y_test, batch_size=batch_size)

    classes = model.predict(x_test, batch_size=batch_size)

    return model, loss_and_metrics, classes, y_test

for number in range(45):
    predict(600, number+1, 10, 32,0)
    print("number:", number+1)
