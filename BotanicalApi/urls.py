from django.urls import path
from BotanicalApi import views

urlpatterns = [
    path('process-image/', views.process_image, name='process_image'),
    path('plant_suggestion/', views.plant_suggestion, name='plant_suggestion'),
    path('post-blog/', views.post_blog, name='post_blog'),
    path('get-blogs/', views.get_blogs, name='get_blogs'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
]
