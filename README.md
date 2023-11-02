# web-hosting-gravisu
Both the server and the web code for deploying (web-hosting) the gravisu (GradCam Visualization).

**How to host the server (server.py)**
Virtual environment is preferred.
$ python3 -m venv gradcam++
$ source gradcam++/bin/activate

hosting server.py
* Change directory to where the python script ({python}.py) exists.
* Use uvicorn to host the server ({python}:app).
$ (gradcam++) pip install FastAPI uvicorn
$ (gradcam++) cd /backend
$ (gradcam++) uvicorn server:app --host 0.0.0.0 --port 8000
