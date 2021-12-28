import os
import pathlib
import keras.models
import ResNetCheckers
import gamePlayer
import Training
import pickle
from keras import backend as k

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

load = int(input("press 1 to create new model[WARNING THIS WILL OVERWRITE THE MODEL SAVED CURRENTLY] or press any other number to load saved model"))

model = keras.models.load_model('AlphaZeroCheckersModel')  ###path of file here
confirm = ''
if model is not None and load == 1:
    confirm = input("Are you sure you want to overwrite your model? type 'confirm' to confirm")
if model is None or confirm == 'confirm':
    # from scratch
    myNetwork = ResNetCheckers.Network()
    model = myNetwork.getModel()
    model.save('AlphaZeroCheckersModel')  ###path of file here

allData = []
trainingData = []

while True:
    print("Choose 1 for generation and training options\n")
    print("Choose 2 to test current model against other agents\n")
    print("Choose 3 to quit\n")
    mainMenu = int(input("Choose mode:\n"))
    if mainMenu == 1:     

        choice = int(input(
                "press 1 to create training data through playing games, press 2 to train the current model on all currently saved data or press 3 to run the full AlphaZeroAlgorithm loop"))

        # Creating training data through playing X games

        if choice == 2 or choice == 3:
            print("What learning rate do you wish to use? \n")
            learning_Choice = int(input("press 1 to give your rate or press any other number to use default rate (0.0001)"))
            # Training.trainNetwork(model, trainingData)
            # newModel = keras.models.load_model('AlphaZeroCheckersModel')  ###path of file here
            if learning_Choice == 1:
                learningRate = float(input("Give your learning rate"))
                k.set_value(model.optimizer.learning_rate, learningRate)
            else:
                k.set_value(model.optimizer.learning_rate, 0.0001)

        # Loading training data
        if choice == 2:
            path = pathlib.Path(__file__).parent.resolve()
            print("Loading data from the project directory: ", path,
                    "\n")  # or from current directory -> directory = os.getcwd()
            with os.scandir(path) as files:
                for file in files:
                    if file.is_file():
                        if file.name.startswith('TrainingData') is True:
                            print(len(allData))
                            with open(file, "rb") as fp:  # Unpickling
                                trainingData = pickle.load(fp)
                                allData = allData + trainingData
                                print(file.name)
                                print(len(allData))
            # Training data

            Training.trainNetwork(model, trainingData)
            model.save('AlphaZeroCheckersModel')  ###path of file here
            print("model saved!")
        else:
            if choice == 1:
                print("Creating data through playing games:\n")
                iterations = 1
            else:
                print("executing AlphaZero algorithm[WARNING: THIS WILL OVERWRITE THE SAVED MODEL]:\n")
                iterations = int(input("Give how many iterations of the algorithm you wish to complete:"))
                evaluation = int(input("Do you wish to enable evaluation? Evaluation puts the most recently trained model against the current best in a series of matches.\n The most recently model is only accepted as the new best model if it wins a certain threshold of games. 1 to enable evaluation, 0 to disable\n"))
                if evaluation == 1:
                    newModel = keras.models.load_model('AlphaZeroCheckersModel')  ###path of file here
                    frequency = int(input("Per how many iterations do you wish to evaluate?"))
                    evalGames = int(input("How many games per evaluation?"))
                    threshold_win = int(input("How many evaluation games should a model win to be accepted as the new best?"))
                    threshold_loss = int(input("How many evaluation games should a model lose at most to be accepted as the new best?"))
                else:
                    print("It is recommended to play more games without evaluation as only the most recent batch of games will be used")
            no_games = int(input("Give a number of games you wish to self-generate:\n"))
            simulations = int(input(
                "How many MCTS simulations per turn? Default: 50, cannot be less than 2. The more games the 'better' the decisions of the bot, but games take significantly longer"))
            if simulations < 2:
                simulations = 50
            allData = []
            for i in range(iterations):
                print("iteration: ", i)
                trainingData = gamePlayer.selfplay(no_games, model, simulations)  # generate self play data               
                print("all games completed!")
                if choice == 3:
                    print("Training")
                    if evaluation == 1:
                        allData += trainingData
                        Training.trainNetwork(newModel, allData)  # training loop
                        if i % (frequency-1) == 0 and i != 0:
                            print("Evaluating Default MCTS simulations in Eval code is 100, refer to Agent.py file to change")
                            wins, losses = gamePlayer.evaluate(model, newModel, evalGames)
                            if wins >= threshold_win and losses < threshold_loss:
                                print("Eval passed!")
                                model = newModel #the new best model
                                model.save('AlphaZeroCheckersModel')
                            allData = []
                            newModel = keras.models.load_model('AlphaZeroCheckersModel')#try again
                    else:
                        Training.trainNetwork(model, trainingData)  # training loop            
    elif mainMenu == 2:
        numGames = int(input("How many games do you wish to run?"))
        print("Players:\n")
        print("0 -> human player\n")
        print("1 -> random player\n")
        print("2 -> AlphaZero player\n")
        player1 = int(input("Choose first player:\n"))
        player2 = int(input("Choose second player:\n"))
        victories, draws = gamePlayer.evaluateplayer(model, numGames, player1, player2)
        print("Victories " + str(victories/numGames) + " Draws " + str(draws/numGames))
    else:
        break
