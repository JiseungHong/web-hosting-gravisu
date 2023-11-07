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
import tensorflow as tf
import pandas as pd 


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


def load_class(dataframe, class_id) :
    selected_rows= dataframe[dataframe['prediction']==class_id] 
    select_n = min(4, len(selected_rows))
    random_selected_rows = selected_rows.sample(n=select_n) 

    return select_n, random_selected_rows

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
def renew_make_gradcam(model_location, user_images_folder, save_heatmap) : 
    loaded_model = keras.models.load_model(model_location)
    #loaded_model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    num_class = loaded_model.layers[-1].output_shape[1]

    images = [] 
    for image_name in os.listdir(user_images_folder):
        images.append(image_name)

    assert len(images), f"There's no data in {user_images_folder}"

    # heatmap 폴더가 이미 존재하면 삭제
    if os.path.exists(save_heatmap):
        shutil.rmtree(save_heatmap)

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
        data.append([id+1, img_name, img_path, category_id, save_path]) 
       
    data_df = pd.DataFrame(data, columns=['id', 'img_name', 'img_path', 'prediction', 'heatmap_path'])
    return data_df 