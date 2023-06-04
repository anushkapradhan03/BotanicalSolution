from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from .models import Blog
from BotanicalApi.mlModelsFunctions import predict_image, trainPlantPredictionModel

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import sys
import os
import glob
import re
import numpy as np
import cv2

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


# Model saved with Keras model.save()
diseaseDetectionAndSolution= r'D:\remoteGIThub\BotanicalSolution\BotanicalApi\mlModel\diseaseDetectionAndSolutionModel.h5'

# # Load your trained model
DiseaseDetectionAndSolutionModel = load_model(diseaseDetectionAndSolution)

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def model_predict(img_path, model):
    
    #update by ViPS
    img = cv2.imread(img_path)
    new_arr = cv2.resize(img,(100,100))
    new_arr = np.array(new_arr/255)
    new_arr = new_arr.reshape(-1, 100, 100, 3)
    

    
    preds = model.predict(new_arr)
    return preds

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        # Save the image and enum value
        f = request.FILES.get('image')
        enum_value = request.POST.get('enum')
        #f = request.files['image']
        print(f)
        #print(image)
        #f = image
        #f.filename = 'detectThis'

        # Perform any necessary processing or saving of the image
        # Save the image temporarily
        #image_path = '/path/to/save/image.png'  # Replace with the actual path to save the image

        # with open(image_path, 'wb') as file:
        #     for chunk in image.chunks():
        #         file.write(chunk)

        # Call the predict_image function from ml_model.py

        

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads',f.filename )  #secure_filename(f.filename)
        f.save(file_path)
        #file_path = r'D:\remoteGIThub\BotanicalSolution\BotanicalApi\uploads\PaperBellBact Spot.JPG'

        # Make prediction
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


        #prediction = predict_image(image_path)

        # Return the prediction result or any other response
        return JsonResponse({'message': 'Image processed successfully', 'prediction': prediction})
    else:
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def plant_suggestion(request):
    if request.method == 'POST':
        # Access the temperature, precipitation, and elevation values
        temperature = request.POST.get('temperature')
        precipitation = request.POST.get('precipitation')
        elevation = request.POST.get('elevation')
        print(temperature +" "+ precipitation+" "+elevation)

        # Load the dataset
        dataset_path = 'D:\minorProject\BotanicalSolution\BotanicalApi\plantprdecitiondataset.csv'
        dataset = pd.read_csv(dataset_path)
        print(dataset)

        # Split the dataset into input features (X) and target variable (y)
        X = dataset[['temperature', 'elevation', 'precipitation']]
        y = dataset['plant_type.']
        print('set')
        # Create and train the model
        model = DecisionTreeClassifier()
        model.fit(X, y)

        # Perform the prediction based on the given values
        predicted_plant = model.predict([[temperature, elevation, precipitation]])
        #predicted_plant = ["abc", "def"]
        predicted_plant = predicted_plant.tolist() 

        return JsonResponse({'predicted_plant': predicted_plant})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def post_blog(request):
    if request.method == 'POST':
        # Retrieve the blog details from the request
        title = request.POST.get('title')
        short_description = request.POST.get('short_description')
        detailed_paragraph = request.POST.get('detailed_paragraph')
        image = request.FILES.get('image')
        user_id = request.POST.get('user_id')
        star_ratings = request.POST.get('star_ratings')

        # Retrieve the User instance
        user = get_object_or_404(User, id=user_id)

        # Create a new blog instance
        blog = Blog(
            title=title,
            short_description=short_description,
            detailed_paragraph=detailed_paragraph,
            user=user,
            star_ratings=star_ratings
        )

        # If an image is provided, assign it to the blog instance
        if image:
            blog.image = image

        # Save the blog
        blog.save()

        return JsonResponse({'message': 'Blog posted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def get_blogs(request):
    blogs = Blog.objects.all()

    blog_data = []
    for blog in blogs:
        blog_data.append({
            'title': blog.title,
            'short_description': blog.short_description,
            'detailed_paragraph': blog.detailed_paragraph,
            'image': blog.image.url if blog.image else None,
            'user': blog.user.username,
            'star_ratings': blog.star_ratings,
            'posted_date': blog.posted_date.strftime('%Y-%m-%d'),
        })

    return JsonResponse({'blogs': blog_data})


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Sign in successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'Sign up successful'})
        else:
            return JsonResponse({'error': 'Username and password are required'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def signout(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})
