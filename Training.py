import numpy as np
import tensorflow as tf
def trainNetwork(model, trainingData):
    #x, yPolicy, yValue = list(zip(*trainingData))
    x = [i[0] for i in trainingData]
    x = np.asarray(x)
    yPolicy = [i[1] for i in trainingData]
    yPolicy = np.asarray(yPolicy)
    yValue = [i[2] for i in trainingData]
    yValue = np.asarray(yValue)
    model.fit(x=x, y=[yPolicy, yValue], batch_size=2048, epochs=10, verbose=1)

