from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

# Create your views here.
from django.middleware.csrf import get_token
from BotanicalApi.constant.BotanicalConstant import BotanicalConstant
from BotanicalApi.modelLogic.deseaseDetectionService import detectDesease
from BotanicalApi.modelLogic.detectObjectType import detectIsLeaf
# from BotanicalApi.modelLogic.deseaseDetectionService import detectDesease
from BotanicalApi.modelLogic.plantSuggestionService import suggestPlant
import os


# get Token
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})



#### Request Functions

@csrf_exempt
def process_image(request):
    message = ""
    if request.method == 'POST':
        # Save the image and enum value
        uploaded_file = request.FILES.get('image')
        enum_value = request.POST.get('enum')
        print(uploaded_file)

        if uploaded_file:
            # Create a unique filename to avoid overwriting existing files
            file_name = f"{enum_value}_{uploaded_file.name}"
            basepath = os.path.dirname(__file__)
            print('basepath',basepath)

            # Define the destination path
            destination_path = os.path.join(basepath, 'uploads', file_name)

            # Open a file for writing and save the content
            with open(destination_path, 'wb') as destination_file:
                for chunk in uploaded_file.chunks():
                    destination_file.write(chunk)
        else:
            return JsonResponse({'message': 'No file uploaded', 'prediction': "error"})

        # try:
        #     # Save the file to ./uploads
        #     basepath = os.path.dirname(__file__)
        #     print('basepath',basepath)
        #     fs = FileSystemStorage(location=os.path.join(os.path.dirname(__file__), 'uploads'))
        #     filename = fs.save(uploaded_file.name, uploaded_file)
        #     file_path = fs.url(filename)
        # except:
        #     return JsonResponse({'message': 'Image Saving Failed', 'prediction': "error"})

        # detect Plant leave of not
        # try:
        #     messageLeaf, isPlant = detectIsLeaf(file_path)
        #     message = message + 'This Image is : ' + messageLeaf
            
        # except:
        #     return JsonResponse({'message': 'Image processed Fail', 'prediction': "error"})
        
        isPlant = True
        if(isPlant):
            print(enum_value)
            try:
                if(enum_value=="solution"):
                    
                    prediction = detectDesease(destination_path)

                    # Return the prediction result or any other response
                    message = message + " | Image processed successfully: detectDesease'" 
                    # Remove the file after processing
                    os.remove(destination_path)
                    return JsonResponse({'message': message, 'prediction': prediction})
                elif(enum_value=="leaf"):
                    # prediction = detectLeafType(file_path)
                    prediction = "Feature Under Development"
                    message = message + " | Image processed successfully: leafPredection'" 
                    # Remove the file after processing
                    os.remove(destination_path)
                    return JsonResponse({'message': message, 'prediction': prediction})
            
                
            except:
                # Remove the file after processing
                os.remove(destination_path)
                return JsonResponse({'message': 'Image or Enum Failed or not passed', 'prediction': "error"})
        else:
           # Remove the file after processing
           os.remove(destination_path)
           return JsonResponse({'message': message, 'prediction': "Not a leaf"}) 

    else:
        # Remove the file after processing
        os.remove(destination_path)
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def plant_suggestion(request):
    if request.method == 'POST':
        # Access the temperature, precipitation, and elevation values
        try:
            temperature = request.POST.get(BotanicalConstant.temperature)
            precipitation = request.POST.get(BotanicalConstant.precipitation)
            elevation = request.POST.get(BotanicalConstant.elevation)

            try:
                predicted_plant = suggestPlant(temperature, precipitation, elevation)  
                return JsonResponse({'predicted_plant': predicted_plant})  
            except:
                return JsonResponse({'predicted_plant Failed To predict'}, status=206)

        except:
            return JsonResponse({'error': 'temperature, precipitation, elevation not in form-data'},  status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=404)


# # @csrf_exempt
# # def post_blog(request):
# #     if request.method == 'POST':
# #         # Retrieve the blog details from the request
# #         title = request.POST.get('title')
# #         short_description = request.POST.get('short_description')
# #         detailed_paragraph = request.POST.get('detailed_paragraph')
# #         image = request.FILES.get('image')
# #         user_id = request.POST.get('user_id')
# #         star_ratings = request.POST.get('star_ratings')

# #         # Retrieve the User instance
# #         user = get_object_or_404(User, id=user_id)

# #         # Create a new blog instance
# #         blog = Blog(
# #             title=title,
# #             short_description=short_description,
# #             detailed_paragraph=detailed_paragraph,
# #             user=user,
# #             star_ratings=star_ratings
# #         )

# #         # If an image is provided, assign it to the blog instance
# #         if image:
# #             blog.image = image

# #         # Save the blog
# #         blog.save()

# #         return JsonResponse({'message': 'Blog posted successfully'})
# #     else:
# #         return JsonResponse({'error': 'Invalid request method'})

# # def get_blogs(request):
# #     blogs = Blog.objects.all()

# #     blog_data = []
# #     for blog in blogs:
# #         blog_data.append({
# #             'title': blog.title,
# #             'short_description': blog.short_description,
# #             'detailed_paragraph': blog.detailed_paragraph,
# #             'image': blog.image.url if blog.image else None,
# #             'user': blog.user.username,
# #             'star_ratings': blog.star_ratings,
# #             'posted_date': blog.posted_date.strftime('%Y-%m-%d'),
# #         })

# #     return JsonResponse({'blogs': blog_data})

# # @csrf_exempt
# # def signin(request):
# #     if request.method == 'POST':
# #         username = request.POST.get('username')
# #         password = request.POST.get('password')

# #         user = authenticate(request, username=username, password=password)
# #         if user is not None:
# #             login(request, user)
# #             return JsonResponse({'message': 'Sign in successful'})
# #         else:
# #             return JsonResponse({'error': 'Invalid credentials'})
# #     else:
# #         return JsonResponse({'error': 'Invalid request method'})

# # @csrf_exempt
# # def signup(request):
# #     if request.method == 'POST':
# #         username = request.POST.get('username')
# #         password = request.POST.get('password')

# #         if username and password:
# #             # Create a new user
# #             user = User.objects.create_user(username=username, password=password)
# #             return JsonResponse({'message': 'Sign up successful'})
# #         else:
# #             return JsonResponse({'error': 'Username and password are required'})
# #     else:
# #         return JsonResponse({'error': 'Invalid request method'})

# # def signout(request):
#     logout(request)
#     return JsonResponse({'message': 'Logged out successfully'})



if __name__ == '__main__':
    print("importing View")