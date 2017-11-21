import tensorflow as tf
import RadarImage
from subnet.AlexnetTiny import *
import Settings as settings

class IceNet:
	def __init__(self):
		self.isTraining = tf.placeholder(tf.bool)
		self.inputImage = tf.placeholder(tf.float32, 
						 [None, RadarImage.DATA_WIDTH, RadarImage.DATA_HEIGHT, RadarImage.DATA_CHANNELS])
		self.inputAngle = tf.placeholder(tf.float32, [None, 1])
		self.groundTruth = tf.placeholder(tf.float32, [None, settings.NUMBER_OF_CATEGORIES])

		self.subnet = AlexnetTiny(self.isTraining, self.inputImage, self.inputAngle, self.groundTruth)

	def Build(self):

		netOutput = self.subnet.Build()
		cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=netOutput, labels=self.groundTruth))
		accuracy = self.calculateAccuracy(netOutput, self.groundTruth)

		return cost, accuracy

	def calculateAccuracy(self, netOutput_, groundTruth_):
		correctPredictions = tf.equal(tf.argmax(netOutput_, 1), tf.argmax(groundTruth_, 1))
		correctPredictions = tf.reshape(correctPredictions, shape=[-1])

		accuracy = tf.reduce_mean(tf.cast(correctPredictions, tf.float32))
		return accuracy