from typing import List
from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn, os, time
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd 

from new_utils import renew_model, renew_make_gradcam, visual_histogram
import shutil, zipfile, uuid

class textField(BaseModel) :
  text: str

user_images_folder = f"user_images"
model_folder = f"model"
save_heatmap = f"heatmap"

# Arbitrary location for csv. File name involved.
csv_location = f"test.csv"

# Arbitrary White (Blank) image
white_image_loc = f"heatmap/white.png"
histogram_save_location = f"heatmap/histogram"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

global_column_id = 1;
global_class_id = 1;

app.mount("/heatmap", StaticFiles(directory="heatmap"), name="heatmap")
# app.mount("/white", StaticFiles(directory="white"), name="white")

@app.get("/hello")
def hello():
    return {'message': 'HELLO CS492 TAs!'}

@app.post("/test")
async def test():
    # Initialize global column/ class id.
    global global_column_id 
    global_column_id = 1
    
    global global_class_id
    global_class_id = 1
    
    result = ['dog1.png', 'dog2.png', 'dog3.png', 'dog4.png']
    max_column_id = [6, 6, 8]
    histogram_path = 'heatmap/histogram/histogram_1.png'
    return {'image_paths': result, 'max_value': max_column_id, 'histogram': histogram_path[8:]}

@app.post("/upload-images")
async def upload_images(files: List[UploadFile]):
    # Ensure the user_images folder exists, and clear its contents if it exists
    if os.path.exists(user_images_folder):
        for filename in os.listdir(user_images_folder):
            file_path = os.path.join(user_images_folder, filename)
            if os.path.isdir(file_path):
                continue
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
def select_images(csv_location, white_image_loc,  class_id : int = 1 , column_id : int =1) -> list:
    dataframe = pd.read_csv(csv_location)
    selected_rows= dataframe[(dataframe['prediction'] == class_id) & (dataframe['column_id'] == column_id)]

    heatmap_address = selected_rows['heatmap_path'].tolist() 
    while len(heatmap_address) < 4 : 
        heatmap_address.append(white_image_loc)
    
    return heatmap_address

def load_histogram(class_id, histogram_save_location, save_heatmap) : 
    histogram_path = os.path.join(histogram_save_location, f'histogram_{class_id}.png').replace('\\', '/')

    # Check if image exists.
    if os.path.exists(histogram_path):
        # Return the image path.
        return histogram_path
    else:
        return os.path.join(save_heatmap, 'white.png').replace('\\', '/')


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
    start_time = time.time()
    model_location = renew_model(model_folder) 

    # 1) renew save_heatmap folder 
    # 2) make gradcam & save heatmap in save_heatmap folder
    # 3) save csv with infomation at 'csv_location' 
    num_class = renew_make_gradcam(model_location, user_images_folder, save_heatmap, csv_location)
    visual_histogram(num_class, csv_location, save_folder = histogram_save_location)
    end_time = time.time()
    duration = end_time - start_time
    duration_minutes = int(duration // 60)
    duration_seconds = int(duration % 60)
    duration_str = f"{duration_minutes} m {duration_seconds} s"
    
    df = pd.read_csv(csv_location)

    max_column_id = [] 
    for c_id in range(num_class) : 
        c_column_id = df.loc[df['prediction'] == c_id + 1, 'column_id'].tolist()
        if len(c_column_id) == 0 : 
            class_max_column_id = 0 
        else : 
            class_max_column_id = max(c_column_id)
        
        max_column_id.append(class_max_column_id)
        
    # Initialize global column/ class id.
    global global_column_id 
    global_column_id = 1
    
    global global_class_id
    global_class_id = 1

    result = select_images(csv_location, white_image_loc)
    histogram_path = load_histogram(class_id = 1, histogram_save_location= histogram_save_location, save_heatmap= save_heatmap)
    
    result = [img[8:] for img in result]
    
    print('RUN')
    print("class:", global_class_id, "column:", global_column_id)
    print(result, histogram_path[8:], max_column_id)
    return {'image_paths': result, 'max_value': max_column_id, 'histogram': histogram_path[8:], 'duration': duration_str}

@app.post("/next-button")
async def next_button():
    global global_column_id
    global_column_id += 1
    result = select_images(csv_location, white_image_loc, global_class_id, global_column_id)
    result = [img[8:] for img in result]
    
    print('NEXT')
    print("class:", global_class_id, "column:", global_column_id)
    print(result)
    return {'image_paths': result}

@app.post("/prev-button")
async def prev_button():
    global global_column_id
    global_column_id -= 1
    result = select_images(csv_location, white_image_loc, global_class_id, global_column_id)
    result = [img[8:] for img in result]
    
    print('PREV')
    print("class:", global_class_id, "column:", global_column_id)
    print(result)
    return {'image_paths': result}

@app.post("/class-dropdown")
async def class_dropdown(class_num: int = Form(...)):
    global global_column_id
    global global_class_id
    global_class_id = class_num
    global_column_id = 1
    
    result = select_images(csv_location, white_image_loc, global_class_id, global_column_id)
    histogram_path = load_histogram(class_id = class_num, histogram_save_location= histogram_save_location, save_heatmap= save_heatmap)
    ######### test
    # result = ['dog5.png', 'dog6.png', 'dog7.png', 'dog4.png']
    # histogram_path = 'heatmap/histogram/histogram_3.png'
    #########
    result = [img[8:] for img in result]
    
    print('DROPDOWN')
    print("class:", global_class_id, "column:", global_column_id)
    print(result, histogram_path[8:])
    return {'image_paths': result, 'histogram': histogram_path[8:]}

if __name__=='__main__':
    uvicorn.run(app, host='110.76.86.172', port = 8000)
