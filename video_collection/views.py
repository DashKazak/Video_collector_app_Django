from email import message
from django.shortcuts import render,redirect,get_object_or_404
from .forms import SearchForm, VideoForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Video
from django.db.models.functions import Lower

# model describes both structure of the db + object in your code  

# Create your views here.
#homepageview
def home(request):
    app_name = 'Dinner Collections'
    return render(request, 'video_collection/home.html', {'app_name': app_name})
    #dictionary in the end matches the placeholder in home.html and connects the variable between the files

#2. create a function add in views
#3. from .forms import your form
def add(request):
    #assign the form
    if request.method == 'POST':
        new_video_form = VideoForm(request.POST)
        #is_valid is a method
        if new_video_form.is_valid():
            #save to the db
            #validating usrer input
            try:
                new_video_form.save()
                #if we have a valid form and have saved a new video, we will redirect the user
                return redirect('video_list')
                #messages.info(request,'Success')
            except ValidationError:
                messages.warning(request, 'Invalid YouTube url')
            #integrity - db double entry error
            except IntegrityError:
                messages.warning(request, 'You already added this video')
        
        #allow user to edit their faulty infoif the video is not saved (try failed)
        messages.warning(request, 'Data is incomplete')
        return render(request, 'video_collection/add.html', {'new_video_form':new_video_form})

    new_video_form = VideoForm()
    #Server comes back with an html file with the information requested 
    #from here, next step is to create an add.html
    return render(request, 'video_collection/add.html', {'new_video_form':new_video_form})

def video_list(request):
    search_form = SearchForm(request.GET) #build form from data that user sent to app

    if search_form.is_valid(): #if user has enterd data
        search_term = search_form.cleaned_data['search_term'] 
        #lower method allows sorting by alphabet, ignoring computers urge to put non-capital letters last
        videos = Video.objects.filter(name__icontains = search_term).order_by(Lower('name'))
        #django matching tool __icontain
    else:
        #new user or form is not valid
        search_form = SearchForm()
        videos = Video.objects.order_by('name')
    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})

def video_info(request):
    #on the video form, each video has a video ID from the url


    p_video = get_object_or_404(Video, video_id= Video.video_id)
    return render(request, 'video_info', p_video = p_video)
