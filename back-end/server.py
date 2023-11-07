from typing import List, Annotated
from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn, os

class textField(BaseModel) :
  text: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/textreturn")
def text_return(data: dict):
    if "text" in data:
        input_text = data["text"]
        return {'text': input_text}
    else:
        return {'error': 'Invalid request payload'}

user_images_folder = "user_images"

@app.post("/upload-images")
async def upload_images(files: List[UploadFile]):
    # Ensure the user_images folder exists, and clear its contents if it exists
    if os.path.exists(user_images_folder):
        for filename in os.listdir(user_images_folder):
            file_path = os.path.join(user_images_folder, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    else:
        os.makedirs(user_images_folder)

    # Save the uploaded image files to the user_images folder
    for file in files:
        file_path = os.path.join(user_images_folder, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

    # Return a response to the client (e.g., success message)
    return {"message": "Images uploaded and stored in user_images folder."}

global_class_num = 0
global_index_num = 0

'''
Find the result images and return 4 image urls.
'''
def select_images(class_num: int = 0, index_num: int = 0) -> list:
    return ['image_url1', 'image_url2', 'image_url3', 'image_url4']

@app.post("/upload-model")
async def upload_model(files: List[UploadFile]):
    # TODO: save the uploaded model in the model folder.
    
    result = select_images()
    # TODO: send the selected images to the Web.
    pass

@app.post("/next-button")
async def next_button():
    pass

@app.post("/prev-button")
async def prev_button():
    pass

@app.post("/class-dropdown")
async def prev_button(class_num: int):
    global global_class_num
    global_class_num = class_num
    pass

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port = 8000)