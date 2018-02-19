import numpy as np
import matplotlib.pyplot as plt

def deltaLoss(x, y, w0, w1):
    # Calculates the differential of the loss function
    dw0 = 0
    dw1 = 0
    length = len(x)
    for i in range(length):
        dw0 -= 2 / length * (y[i] - (w0 + w1 * x[i]))
        dw1 -= 2 / length * x[i] * (y[i] - (w0 + w1 * x[i]))
    return dw0, dw1

def regressionBatch(dataset, alfa, eps):
    w0 = 0
    w1 = 0
    x = dataset[:,0]
    y = dataset[:,1]
    q = len(dataset)
    count = 0
    dLoss = deltaLoss(x, y, w0,w1)
    norm = np.linalg.norm(dLoss)
    while norm > eps:
        w0 -= alfa / q * dLoss[0]
        w1 -= alfa / q * dLoss[1]
        dLoss = deltaLoss(x, y, w0, w1)
        norm = np.linalg.norm(dLoss)
        count += 1
        alfa = 1000 / (1000 + len(x))
    return w0, w1, count        

def regressionStoch(dataset, alfa, eps):
    w0 = 0
    w1 = 0
    norm = 1
    x = []
    y = []
    count = 0
    while norm > eps:
        i = np.random.randint(15)
        x = np.append(x, dataset[i,0])
        y = np.append(y, dataset[i,1])
        count += 1
        xlast = x[-1]
        ylast = y[-1]
        w0 = w0 + alfa * (ylast - (w0 + w1 * xlast))
        w1 = w1 + alfa * xlast * (ylast - (w0 + w1 * xlast))
        norm = np.linalg.norm(deltaLoss(x, y, w0,w1))
        alfa = 1000 / (1000 + len(x))
    return w0, w1, count

# Load data
data_en = np.loadtxt('salammbo_a_en.txt')
data_fr = np.loadtxt('salammbo_a_fr.txt')


# Data processing
max_noc =  max(max(data_en[:,0]), max(data_fr[:,0]))
max_noA = max(max(data_en[:,1]), max(data_fr[:,1]))
data_en[:,0] /= max_noc
data_en[:,1] /= max_noA
data_fr[:,0] /= max_noc
data_fr[:,1] /= max_noA

# Batch gradient descent
regBatch_en = regressionBatch(data_en, 0.8, 0.001)
regBatch_fr = regressionBatch(data_fr, 0.8, 0.001)

plt.plot(data_en[:,0], data_en[:,1], 'r+')
plt.plot(data_fr[:,0], data_fr[:,1], 'g+')
x = np.linspace(0,1)
plt.plot(x, regBatch_en[0] + regBatch_en[1] * x, 'r')
plt.plot(x, regBatch_fr[0] + regBatch_fr[1] * x, 'g')

# Stochastic gradient descent
plt.figure()
regStoch_en = regressionStoch(data_en, 0.8, 0.001)
regStoch_fr = regressionStoch(data_fr, 0.8, 0.001)

plt.figure()
plt.plot(data_en[:,0], data_en[:,1], 'r+')
plt.plot(data_fr[:,0], data_fr[:,1], 'g+')
plt.plot(x, regStoch_en[0] + regStoch_en[1] * x, 'r')
plt.plot(x, regStoch_fr[0] + regStoch_fr[1] * x,'g')

