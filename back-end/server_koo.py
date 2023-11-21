from typing import List, Annotated
from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd 

from new_utils import renew_model, renew_make_gradcam, visual_histogram

# load_class 함수 -> select_images 함수로 변경

import uvicorn, os

class textField(BaseModel) :
  text: str


# 임의의 Image/ model / heatmap foler
user_images_folder = f"C:/Users/user/Desktop/assignment/image"
model_folder = f"C:/Users/user/Desktop/assignment/model" # tf_keras_vgg16_mura_model.h5
save_heatmap = f"./heatmap"

# 임의로 저장한 csv_location. 파일 이름까지 포함되어야함. 
csv_location = f"./test.csv"
histogram_save_location = f"./heatmap/histogram"

# 임의의 white image 
white_image_loc = f"./heatmap/white.png"


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


'''
Find the result images and return 4 image urls.
'''

#def select_images(class_num: int = 0, index_num: int = 1) -> list:
#    return ['image_url1', 'image_url2', 'image_url3', 'image_url4']

# csv_location, white_image_loc 의 값은 server.py 상단에서 설정한 값입니다. 
def select_images(csv_location, white_image_loc,  class_id : int = 1 , column_id : int =1) -> list:
    dataframe = pd.read_csv(csv_location)
    max_column_id = max(dataframe.loc[dataframe['prediction'] == class_id, 'column_id'].tolist())
    
    # UI 단위에서 Column id 조정하기  
    #if column_id > max_column_id : 
    #    print("column id is bigger than max column_id")
    #    column_id = max_column_id
    selected_rows= dataframe[(dataframe['prediction'] == class_id) & (dataframe['column_id'] == column_id)]

    heatmap_address = selected_rows['heatmap_path'].tolist() 
    while len(heatmap_address) < 4 : 
        heatmap_address.append(white_image_loc)
    
    return heatmap_address

# 특정 Class_id 에 해당하는 histogram 이미지의 주소 값을 불러옵니다. 
# 만약 histogram 이미지가 존재하지 않는다면, 'No-Data' 이미지를 대신 불러옵니다. 
def load_histogram(class_id, histogram_save_location, save_heatmap) : 
    histogram_path = os.path.join(histogram_save_location, f'histogram_{class_id}.png').replace('\\', '/')

    # 생성된 경로에 이미지 파일이 존재하는지 확인
    if os.path.exists(histogram_path):
        # 이미지 파일이 존재하면 해당 경로를 반환
        return histogram_path
    
    else:
        return os.path.join(save_heatmap, 'No_Data.png').replace('\\', '/')





@app.post("/upload-model")
async def upload_model(files: List[UploadFile]): # input 불필요 
    # TODO: save the uploaded model in the model folder.
    
    # model_folder 에 저장된 model 파일 이름을 읽어, model_location 값 불러오기 
    model_location = renew_model(model_folder) 

    # 4개의 Input 모두 server.py 상단에서 수정할 수 있음. 
    # 1) renew save_heatmap folder 
    # 2) make gradcam & save heatmap in save_heatmap forlder
    # 3) save csv with infomation at 'csv_location' 
    num_class = renew_make_gradcam(model_location, user_images_folder, save_heatmap, csv_location)
    
    # 모든 Class에 대해서 Image captioining 결과를 histogram으로 만들어 save_folder 위치에 저장하기 
    visual_histogram(num_class, csv_location, save_folder = histogram_save_location)

    df = pd.read_csv(csv_location)
    # max_column_id 반영하기

    max_column_id = [] 
    for c_id in range(num_class) : 
        c_column_id = df.loc[df['prediction'] == c_id + 1, 'column_id'].tolist()
        if len(c_column_id) == 0 : 
            class_max_column_id = 0 
        else : 
            class_max_column_id = max(c_column_id)
        
        max_column_id.append(class_max_column_id)

    # 최초 column_id / class_id 정의. 여기서 정의해주는 것이 깔끔할 듯.  
    global global_column_id 
    global_column_id = 1

    global global_class_id
    global_class_id = 1 

    # csv_location 에서 데이터를 불러와서, 조건에 맞는 4개의 heatmap 이미지 주소값을 불러옴 

    result = select_images(csv_location, white_image_loc)
    histogram_path = load_histogram(class_id = 1, histogram_save_location= histogram_save_location, save_heatmap= save_heatmap)
    
    # TODO: send the selected images to the Web.
    return result, max_column_id, histogram_path

# 아래는 global 변수 값만을 변경하여, 4개의 image 씩 보내도록 설정
# image captioining histogram은 Class_id 가 변경되었을 때에만 바뀌도록 설정해야함. 
@app.post("/next-button")
async def next_button():
    global_column_id += 1 
    return select_images(csv_location, white_image_loc, global_class_id, global_column_id)

@app.post("/prev-button")
async def prev_button():
    global_column_id -= 1 
    return select_images(csv_location, white_image_loc, global_class_id, global_column_id)


# Histogram 추가 완료.  
@app.post("/class-dropdown")
async def prev_button(class_num: int):
    global_class_id = class_num
    # class_dropdown 시 column_id 1로 세팅하기 
    global_column_id = 1

    heatmap_path = select_images(csv_location, white_image_loc, global_class_id, global_column_id)
    histogram_path = load_histogram(global_class_id, histogram_save_location, save_heatmap)
    return heatmap_path, histogram_path 
    

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port = 8000)