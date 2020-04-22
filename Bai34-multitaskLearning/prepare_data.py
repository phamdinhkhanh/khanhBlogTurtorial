import numpy as np
from sklearn.model_selections import train_test_split
import glob2
import pandas as pd


class Dataset():
	# Hàm lấy toàn bộ ảnh
	def _list_images(root_dir, exts = ['.jpg', '.jpeg', '.png']):
	  list_images = glob2.glob('Bai34-multitaskLearning'+'/**')
	  image_links = []
	  for image_link in list_images:
	    for ext in exts:
	      if ext in image_link[-5:]:
	        image_links.append(image_link)
	  return image_links

	@staticmethod
	def _data_source(root_dir):
		# Lấy dữ liệu ảnh lưu vào pandas dataframe: label là nhãn, source là link tới ảnh
		imagePaths = sorted(_list_images(root_dir=root_dir))
		labels = [path.split("/")[2] for path in imagePaths]
		data = pd.DataFrame({'label': labels, 'source': imagePaths})
		return data