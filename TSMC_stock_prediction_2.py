# -*- coding: utf-8 -*-
"""108062281_bonus.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m0-N0iQEGIUvEuph5Xk9kBme6KcgxhlA
"""

import pandas as pd
import numpy as np
import csv
import math
import matplotlib.pyplot as plt
import tensorflow as tf
from numpy import array
from sklearn.preprocessing import MinMaxScaler #=> transform value between 0 to 1
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

# Global attributes
StudentID = '108062281'
output_dataroot = StudentID + '_bonus_prediction.csv'

df = pd.read_csv("inputBonus.csv")
dfPrice = df.reset_index()["TSMC"]

def preprocessData(data, timestep):
  Xdata = []
  Ydata = []
  size = len(data)
  for i in range(size-timestep-1):
    arr = data[i:(i+timestep), 0]
    Xdata.append(arr)
    Ydata.append(data[i+timestep, 0])
  return np.array(Xdata), np.array(Ydata)

scaler = MinMaxScaler(feature_range=(0,1))
dfPrice = scaler.fit_transform(np.array(dfPrice).reshape(-1,1)) #transform to between 0 and 1

dataSize = len(dfPrice)
trainSize = int(dataSize*0.65)
testSize = dataSize - trainSize
trainData = dfPrice[0:trainSize,:]
testData = dfPrice[trainSize:dataSize,:1]

timestep = 100
xTrain, yTrain = preprocessData(trainData, timestep)
xTest, yTest = preprocessData(testData, timestep)
xTrain = xTrain.reshape(xTrain.shape[0], xTrain.shape[1], 1)
xTest = xTest.reshape(xTest.shape[0], xTest.shape[1], 1)

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(100,1)))
model.add(LSTM(50, return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(xTrain, yTrain, validation_data=(xTest, yTest), epochs=100, batch_size=64, verbose=1)

trainPredict = model.predict(xTrain)
testPredict = model.predict(xTest)

trainPredict = scaler.inverse_transform(trainPredict)
testPredict = scaler.inverse_transform(testPredict)
print("RMSE yTrain:", math.sqrt(mean_squared_error(yTrain, trainPredict)))
print("RMSE yTest:", math.sqrt(mean_squared_error(yTest, testPredict)))

steps = 100
trainPredictPlot = np.empty_like(dfPrice)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[steps:len(trainPredict)+steps, :] = trainPredict

testPredictPlot = np.empty_like(dfPrice)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(steps*2)+1:len(dfPrice)-1, :] = testPredict

plt.plot(scaler.inverse_transform(dfPrice))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()

xInput = testData[len(testData)-100:].reshape(1, -1)
xList = list(xInput)
xList = xList[0].tolist()

outputData = []
n = 100
i = 0
while(i < 20):
  if(len(xList) > 100):
    xInput = np.array(xList[1:])
    xInput = xInput.reshape(1, -1)
    xInput = xInput.reshape((1, n, 1))
    yPred = model.predict(xInput, verbose=0)
    xList.extend(yPred[0].tolist())
    xList = xList[1:]
    outputData.extend(yPred.tolist())
    i = i + 1
  else:
    xInput = xInput.reshape((1, n, 1))
    yPred = model.predict(xInput, verbose=0)
    xList.extend(yPred[0].tolist())
    outputData.extend(yPred.tolist())
    i = i + 1

dfRes = dfPrice.tolist()
dfRes.extend(outputData)

newData = dfPrice.tolist()
newData.extend(outputData)
predictedData = []
predictedData.extend(outputData)
finalData = scaler.inverse_transform(newData).tolist()
finalPredictData = scaler.inverse_transform(predictedData).tolist()

outputDates = ['2021/10/15', '2021/10/18', '2021/10/19', '2021/10/20', '2021/10/21', '2021/10/22', '2021/10/25', '2021/10/26', '2021/10/27', '2021/10/28', '2021/10/29', 
               '2021/11/1', '2021/11/2', '2021/11/3', '2021/11/4', '2021/11/5', '2021/11/8', '2021/11/9', '2021/11/10', '2021/11/11']

storePrediction = []
for prices in finalPredictData:
  storePrediction.append(prices[0])

temp = []
elmTemp = []
idx = 0
while(idx < len(storePrediction)):
  elmTemp.append(outputDates[idx])
  elmTemp.append(int(storePrediction[idx]))
  temp.append(elmTemp)
  elmTemp = []
  idx = idx + 1
output_datalist = np.array(temp)

# Write prediction to output csv
with open(output_dataroot, 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    for row in output_datalist: #finalPredictData:
        writer.writerow(row)

