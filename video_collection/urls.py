from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('add', views.add, name='add_video'),
    path('video_list',views.video_list,name='video_list'),
    #creating a url for a page that would display information aboutt each video
    path('video_info', views.video_info, name='video_info' )
    #flow: 
    # 1. make a path 
    # 2. add a function in the view with the same string name (ex. add)
    # 3. create a new file in the video_collection folder: forms.py
    # We need a form to show to the user on the page so Django can collect user information directly from the form. 
    #At this point we already made a model for the database to follow. Model maps data from the form to the database.
    # Forms are created in forms.py. Go to forms.py for further details 
    

]