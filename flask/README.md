# Flask app

Do project yêu cầu sử dụng tensorflow bản 2.0.0. Cài đặt package này dễ bị conflict với các package còn lại trên python.


* Cách tốt nhất là khởi tạo một môi trường ảo. Trong folder sau khi clone package về các bạn gõ lệnh.

`python3 -m venv --system-site-packages ./venv`

Khi đó trong folder xuất hiện một folder của `virtual environment` là `.venv`. 

* Activate virtual enviroment bằng câu lệnh:

`./venv/Scripts/activate`


Tiếp theo:

* Cài đặt các packages cần thiết trong `virtual enviroment` thông qua file `requirements.txt`.

`python install -r requirements.txt --user`

* Start app bằng câu lệnh:

`python server.py`
