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
        inputShape = (4, 8, 17)
        inputs = Input(shape=inputShape)
        network = self.buildConvLayer(inputs)
        for i in range(10):
            network = self.buildResLayer(network)
        value_head = self.buildValueHead(network)
        policy_head = self.buildPolicyHead(network)
        model = Model(inputs, [policy_head, value_head])
        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=tf.keras.optimizers.Adam(0.2))
        return model

    def buildValueHead(self, inputs):
        value = Conv2D(filters=1, kernel_size=1, strides=1)(inputs)
        value = self.bn_relu(value)
        value = Flatten()(value)
        value = Dense(256)(value)
        value = ReLU()(value)
        value = Dense(1, activation='tanh')(value)
        return value

    def buildPolicyHead(self, inputs):
        policy = Conv2D(filters=32, kernel_size=1, strides=1)(inputs)
        policy = self.bn_relu(policy)
        policy = Flatten()(policy)
        policy = Dense(256, activation='softmax')(policy)  # 32 x 4 x 8
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

# plot_model(theModel, to_file='model_plot.png', show_shapes=True, show_layer_names=False)
