# web-hosting-gravisu
Both the server and the web code for deploying (web-hosting) the gravisu (GradCam Visualization).


**How to host the server (server.py)**
Virtual environment is preferred.

$ python3 -m venv gradcam++

$ source gradcam++/bin/activate


hosting server.py
* Change directory to where the python script ({python}.py) exists.
* Make sure to modify the url in the javascript with your own ip address.
* Use uvicorn to host the server ({python}:app).

$ (gradcam++) cd back-end/tf.keras-gradcamplusplus

$ (gradcam++) pip install -r requirement.txt

$ (gradcam++) uvicorn server:app --host 0.0.0.0 --port 8000




=====================================================
First - Change python version as 3.8 for lavis model 

$ python -m venv new_grad

$ new_grad\Scripts\activate 

$ (new_grad) cd back-end/tf.keras-gradcamplusplus

$ (new_grad) cd back-end/tf.keras-gradcamplusplus

