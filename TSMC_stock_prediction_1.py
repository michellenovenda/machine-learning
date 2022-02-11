# -*- coding: utf-8 -*-
"""108062281_basic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1McNbWgtUCp-LBOt4kgC9TwbazIk2jUnA
"""

#!/usr/bin/env python
# coding: utf-8

# import packages
import numpy as np
import matplotlib.pyplot as plt
import csv
import math
import random

# Global attributes
StudentID = '108062281'
input_dataroot = 'input.csv'
output_dataroot = StudentID + '_basic_prediction.csv'

input_datalist =  []
output_datalist =  []

# You can add your own global attributes here
trainingData = []
testData = []
xTrain = [] #MTK
yTrain = [] #TSMC
xTest = []
yTest = []
dates = []

with open(input_dataroot, newline='') as csvfile:
    input_datalist = np.array(list(csv.reader(csvfile)))
# print(input_datalist)

totalData = len(input_datalist)

def SplitData():
  global trainingData, testData, input_datalist, totalData
  dateList = []
  idx = 0
  for rows in input_datalist:
    dataPredict = rows[0].split()
    date = dataPredict[0].split('/')
    year = str(date[0])
    month = str(date[1])
    day = str(date[2])
    if(len(month) == 1):
      month = '0' + month
    if(len(day) == 1):
      day = '0' + day
    curDate = year + '-' + month + '-' + day
    currentDate = np.datetime64(curDate)
    dateList.append(currentDate)
  #Remember to change the starting date!
  startingIdx = dateList.index(np.datetime64('2021-10-15'))
  trainingData = input_datalist[:startingIdx]
  testData = input_datalist[startingIdx:totalData]

def PreprocessData():
  global trainingData, testData, xTrain, yTrain, xTest, yTest, dates
  xTemp = []
  yTemp = []
  datesTemp = []

  #append training datas of MTK and TSMC to an empty list.
  for datas in trainingData:
    xTemp.append(datas[1].split())
    yTemp.append(datas[2].split())
  for elm in xTemp:
    xTrain.append(int(elm[0]))
  for elm in yTemp:
    yTrain.append(int(elm[0]))
  xTrain = np.array(xTrain)
  yTrain = np.array(yTrain)
  
  #get the dates of the test data, which is 10/15-11/11.
  for dt in testData:
    datesTemp.append(dt[0].split())
  for date in datesTemp:
    dates.append(date[0])
  
  #testing purposes.
  #====================================
  xTmp = []
  for datas in testData:
    xTmp.append(datas[1].split())
  for elm in xTmp:
    xTest.append(int(elm[0]))
  xTest = np.array(xTest)
  #====================================

def Regression():
  global xTrain, yTrain
  model = np.polyfit(xTrain, yTrain, 3)
  return model

def CountLoss():
  #calculate RMSE
  global testData, yTest
  countScoreTemp = []
  countScore = []
  for accurates in testData:
    countScoreTemp.append(accurates[2].split())
  for temps in countScoreTemp:
    countScore.append(int(temps[0]))
  countScoreArr = np.array(countScore)
  yTestArr = np.array(yTest)
  MSE = np.square(np.subtract(countScoreArr, yTestArr)).mean()
  RMSE = math.sqrt(MSE)
  return RMSE

def calculateMAPE():
  #replace the 0s in TSMC with actual datas
  global testData, yTest
  countScoreTemp = []
  countScore = []
  for accurates in testData:
    countScoreTemp.append(accurates[2].split())
  for temps in countScoreTemp:
    countScore.append(int(temps[0]))
  countScoreArr = np.array(countScore)
  yTestArr = np.array(yTest)
  return np.mean(np.abs((countScoreArr-yTestArr)/countScoreArr))*100

def MakePrediction(model):
  global xTest, yTest
  predict = np.poly1d(model)
  for data in xTest:
    yTest.append(predict(data))

SplitData()
PreprocessData()
regressionModel = Regression()
a = regressionModel[0]
b = regressionModel[1]
c = regressionModel[2]
d = regressionModel[3]
MakePrediction(regressionModel)

temp = []
elmTemp = []
i = 0
while i < len(yTest):
  elmTemp.append(dates[i])
  elmTemp.append(int(yTest[i]))
  temp.append(elmTemp)
  elmTemp = []
  i += 1
output_datalist = np.array(temp)

print("RMSE", CountLoss())
# print("MAPE", calculateMAPE())

plt.figure(figsize=(16, 8))
plt.title("Stock Price History")
plt.xlabel('MTK', fontsize=18)
plt.ylabel('TSMC', fontsize=18)
plt.scatter(xTrain, yTrain)
plt.scatter(xTest, yTest)
plt.plot(xTrain, (a*(xTrain**3)+b*(xTrain**2)+c*xTrain+d))

# Write prediction to output csv
with open(output_dataroot, 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # writer.writerow(['Date', 'TSMC Price'])
    
    for row in output_datalist:
        writer.writerow(row)