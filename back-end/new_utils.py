import requests
import os
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import get_file
from tensorflow.keras import Model

from tensorflow import keras 
import shutil
import numpy as np
import torch
import tensorflow as tf
import pandas as pd 
from collections import Counter
import matplotlib.pyplot as plt
from lavis.models import load_model_and_preprocess


def find_last_conv_layer(model) : 
    layers = model.layers
    last_conv_layer = None
    for layer in reversed(layers):
        if 'conv' in layer.name.lower():  # 합성곱 레이어의 이름에 "conv2d"가 포함되어 있는 경우
            last_conv_layer = layer
            break
    return last_conv_layer.name 



def preprocess_image(img_path, target_size=(224, 224)):
    img = image.load_img(img_path, target_size=target_size)
    img = image.img_to_array(img)
    img /= 255

    return img

def show_imgwithheat(img_path, heatmap,alpha=0.4):
    """Show the image with heatmap and save the result.

    Args:
        img_path: string, path to the original image.
        heatmap: image array, get it by calling grad_cam().
        save_path: string, path to save the result image.
        alpha: float, transparency of heatmap.
    """
    img = cv2.imread(img_path)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = (heatmap * 255).astype("uint8")
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    superimposed_img = heatmap * alpha + img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype("uint8")
    superimposed_img = cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB)
    return superimposed_img

    # Save the result image
    

def new_grad_cam_plus(model, img, label_name=None, category_id=None):
    img_tensor = np.expand_dims(img, axis=0)

    layer_name = find_last_conv_layer(model)

    conv_layer = model.get_layer(layer_name)
    heatmap_model = Model([model.inputs], [conv_layer.output, model.output])

    with tf.GradientTape() as gtape1:
        with tf.GradientTape() as gtape2:
            with tf.GradientTape() as gtape3:
                conv_output, predictions = heatmap_model(img_tensor)
                if category_id is None:
                    category_id = np.argmax(predictions[0])
                if label_name is not None:
                    print(label_name[category_id])
                output = predictions[:, category_id]
                conv_first_grad = gtape3.gradient(output, conv_output)
            conv_second_grad = gtape2.gradient(conv_first_grad, conv_output)
        conv_third_grad = gtape1.gradient(conv_second_grad, conv_output)

    global_sum = np.sum(conv_output, axis=(0, 1, 2))

    alpha_num = conv_second_grad[0]
    alpha_denom = conv_second_grad[0]*2.0 + conv_third_grad[0]*global_sum
    alpha_denom = np.where(alpha_denom != 0.0, alpha_denom, 1e-10)

    alphas = alpha_num/alpha_denom
    alpha_normalization_constant = np.sum(alphas, axis=(0,1))
    alphas /= alpha_normalization_constant

    weights = np.maximum(conv_first_grad[0], 0.0)

    deep_linearization_weights = np.sum(weights*alphas, axis=(0,1))
    grad_cam_map = np.sum(deep_linearization_weights*conv_output[0], axis=2)

    heatmap = np.maximum(grad_cam_map, 0)
    max_heat = np.max(heatmap)
    if max_heat == 0:
        max_heat = 1e-10
    heatmap /= max_heat

    return category_id, heatmap


# when model update, 1) renew model_location folder, 2) return model_location 
def renew_model(model_folder) :
    #if os.path.exists(model_folder):
    #    shutil.rmtree(model_folder) 
    #os.makedirs(model_folder)

    models = [] 
    for model_name in os.listdir(model_folder):
        models.append(model_name)
    
    assert len(models), f"There's no model in {model_folder}" 


    model_name = models[0]
    model_location = os.path.join(model_folder, model_name).replace('\\', '/')

    return model_location 


