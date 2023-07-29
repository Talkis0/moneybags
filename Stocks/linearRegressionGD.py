import csv
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

current_folder = os.getcwd()
print(current_folder)
priceData = current_folder + '\\' + 'Stocks_daily' + '\\' + 'BA.csv'
with open(priceData, "r", newline='') as csvfile:
    reader = csv.reader(csvfile)
    openData = []
    highData = []
    lowData = []
    closeData = []
    volumeData = []
    for row in reader:
        openData.append(row[1])
        highData.append(row[2])
        lowData.append(row[3])
        closeData.append(row[4])
        volumeData.append(row[6])
        
        # Process each row of the CSV file as needed
        # print(row)

# files = os.listdir(priceData)

# print('\n',files)
# print(openData)



adjOpen = []
adjHigh = []
adjLow = []
adjClose = []
adjVol = []
targetPrice = []
print('\n', len(openData))
for i in range(len(openData)-2, len(openData)-1827, -1):
    # print(openData[i])
    # print(i)
    adjOpen.append(float(openData[i]))
    adjHigh.append(float(highData[i]))
    adjLow.append(float(lowData[i]))
    adjClose.append(float(closeData[i]))
    adjVol.append(float(volumeData[i]))
    targetPrice.append(float(closeData[i+1]))


print('\n',len(adjOpen))

m = 1825 # number of training examples
x = 5 # input variables
y = 1 # output variable or target variable
thetas = []
x = [adjOpen, adjHigh, adjLow, adjClose, adjVol]
y = [targetPrice]

xT = np.transpose(x)
yT = np.transpose(y)
# print(x)
theta = np.matmul(np.matmul(np.linalg.inv(np.matmul(x,xT)),x),yT)


print(theta)

testOpen = []
testHigh = []
testLow = []
testClose = []
testVol = []
testTargetPrice = []
xTest = []
# print('\n', len(openData)-1825)
for i in range(len(openData)-1828,len(openData)-1900 , -1):
    # print(openData[i])
    # print(i)
    xTest.append(float(openData[i])*theta[0]+float(highData[i])*theta[1]+float(lowData[i])*theta[2]+float(closeData[i])*theta[3]+float(volumeData[i])*theta[4])
    # testOpen.append(float(openData[i]))
    # testHigh.append(float(highData[i]))
    # testLow.append(float(lowData[i]))
    # testClose.append(float(closeData[i]))
    # testVol.append(float(volumeData[i]))
    testTargetPrice.append(float(closeData[i+1]))

fig, ax = plt.subplots()
ax.plot(xTest, color='blue')
ax.plot(testTargetPrice, color='orange')
ax.legend()
plt.show()
