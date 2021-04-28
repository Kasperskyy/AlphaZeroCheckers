from copy import deepcopy
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo
from checkers.game import Game
from tensorflow.keras.models import Model
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Lambda
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
import tensorflow as tf
from tensorflow.python.keras.layers import ReLU, Add

game = Game()
chess_game = Game()
montecarlo = MonteCarlo(Node(chess_game))


def build():
    # initialize the input shape and channel dimension (this code
    # assumes you are using TensorFlow which utilizes channels
    # last ordering)
    inputShape = (8, 8)
    # construct both the "category" and "color" sub-networks
    inputs = Input(shape=inputShape)

    # categoryBranch = FashionNet.build_category_branch(inputs,
    #                                                   numCategories, finalAct=finalAct, chanDim=chanDim)
    # colorBranch = FashionNet.build_color_branch(inputs,
    #                                             numColors, finalAct=finalAct, chanDim=chanDim)
    # # create the model using our input (the batch of images) and
    # # two separate outputs -- one for the clothing category
    # # branch and another for the color branch, respectively
    # model = Model(
    #     inputs=inputs,
    #     outputs=[categoryBranch, colorBranch],
    #     name="fashionnet")
    # # return the constructed network architecture

    return model

def buildPolicyHead(inputs):
    policy = Conv2D(filters=1,kernel_size=1,strides=1)(inputs)
    #to be continued
    # policy =
def buildValueHead(inputs):
#finish

def buildConvLayer(inputs):
    conv = Conv2D(padding='same', filters=256, strides=1, kernel_size=3)
    conv = relu_bn(conv)
    return conv


def buildResLayer(inputs):
    block = buildConvLayer(inputs)
    block = Conv2D(padding='same', filters=256, strides=1, kernel_size=3)(inputs)
    block = BatchNormalization()(block)
    skip = Add()[inputs, block]
    skip = ReLU()(skip)
    return skip


def relu_bn(inputs: tf) -> tf:
    relu = ReLU()(inputs)
    bn = BatchNormalization()(relu)
    return bn
