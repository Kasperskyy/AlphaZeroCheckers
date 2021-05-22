import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import keras.models
import ResNetCheckers
import main
import Training
from keras import backend as k

# !!!!!  When loading a model instead of making a new one, uncomment the loadfile command

# from scratch
myNetwork = ResNetCheckers.Network()
model = myNetwork.getModel()

# from file
#model = keras.models.load_model('AlphaZeroCheckersModel') ###path of file here
#k.set_value(model.optimizer.learning_rate, 0.0001)

# [print(i.shape, i.dtype) for i in model.inputs]
# [print(o.shape, o.dtype) for o in model.outputs]

for i in range(1000):
    print("iteration: ",i)
    trainingData = main.selfplay(100, model)  # generate self play data


    # ##the next 6 lines can be commented to omit evaluation
    #newModel = myNetwork.build()   #create new model to train
    # newModel.set_weights(model.get_weights()) #copy weights
    #Training.trainNetwork(newModel, trainingData) # training loop
    #isNewNetworkBetter = main.evaluate(model, model, 100) #evaluate model
    #print(main.evaluate(model, model, 10))
    # if isNewNetworkBetter == True:
    #   model = newModel
    Training.trainNetwork(model, trainingData)
    # if i % 10 == 0:
   # model.save('AlphaZeroCheckersModel')  ###path of file here
  #  print("model saved!")
