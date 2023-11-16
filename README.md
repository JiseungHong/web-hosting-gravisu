# web-hosting-gravisu
Both the server and the web code for deploying (web-hosting) the gravisu (GradCam Visualization).


===================
Need to change python version as 3.8 for Image captioining(lavis) model 

When Window
1. Install pyenv 

2. Open powershell as Administrator

3. Change policy of powershell & change python version 
$ Set-ExecutionPolicy RemoteSigned -Scope Process
$ pyenv install 3.8.10   
$ pyenv global 3.8.10
$ Set-ExecutionPolicy Restricted -Scope Process 

4. Then make Virtual environment

=============================


**How to host the server (server.py)**
Virtual environment is preferred.

$ python -m venv gradcam++

$ source gradcam++/bin/activate
$ (window) gradcam++\Scripts\activate

hosting server.py
* Change directory to where the python script ({python}.py) exists.
* Make sure to modify the url in the javascript with your own ip address.
* Use uvicorn to host the server ({python}:app).

$ (gradcam++) cd back-end/tf.keras-gradcamplusplus

$ (gradcam++) pip install -r requirement.txt

$ (gradcam++) uvicorn server:app --host 0.0.0.0 --port 8000




