# USAGE
# python train.py --dataset dataset --model fashion_multitask_learning.h5 --labelbin mlb.pkl

from net import KhanhBlogNet
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import MultiLabelBinarizer

# Thiết lập ArgumentParser
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
  help="path to input dataset")
ap.add_argument("-m", "--model", required=True, default="model_fashion_multitask_learning.h5",
  help="path to output model")
ap.add_argument("-l", "--labelbin", required=True,
  help="path to output label binarizer")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
  help="path to output accuracy/loss plot")
args = vars(ap.parse_args())

# Thiết lập tham số
INPUT_SHAPE = (96, 96, 3)
N_CLASSES = 6
DATASET_DIR = 'dataset'
BATCH_SIZE = 32

# Khởi tạo dữ liệu
images = []
labels = []

# Dataset
data = Dataset._data_source(DATASET_DIR)
data_sources = Dataset.data.groupby('label').source.apply(lambda x: list(x))
for i, sources in enumerate(data_sources):
  np.random.shuffle(list(sources))
  label = data_sources.index[i]
  sources = data_sources[label]
  for imagePath in sources:
    # Đọc dữ liệu ảnh
    image = cv2.imread(imagePath)
    image = cv2.resize(image, INPUT_SHAPE[:2])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.array(image)
    images.append(image)
    # Gán dữ liệu label
    fashion, color = label.split('_')
    labels.append([fashion, color])
  

# MultiLabel Encoding cho nhãn của ảnh
mlb = MultiLabelBinarizer()
# One-hot encoding cho fashion
y = mlb.fit_transform(labels)
# Lưu the multi-label binarizer
print("[INFO] serializing label binarizer...")
f = open(args["labelbin"], "wb")
f.write(pickle.dumps(mlb))
f.close()

print('[INFO] classes of labels: ', mlb.classes_)
# Phân chia train/validation theo tỷ lệ 80/20
(X_train, X_val, y_train, y_val) = train_test_split(images, y, 
                                                    test_size=0.2, random_state=123)
print('[INFO] X_train.shape: {}, y_train.shape: {}'.format(X_train.shape, y_train.shape))
print('[INFO] X_val.shape: {}, y_val.shape: {}'.format(X_val.shape, y_val.shape))


# Stack list numpy array của ảnh thành một array
images = np.stack(images)
images = images/255.0

# Khởi tạo data augumentation
image_aug = ImageDataGenerator(rotation_range=25, 
                         width_shift_range=0.1, height_shift_range=0.1, 
                         shear_range=0.2, zoom_range=0.2,
                         horizontal_flip=True, fill_mode="nearest")


print('[INFO] training model...')
# Khởi tạo mô hình
model = KhanhBlogNet.build_model(inputShape=INPUT_SHAPE, classes=N_CLASSES,  finAct='sigmoid')
model.load_weights(args['model'])

# Khởi tạo optimizer
LR_RATE = 0.01
EPOCHS = 50
opt = Adam(lr=LR_RATE, decay=LR_RATE / EPOCHS)

# Huấn luyện mô hình
history = model.fit(
  image_aug.flow(X_train, y_train, batch_size=BATCH_SIZE),
  validation_data=(X_val, y_val),
  steps_per_epoch=len(X_train) // BATCH_SIZE,
  epochs=EPOCHS, verbose=1)

# Lưu mô hình
print("[INFO] serializing network...")
model.save(args["model"])


# lưu multi-label binarizer
print("[INFO] serializing label binarizer...")
f = open(args["labelbin"], "wb")
f.write(pickle.dumps(mlb))
f.close()

# lưu biểu đồ accuracy và loss quá trình huấn luyện
# plt.style.use("ggplot")
plt.figure()
N = EPOCHS
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="upper left")
plt.savefig(args["plot"])