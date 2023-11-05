from django.conf import settings
import os

from tensorflow import keras
import tensorflow as tf
import numpy as np
import cv2


basePath = settings.BASE_DIR
# Model saved with Keras model.save()
diseaseDetectionAndSolutionRelativePath = '/BotanicalApi/mlModel/diseaseDetectionAndSolutionModel.h5'
diseaseDetectionAndSolutionModelPath= os.path.join(basePath, diseaseDetectionAndSolutionRelativePath)




# # Function to load a saved .h5 model and make predictions
def load_and_predict_h5_model(model_path):
    # Load the saved model
    model = keras.models.load_model(model_path)
    return model

def model_predict(img_path, model):
    
    #update by ViPS
    img = cv2.imread(img_path)
    new_arr = cv2.resize(img,(100,100))
    new_arr = np.array(new_arr/255)
    new_arr = new_arr.reshape(-1, 100, 100, 3)

    preds = model.predict(new_arr)
    return preds



def detectDesease(file_path):
    # Make prediction
    DiseaseDetectionAndSolutionModel = load_and_predict_h5_model(diseaseDetectionAndSolutionModelPath)
    preds = model_predict(file_path, DiseaseDetectionAndSolutionModel)

    # Process your result for human
    pred_class = preds.argmax()              # Simple argmax

    
    CATEGORIES = ['Pepper__bell___Bacterial_spot','Pepper__bell___healthy',
        'Potato___Early_blight' ,'Potato___Late_blight', 'Potato___healthy',
        'Tomato_Bacterial_spot' ,'Tomato_Early_blight', 'Tomato_Late_blight',
        'Tomato_Leaf_Mold' ,'Tomato_Septoria_leaf_spot',
        'Tomato_Spider_mites_Two_spotted_spider_mite' ,'Tomato__Target_Spot',
        'Tomato__YellowLeaf__Curl_Virus', 'Tomato_mosaic_virus',
        'Tomato_healthy']
    
    prediction = CATEGORIES[pred_class]
    return prediction


if __name__ == '__main__':
    print("importing deseaseDetectionService")