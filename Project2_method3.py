__author__ = 'penghao'
from scipy import spatial
import numpy as np
import datetime

def getDataMatrix():
    infile = np.loadtxt('train.txt')
    dataMatrix = infile[:,:]
    return dataMatrix

def setKValidation(num): #num is 0 - 9 10-fold validation
    dataMatrix = getDataMatrix()
    x = np.arange(200)
    np.random.seed(0)
    np.random.shuffle(x) # x is a list of random number from 0 to 99
    y = np.split(x,10) # y is a set of arrary that cut the list by 10 slides
    z = x.tolist()
    for element in y[num]:
        z.remove(element)

    trainData = dataMatrix[z]
    testData = dataMatrix[y[num]]
    return trainData, testData #180 for training, 20 for testing

def setCorrelation(num): #num is 0 - 9 10-fold validation
    dataMatrix = calcorelation()
    x = np.arange(200)
    np.random.seed(0)
    np.random.shuffle(x) # x is a list of random number from 0 to 99
    y = np.split(x,10) # y is a set of arrary that cut the list by 10 slides
    z = x.tolist()
    for element in y[num]:
        z.remove(element)

    trainData = dataMatrix[z]
    testData = dataMatrix[y[num]]
    return trainData, testData #180 for training, 20 for testing

def calAve(vector):
    sum = 0.0
    count = 0.0
    for element in vector:
        if element !=0:
            sum = sum + element
            count += 1
    ave = sum/count
    return ave

def calcorelation(): #calculate the correaltion
    dataMatrix =  getDataMatrix()
    for i in range(0,200):
        ave = calAve(dataMatrix[i])
        for idx, element in enumerate(dataMatrix[i]):
            if element !=0:
                dataMatrix[i][idx] = dataMatrix[i][idx] - ave
    return dataMatrix

def calWeight(trainData, testVector,num):# adjust the matrix, remain the rate that both have the rating

    newtr =np.copy(trainData)
    newtest = np.copy(testVector)
    wList = []
    idxList = np.where(newtest == 0)
    idxList2 = np.where(newtr[num] == 0.0)
    finallist = idxList2[0].tolist() + idxList[0].tolist()
    setList = set(finallist)
    final = list(setList)
    newtr[num][final] = 0
    newtest[final] = 0

    if np.count_nonzero(newtr[num]) == 0:
        result = 0
    else:

        result = 1 - spatial.distance.cosine(trainData[num], testVector)

    return result

def calWeightList(k,trainData,testData): # k is 0 -9
    wList = []
    for i in range(0,180):
        w= calWeight(trainData,testData[k],i)
        wList.append(w)
    return wList

def modifyTrainData(trainData):
    modifyTrain = np.copy(trainData)
    aveRate = []
    for idx in range(0,180):
        sum = 0.0
        count = 0.0
        for num in trainData[idx]:
            if num !=0:
                sum = sum + num
                count = count + 1
        ave = sum/count
        aveRate.append(ave)
    for idx in range(0,180):
        for i, num in enumerate(modifyTrain[idx]):
            if num !=0:
                modifyTrain[idx][i] = num - aveRate[idx]

    return modifyTrain

def predict(k,w,trainData,testData):
    sum = 0.0
    count = 0.0
    for element in testData[k]:
        if element != 0:
            sum = sum + element
            count = count + 1
    testave = sum/ count

    mTrain = modifyTrainData(trainData)
    predictList = []
    sumW = 0
    for num in w:
        sumW = sumW + abs(num)

    sumAbove = []
    rateList = []
    for i in range(0,1000):
        for idx in range(0,180):
            sumAll = 0
            rate = mTrain[:,i]
            weight = w[idx]
            for num in rate:
                sumAll = sumAll + num*weight
        predictRate = testave + sumAll/sumW
        rateList.append(predictRate)
        sumAbove.append(sumAll)

    return rateList

def testAccuracy(k,prediction,testData,flag):
    count = 0
    countAcc = 0
    if flag == 1:
        for idx, num in enumerate(testData[k]):
            if num !=0:
                count += 1

                if round(prediction[idx]) == num:

                    countAcc += 1
    if flag == 2:
        for idx, num in enumerate(testData[k]):
            if num !=0:
                count += 1

                if round(prediction[idx]) == num or round(prediction[idx]) == num + 1 or round(prediction[idx]) == num - 1:

                    countAcc += 1

    return count, countAcc

def MAE(k,prediction,testData,flag):
    count = 0
    countAcc = 0
    mae =0.0
    if flag == 1:
        for idx, num in enumerate(testData[k]):
            if num !=0:
                count += 1
                mae +=abs(round(prediction[idx]) -num)
                    #countAcc += 1
    return count, mae

def CrossValidation1(num):
    trainData, testData = setKValidation(num)
    wTrainData, wTestData = setCorrelation(num)
    totalRateNum = 0.0
    accPrediction = 0.0
    accRateSum= 0.0
    for i in range(0,20):
        #i=8
        w = calWeightList(i,wTrainData,wTestData)  # wlist

        preList = predict(i,w,trainData,testData)
        total, acc = testAccuracy(i,preList,testData,1)
        countnumber, maeTotal = MAE(i,preList,testData,1)
        mae = float(maeTotal)/float(countnumber)
        #totalRateNum += total
        #accPrediction += acc
        accRate = float(acc)/float(total)
        accRateSum +=accRate
    #print accRateSum/20.0
    print mae

def main():
    a = datetime.datetime.now().replace(microsecond=0)
    for i in range(10):

        CrossValidation1(i)
    b = datetime.datetime.now()
    print(b-a)

if  __name__ =='__main__':
    main()
