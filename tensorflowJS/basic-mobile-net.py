# organize imports
import numpy as np
from keras.preprocessing import image
from keras.models import Model
from keras.applications import imagenet_utils, mobilenet
import tensorflowjs as tfjs

# process an image to be mobilenet friendly
def process_image(img_path):
	img = image.load_img(img_path, target_size=(224, 224))
	img_array = image.img_to_array(img)
	img_array = np.expand_dims(img_array, axis=0)
	pImg = mobilenet.preprocess_input(img_array)
	return pImg

# main function
if __name__ == '__main__':

	# path to test image
	test_img_path = "G:\\git-repos\\mobile-net-projects\\dataset\\test\\test_image_1.jpg"

	# process the test image
	pImg = process_image(test_img_path)

	# define the mobilenet model
	mobilenet = mobilenet.MobileNet()

	# make predictions on test image using mobilenet
	prediction = mobilenet.predict(pImg)

	# obtain the top-5 predictions
	results = imagenet_utils.decode_predictions(prediction)
	print(results)

	# convert the mobilenet model into tf.js model
	save_path = "output\\mobilenet"
	tfjs.converters.save_keras_model(mobilenet, save_path)
	print("[INFO] saved tf.js mobilenet model to disk..")