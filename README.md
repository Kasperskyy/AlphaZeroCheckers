# AlphaZeroCheckers
A University Project iniitally created as a project for the subject Artificial Intelligence, and then expanded and improved.

## Overview
an AI for the board game known as American Checkers, using the AlphaZero approach: trained with no external data other than the rules of the game, it generates data by playing against itself and learning form these games, constantly improving. Adapted from the Original AlphaZero paper for chess and simplified for checkers. See: https://arxiv.org/pdf/1712.01815.pdf

## Getting Started
To start, run main.py. You will be presented with a menu of choices also described here:

## Generating 

First you must choose whether to use the saved model, or create a new one. CREATING A NEW ONE WILL OVERWRITE! Then, choose if you wish to generate more data or train the model on data generated from previous runs. This can be done in a loop(this is also implemented), training for X games and then training the model, with optional evaluation of the "best model" with the newly trained one and only accepting the new one if it is better. We first created data on multiple computers and then trained on one to save time, and also ommitted model evaluation after every training for time-related reasons. However the full AlphaZero algorithm code is implemented and can also be used. Threshold parameters and numbers of games can all be tweaked in the main.py file. Data is saved after each game, so the program can be closed ant any point and data should be saved without corruption. Data is saved as "TrainingData.txt". When choosing to train on generated data, the program matches and joins all files which have names that start with 'TrainingData', so simply name all generated data e.g. TrainingData1, TrainingData2 etc. to use them all for training.

## Testing

The program has 3 agents, a random agent, a human agent and an MCTS agent that uses the model saved as 'AlphaZeroCheckersModel'
To test, choose 2 on the main menu, and then select all parameteres as prompted. Console visualisation is possible. For more MCTS simulations per turn, the code for the MCTS agent must be modified in agent.py.

## AlphaZeroCheckersModel 

a model that has undergone training by us. It took about 2-3 weeks to train, with 1-3 PCs constantly generating data. Training was done every 1-3 days. It will always win against random agents and has managed to beat the hardest bots on some checkers websites that we have tested it against.
link: https://drive.google.com/file/d/1YcEe63C6MDwAJgruhwAWe1_-D4F0gcd0/view?usp=sharing


Checkers library used: https://pypi.org/project/imparaai-checkers/ implementing these rules of checkers: http://www.usacheckers.com/rulesofcheckers.php


MCTS library used as template and modified: https://pypi.org/project/imparaai-montecarlo/


## Cudadriver 
This file is for gpu training. 
Zawartość pliku powinna znajdować się w odpowiednim pliku z tworzeniem sieci neuronowej.

