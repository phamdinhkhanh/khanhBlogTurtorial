from keras.applications import MobileNet
import argparse
from tensorflowjs import tfjs


model = MobileNet(weights = 'imagenet')
# model.save('mobile.h5')
tfjs.converters.save_keras_model(model, 'imagenet')	