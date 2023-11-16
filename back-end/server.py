from typing import List, Annotated
from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn, os
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd 

from new_utils import renew_model, renew_make_gradcam
import shutil, zipfile, uuid

class textField(BaseModel) :
  text: str

user_images_folder = f"images" # = f"user_images"
model_folder = f"model" # tf_keras_vgg16_mura_model.h5
save_heatmap = f"heatmap"

# Arbitrary location for csv. File name involved.
csv_location = f"test.csv"

# Arbitrary White (Blank) image
white_image_loc = f"white.png"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.mount("/heatmap", StaticFiles(directory="heatmap"), name="heatmap")

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

'''
Find the result images and return 4 image urls.
'''
def select_images(csv_location, white_image_loc,  class_id : int = 0 , column_id : int =1) -> list:
    dataframe = pd.read_csv(csv_location)
    max_column_id = max(dataframe.loc[dataframe['prediction'] == class_id, 'column_id'].tolist())
    
    # 혹 coulmn_id 가 실제 column의 개수보다 많이 들어오면, 메세지를 출력한 다음, 마지막으로 값으로 수정함. 
    if column_id > max_column_id : 
        print("column id is bigger than max column_id")
        column_id = max_column_id
    selected_rows= dataframe[(dataframe['prediction'] == class_id) & (dataframe['column_id'] == column_id)]

    heatmap_address = selected_rows['heatmap_path'].tolist() 
    while len(heatmap_address) < 4 : 
        heatmap_address.append(white_image_loc)
    
    return heatmap_address

@app.post("/upload-model")
async def upload_model(zipFile: UploadFile):
    # return {"message": "NOT IMPLEMENTED; upload dummy zip file."}
    
    if zipFile.filename.endswith(".zip"):
        # Create the model folder if it doesn't exist
        if os.path.exists(model_folder):
            for file_path in os.listdir(model_folder):
                full_path = os.path.join(model_folder, file_path)
                if os.path.isfile(full_path):
                    os.unlink(full_path)
        else:
            os.makedirs(model_folder)

        # Generate a unique filename for the uploaded ZIP file
        unique_filename = str(uuid.uuid4()) + ".zip"
        model_path = os.path.join(model_folder, unique_filename)

        # Save the uploaded ZIP file to the model folder
        with open(model_path, "wb") as model_file:
            model_file.write(await zipFile.read())

        # Unzip the uploaded file (you'll need to have a library like zipfile installed)
        extracted = False
        with zipfile.ZipFile(model_path, "r") as zip_ref:
            # zip_ref.extractall(model_folder)
            for file in zip_ref.namelist():
                if file.endswith('.h5'):
                    # Extract file name and create a direct path under model_folder
                    file_name = os.path.basename(file)
                    extract_path = os.path.join(model_folder, file_name)
                    
                    # Extract the file to the direct path
                    with open(extract_path, "wb") as f:
                        f.write(zip_ref.read(file))
                    extracted = True
                    continue
                # if file.endswith('.h5'):
                #     # Extract only .h5 files
                #     zip_ref.extract(file, model_folder)
        
        os.unlink(model_path)
        if extracted:
            return {"message": "Model (.h5) uploaded and stored in model_folder folder."}
        else:
            return {"error": "No .h5 file found in the uploaded zip."}
    else:
        return {"error": "Invalid file format. Please upload a .zip file."}

@app.post("/run-gradcam")
async def run_gradcam():
    model_location = renew_model(model_folder) 

    # 1) renew save_heatmap folder 
    # 2) make gradcam & save heatmap in save_heatmap folder
    # 3) save csv with infomation at 'csv_location' 
    renew_make_gradcam(model_location, user_images_folder, save_heatmap, csv_location)

    # Initialize global column/ class id.
    global global_column_id 
    global_column_id = 1
    
    global global_class_id
    global_class_id = 0 

    result = select_images(csv_location, white_image_loc)
    default_maximum_value = [3, 3, 3]
    
    result = [img[8:] for img in result]
    print(result)
    return {'image_paths': result, 'max_value': default_maximum_value}

@app.post("/next-button")
async def next_button():
    global_column_id += 1 
    result = select_images(csv_location, white_image_loc, global_class_id, global_column_id)
    return {'image_paths': result}

@app.post("/prev-button")
async def prev_button():
    global_column_id -= 1 
    result = select_images(csv_location, white_image_loc, global_class_id, global_column_id)
    return {'image_paths': result}

@app.post("/class-dropdown")
async def prev_button(class_num: int):
    global global_class_num
    global_class_num = class_num
    
    result = select_images(csv_location, white_image_loc, global_class_id, global_column_id)
    return {'image_paths': result}

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port = 8000)