# Input : model_location / user_imagese_folder / save_heatmap 
# output : dataframe
def renew_make_gradcam(model_location, user_images_folder, save_heatmap, csv_location) : 
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    loaded_model = keras.models.load_model(model_location)
    #loaded_model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    num_class = loaded_model.layers[-1].output_shape[1]

    images = [] 
    if os.path.exists(save_heatmap):
        shutil.rmtree(save_heatmap)

    conv_folder = os.path.join(user_images_folder, "converted_").replace('\\', '/')
    if os.path.exists(conv_folder):
        shutil.rmtree(conv_folder)
   
    allowed_extensions = ['.png', '.jpg', '.jpeg']
    for image_name in os.listdir(user_images_folder):
        _, extension = os.path.splitext(image_name)
        if extension.lower() in allowed_extensions:
            images.append(image_name)

    os.makedirs(conv_folder)
    
    assert len(images), f"There's no data in {user_images_folder}"

    # heatmap 폴더가 이미 존재하면 삭제


    os.makedirs(save_heatmap)

    data = [] 
    for id, img_name in enumerate(images) : 
        img_path = os.path.join(user_images_folder, img_name).replace('\\', '/')
        #img_path = img_path.replace('\\', '/')
        
        

        img = preprocess_image(img_path)
        category_id, heatmap = new_grad_cam_plus(loaded_model, img)
        
        imposed_img = show_imgwithheat(img_path, heatmap)
        save_path = os.path.join(save_heatmap, img_name).replace('\\', '/')
        #save_path = img_path.replace('\\', '/')
        # cv2 는 한글 주소 못 읽어냄.. ㅂㄷㅂㄷ 
        cv2.imwrite(save_path, imposed_img)

        # Grad cam 결과로 masking 이미지 만들기 
        target_size = (400, 300)
        conv_img = resize_and_fill(save_path, target_size)
        conv_img_path = os.path.join(conv_folder, img_name).replace('\\', '/')

        
        cv2.imwrite(conv_img_path, conv_img)

        # image captioning 결과
        model, vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="large_coco", is_eval=True, device=device)
        raw_image = Image.open(img_path).convert("RGB")
        image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
        image_caption_result =model.generate({"image": image})
        # category_id 1부터 시작하도록 수정 
        data.append([id+1, img_name, category_id+1, save_path, conv_img_path, image_caption_result[0], 1]) 
       
    data_df = pd.DataFrame(data, columns=['id', 'img_name', 'prediction', 'heatmap_path', 'conv_heatmap_path',  'image_caption', 'column_id'])

    # make column_num 
    for class_ in range(num_class) : 
        selected_rows= data_df[data_df['prediction']==class_]
        num_data = len(selected_rows)
        num_iterations = num_data // 4

        # 4개씩 묶어서 column_id 값을 부여
        column_id = 1 
        for i in range(num_iterations):
            data_df.loc[selected_rows.index[i * 4: (i + 1) * 4], 'column_id'] = column_id
            column_id += 1
        
        if num_data % 4 > 0:
            data_df.loc[selected_rows.index[num_iterations * 4:], 'column_id'] = column_id
    
    data_df.to_csv(csv_location, index=False)



def resize_and_fill(image_path, target_size):
    # 이미지 로드
    original_image = cv2.imread(image_path)

    # 원본 이미지의 크기
    original_height, original_width = original_image.shape[:2]

    # 타겟 크기 계산
    target_width, target_height = target_size
    aspect_ratio = original_width / original_height

    if target_width / target_height > aspect_ratio:
        # 이미지가 타겟 크기의 가로 비율보다 더 길 경우
        new_width = int(target_height * aspect_ratio)
        resized_image = cv2.resize(original_image, (new_width, target_height))
    else:
        # 이미지가 타겟 크기의 세로 비율보다 더 길 경우
        new_height = int(target_width / aspect_ratio)
        resized_image = cv2.resize(original_image, (target_width, new_height))

    # 검은색으로 채운 이미지 생성
    filled_image = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    offset_x = (target_width - resized_image.shape[1]) // 2
    offset_y = (target_height - resized_image.shape[0]) // 2
    filled_image[offset_y:offset_y + resized_image.shape[0], offset_x:offset_x + resized_image.shape[1]] = resized_image

    return filled_image


def visual_histogram(class_id, csv_location, save_folder=None) : 
    if save_folder is not None : 
        if os.path.exists(save_folder): shutil.rmtree(save_folder)
        os.makedirs(save_folder)
        save_path = os.path.join(save_folder, "histogram.png").replace('\\', '/')

    dataframe = pd.read_csv(csv_location)
    filtered_df = dataframe[dataframe['prediction'] == class_id]
    if len(filtered_df) == 0 : 
        print("No data in this class")
        return 

    result_image_caption = filtered_df['image_caption'].tolist()

    # 무시할 단어 목록 (예: 관사, 조사) 설정하기 
    ignore_words = ["a", "an", "the", "of", "in", "on", "with", "and", "is"]

    all_words = ' '.join(result_image_caption).split()

    # 각 단어의 빈도를 계산하며 무시할 단어는 제외합니다.
    word_frequencies = Counter(word for word in all_words if word not in ignore_words)

    # 빈도 수가 상위 10개인 값만 가져오기 

    top_words = word_frequencies.most_common(10)

    words = [word for word, freq in top_words]
    frequencies = [freq for word, freq in top_words]

    # 히스토그램 생성
    plt.figure(figsize=(12, 6))
    plt.bar(words, frequencies)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)

    if save_folder is None :
        plt.show()
    else :
        plt.savefig(save_path, bbox_inches='tight')
    
    #plt.show()