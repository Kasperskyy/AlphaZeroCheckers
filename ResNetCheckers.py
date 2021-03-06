## IMPORTS


from tensorboard.compat.proto.config_pb2 import ConfigProto


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




class Network:
    def __init__(self):
        self.theModel = self.build()

    def getModel(self):
        return self.theModel

    def build(self):
        inputShape = (4, 8, 5)
        inputs = Input(shape=inputShape)
        network = self.buildConvLayer(inputs)
        for i in range(5):
            network = self.buildResLayer(network)
        value_head = self.buildValueHead(network)
        policy_head = self.buildPolicyHead(network)
        model = Model(inputs, [policy_head, value_head])
        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=tf.keras.optimizers.Adam(0.0001))
        return model

    def buildValueHead(self, inputs):
        value = Conv2D(filters=1, kernel_size=1, strides=1)(inputs)
        value = self.bn_relu(value)
        value = Flatten()(value)
        value = Dense(256)(value)
        value = ReLU()(value)
        initializer = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.005, seed=None)
        value = Dense(1, activation='tanh', kernel_initializer=initializer)(value)
        return value

    def buildPolicyHead(self, inputs):
        policy = Conv2D(filters=2, kernel_size=1, strides=1)(inputs)
        policy = self.bn_relu(policy)
        policy = Flatten()(policy)
        initializer = tf.keras.initializers.RandomNormal(mean=0.5, stddev=0.05, seed=None)
        policy = Dense(256, activation='softmax', kernel_initializer=initializer)(policy)  # 32 x 8
        return policy

    def buildConvLayer(self, inputs):
        conv = Conv2D(padding='same', filters=256, strides=1, kernel_size=3)(inputs)
        conv = self.bn_relu(conv)
        return conv

    def buildResLayer(self, inputs):
        block = self.buildConvLayer(inputs)
        block = Conv2D(padding='same', filters=256, strides=1, kernel_size=3)(inputs)
        block = BatchNormalization()(block)
        skip = Add()([inputs, block])
        skip = ReLU()(skip)
        return skip

    def bn_relu(self,inputs):
        relu = BatchNormalization()(inputs)
        bn = ReLU()(relu)
        return bn

