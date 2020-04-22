# Fashion Image

![]('demo.jpg')

# Huấn luyện mô hình
`python train.py --dataset dataset --model fashion_multitask_learning.h5 --labelbin mlb.pkl`

# Dự báo một ảnh trên mạng
`python predict.py --model fashion_multitask_learning.h5 --labelbin mlb.pickle --image 'https://keimag.com.my/image/cache/cache/4001-5000/4432/main/3163-DSC_0557-2c-0-1-0-1-1-800x1200.jpg'`

![]('demo2.png')

# Dự báo một ảnh trên folder

`python predict.py --model fashion_multitask_learning.h5 --labelbin mlb.pkl --image examples/example_01.jpg`

![]('demo3.png')
