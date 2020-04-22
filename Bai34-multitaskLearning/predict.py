# USAGE
# python predict.py --model fashion_multitask_learning.h5 --labelbin mlb.pkl --image examples/example_01.jpg

# import the necessary packages
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import argparse
import pickle
import cv2
import os
import requests
import matplotlib.pyplot as plt

IMAGE_DIMS = (96, 96, 2)
# Khởi tạo ArgumentParser
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
  help="path to trained model model")
ap.add_argument("-l", "--labelbin", required=True,
  help="path to label binarizer")
ap.add_argument("-i", "--image", required=True,
  help="url link to input image")
args = vars(ap.parse_args())

# Load model và multilabel
print("[INFO] loading network...")
model = load_model(args["model"])
mlb = pickle.loads(open(args["labelbin"], "rb").read())

# read image
def _downloadImage(url):
  img = cv2.imread(url)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  return img

# dự báo image
def _predict_image(image, model, mlb):
  # Lấy kích thước 3 kênh của image
  (w, h, c) = image.shape
  # Nếu resize width = 400 thì height resize sẽ là
  height_rz = int(h*400/w)
  # Resize lại ảnh để hiện thị 
  output = cv2.resize(image, (height_rz, 400))
  # Resize lại ảnh để dự báo
  image = cv2.resize(image, IMAGE_DIMS[:2])/255.0
  # Dự báo xác suất của ảnh
  prob = model.predict(np.expand_dims(image, axis=0))[0]
  # Trích ra 2 xác suất cao nhất
  argmax = np.argsort(prob)[::-1][:2]
  # Show classes và probability ra ảnh hiển thị
  for (i, j) in enumerate(argmax):
    # popup nhãn và xác suất dự báo lên ảnh hiển thị
    label = "{}: {:.2f}%".format(mlb.classes_[j], prob[j] * 100)
    cv2.putText(output, label, (5, (i * 20) + 15), 
      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 0, 0), 2)
  # show the output image
  output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
  # plt.imshow(output)
  # cv2.imwrite('predict.jpg', output)
  cv2.imshow("Output", output)
  cv2.waitKey(0)

image = _downloadImage(args['image'])
_predict_image(image, model, mlb)
