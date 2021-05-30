import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'


def trainNetwork(model, trainingData):
    x = [i[0] for i in trainingData]
    x = np.asarray(x)
    yPolicy = [i[1] for i in trainingData]
    yPolicy = np.asarray(yPolicy)
    yValue = [i[2] for i in trainingData]
    yValue = np.asarray(yValue)
    model.fit(x=x, y=[yPolicy, yValue], batch_size=64, epochs=15, verbose=1)
