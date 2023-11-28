# README

---

**GRAVISU**

---

🔗 [GRAVISU website](http://wlqmfl.com/project/gravisu/index.html)

Building a user-friendly web which provides explanation of CNN based machine learning models (GradCAM).

---

**Code**

---

- Front End

index.html

: Outlines a web page for GRAVISU, a tool designed for image dataset uploading, model training, and image classification result visualization. It features a three-step user interface: the first step for uploading an image dataset, the second for uploading training model information, and the third for displaying image classification results and statistics.

script.js

: Enables uploading and processing image datasets and model files on a web application via FastAPI. It includes functionality to enable upload buttons when files are selected, handles the uploading of images and a model file to the server, and manages the display of image classification results and navigation through them using next and previous buttons.

- Back End

server.py

: This Python code using FastAPI sets up a web server to handle various POST requests for uploading images and a model file, running GradCAM++ for image classification, and navigating through classification results. It includes endpoints to upload images and a machine learning model (in .zip format), perform image classification and image captioning using GradCAM++, and display the results along with the visualization of histograms. The server also facilitates navigation through the classification results with next, previous, and class selection buttons, and handles CORS for cross-origin requests.

new_utils.py

: This Python code utilizes a trained machine learning model to perform Grad-CAM++ visualization on a set of images, which helps in understanding the regions of the image most relevant to the model's predictions. It also includes functionality to preprocess images, generate heatmaps overlaying the original images, and create histograms based on image captions, illustrating the frequency of specific words.

---

**Quick Start**

---

Running GRAVISU composes of 3 steps.

1. Upload test images

Upload the [test images](https://drive.google.com/file/d/1cfk0XSWgBIUw08bqVwThoRWK1lJhYLAq/view?usp=sharing) by clicking the *Browse* button in *1. Upload Your Image Dataset*. Then press *Upload* button. Wait until the message <span style="color:red;">*You have uploaded N images.*</span> appears.

❗️ Note that the images **must** be one of .jpg, .jpeg, .png, or .gif format (e.g. Scroll the images in the test_images folder to upload.)

2. Upload your model

Upload the [test model](https://drive.google.com/file/d/1fYH0bVg8zi30dhljJoquQ21bBacHrnBZ/view?usp=sharing) by clicking the *Browse* button in *2. Input Your Training Model Information*. While the server is saving the model, the message <span style="color:red;">*Uploading model…*</span> will appear. Wait until the message <span style="color:red;">*Model upload complete.*</span> appears.

❗️ Note that the model **must** be sent by .zip format. (e.g. test_model.zip)

❗️ Note that the model **must** be a CNN based model.

3. Run GRAVISU 

Click Run *Gra-Visu* button to run! It’ll take some time.

- When the image appears, move onto the next/ previous image by clicking the left/ right button. Also, you can view the images by its class by clicking the dropdown *Images of N th class*.
- You can also view the histogram of keyword statistics, based on the image captioning.

---

**Hosting the Server**

---

We use [Uvicorn](https://www.uvicorn.org) and [FastAPI](https://fastapi.tiangolo.com) for server hosting. Also, you should be using python version 3.8.10 by using pyenv:

Windows

1. Install pyenv
2. Open powershell as Administrator
3. Change policy of powershell & change python version $ Set-ExecutionPolicy RemoteSigned -Scope Process
    
    `$ pyenv install 3.8.10`
    
    `$ pyenv global 3.8.10 $ Set-ExecutionPolicy Restricted -Scope Process`
    
4. Then make Virtual environment

Mac OS

1. Refer to: [https://leesh90.github.io/environment/2021/04/03/python-install/](https://leesh90.github.io/environment/2021/04/03/python-install/)

Then, run server.py:

`$ cd back-end`

`$ pip install -r tf.keras-gradcamplusplus/requirement.txt`

`$ uvicorn server:app --host your.server.IP.address --port 8000` or  `$ python3 server.py`

❗️ Note that the currently running web application is accessible only to those using [KAIST](https://www.kaist.ac.kr/kr/) Wifi/Ethernet.

---

**Reference**

---

[Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization](https://arxiv.org/abs/1610.02391)

[Grad-CAM++: Improved Visual Explanations for Deep Convolutional Networks](https://arxiv.org/abs/1710.11063)

[LAVIS - A Library for Language-Vision Intelligence](https://github.com/salesforce/LAVIS)