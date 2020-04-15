# from keras.preprocessing.image import img_to_array
# from keras.applications import imagenet_utils	
from PIL import Image
import numpy as np
import hyper as hp
from flask import Flask, request
import flask
# import redis
# import uuid
# import time
import json
import io
import utils
import imagenet


global model 
model = None
# Khởi tạo flask app
app = Flask(__name__)

@app.route("/")
def _hello_world():
	return "Hello world"


@app.route("/predict", methods=["POST"])
def predict():
	data = {"success": False}
	if request.files.get("image"):
		# Lấy file ảnh người dùng upload lên
		image = request.files["image"].read()
		# Convert sang dạng array image
		image = Image.open(io.BytesIO(image))
		# resize ảnh
		image_rz = utils._preprocess_image(image,
			(hp.IMAGE_WIDTH, hp.IMAGE_HEIGHT))
		# Dự báo phân phối xác suất
		dist_probs = model.predict(image_rz)
		# argmax 5
		argmax_k = np.argsort(dist_probs[0])[::-1][:5]
		# classes
		classes = [imagenet.classes[idx] for idx in list(argmax_k)]
		# probability of classes
		classes_prob = [dist_probs[0, idx] for idx in list(argmax_k)]	
		data["probability"] = dict(zip(classes, classes_prob))
		data["success"] = True
	return json.dumps(data, ensure_ascii=False, cls=utils.NumpyEncoder)

if __name__ == "__main__":
	print("App run!")
	# Load model
	model = utils._load_model()
	app.run(debug=False, host=hp.IP, threaded=False)
