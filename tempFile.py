import ResNetCheckers
import main
import Training
import numpy as np
myNetwork = ResNetCheckers.Network()
model = myNetwork.getModel()
#[print(i.shape, i.dtype) for i in model.inputs]
#[print(o.shape, o.dtype) for o in model.outputs]
trainingData = main.selfplay(1, model)
Training.trainNetwork(model, trainingData)
main.evaluate(model,model,2)
