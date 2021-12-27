import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
import keras.models
import ResNetCheckers
import gamePlayer
import Training
import pickle
from keras import backend as k


load = int(input("press 1 to create new model[WARNING THIS WILL OVERWRITE THE MODEL SAVED CURRENTLY] or press any other number to load saved model"))

model = keras.models.load_model('AlphaZeroCheckersModel')  ###path of file here
if model is not None and load == 1:
    confirm = input("Are you sure you want to overwrite your model? type 'confirm' to confirm")
if confirm == 'confirm' or model is None:
    # from scratch
    myNetwork = ResNetCheckers.Network()
    model = myNetwork.getModel()
    model.save('AlphaZeroCheckersModel')  ###path of file here




additionalData = []
trainingData = []
    # with open("TrainingDataAll.txt", "rb") as fp:   # Unpickling
    #   trainingData = pickle.load(fp)
# k.set_value(model.optimizer.learning_rate, 0.0001)
# victory_threshold = 0.51
#drawC=0
#winC=0
#lossC=0
#for i in trainingData:
 #   if i[2] == 1:
  #      winC+=1
   # elif i[2] == 0:
    #    drawC +=1
    #else:
    #    lossC +=1
#with open("TrainingData.txt", "rb") as fp:   # Unpickling
   #additionalData = pickle.load(fp)
#newAdd = additionalData[:len(additionalData)-86]
#with open("TrainingData.txt", "wb") as fp:
   #pickle.dump(newAdd, fp)
#print(model.summary())
print("Choose 1 to generate self play and train\n")
print("Choose 2 to test against other agents\n")
choice = int(input("Choose mode:\n"))
if choice == 1:
    for i in range(1):
        print("iteration: ", i)
        trainingData = gamePlayer.selfplay(2000, model)  # generate self play data
        #model.save('AlphaZeroCheckersModel')  ###path of file here
        with open("TrainingData.txt", "wb") as fp:
            pickle.dump(trainingData, fp)

        #trainingData = trainingData + additionalData
        #newModel = keras.models.load_model('AlphaZeroCheckersModel')  ###path of file here
        #k.set_value(newModel.optimizer.learning_rate, 0.0001)
        #Training.trainNetwork(newModel, trainingData)  # training loop

        # ##the next 6 lines can be commented to omit evaluation
        #isNewNetworkBetter = gamePlayer.evaluate(model, newModel, 1)  # evaluate model #CHANGE TO 50 GIER
        # print(main.evaluate(model, model, 10))

        #if isNewNetworkBetter > victory_threshold:
        #    print(str(isNewNetworkBetter))
        #    model = newModel
        #    print("test passed!")
        #    additionalData = []
        #    model.save('AlphaZeroCheckersModel')  ###path of file here
        #    print("model saved!")
        #else:
        #    print("test failed!")
        #    print(str(isNewNetworkBetter))
        #    additionalData = trainingData
        #    with open("TrainingData.txt", "wb") as fp:
            #    pickle.dump(trainingData, fp)
        #Training.trainNetwork(model, trainingData)
        # if i % 10 == 0:
        #model.save('AlphaZeroCheckersModel')  ###path of file here
        #print("model saved!")
else:
    numgame = 100
    print("Players:\n")
    print("0 -> human player\n")
    print("1 -> random player\n")
    print("2 -> alphazero player\n")
    player1 = int(input("Choose first player:\n"))
    player2 = int(input("Choose second player:\n"))
    victories, draws = gamePlayer.evaluateplayer(model, numgame, player1, player2)
    print("Victories " + str(victories/numgame) + " Draws " + str(draws/numgame))
