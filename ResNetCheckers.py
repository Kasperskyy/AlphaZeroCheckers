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
from tensorflow.python.keras.utils.vis_utils import plot_model



def build():
    inputShape = (4, 8, 17)
    inputs = Input(shape=inputShape)
    network = buildConvLayer(inputs)
    for i in range(10):
        network = buildResLayer(network)
    value_head = buildValueHead(network)
    policy_head = buildPolicyHead(network)
    model = Model(inputs, [policy_head, value_head])
    return model


def buildValueHead(inputs):
    value = Conv2D(filters=1, kernel_size=1, strides=1)(inputs)
    value = bn_relu(value)
    value = Flatten()(value)
    value = Dense(256)(value)
    value = ReLU()(value)
    value = Dense(1, activation='tanh')(value)
    return value


def buildPolicyHead(inputs):
    policy = Conv2D(filters=32, kernel_size=1, strides=1)(inputs)
    policy = bn_relu(policy)
    policy = Flatten()(policy)
    policy = Dense(1024, activation='softmax')(policy)      # 32 x 4 x 8
    return policy


def buildConvLayer(inputs):
    conv = Conv2D(padding='same', filters=256, strides=1, kernel_size=3)(inputs)
    conv = bn_relu(conv)
    return conv


def buildResLayer(inputs):
    block = buildConvLayer(inputs)
    block = Conv2D(padding='same', filters=256, strides=1, kernel_size=3)(inputs)
    block = BatchNormalization()(block)
    skip = Add()([inputs, block])
    skip = ReLU()(skip)
    return skip


def bn_relu(inputs):
    relu = BatchNormalization()(inputs)
    bn = ReLU()(relu)
    return bn


#plot_model(theModel, to_file='model_plot.png', show_shapes=True, show_layer_names=False)
