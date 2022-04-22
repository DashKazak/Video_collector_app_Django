
from urllib import parse

from django.db import models
from django.core.exceptions import ValidationError

# Create your models her that describes a video object and its specifications
#Video class is a sublass of model (inheritance)
class Video(models.Model):
    #mapping the objects of video class to the db model
    name = models.CharField(max_length = 200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank = True, null = True)
    video_id = models.CharField(max_length=40,unique=True)

    def save(self, *args, **kwargs):
        #matches django save method arguments
        # if not self.url.startswith('https://www.youtube.com/watch'):
        #     raise ValidationError(f'Not a YouTube url {self.url}')
        #extract video id from youtube url
        url_components = parse.urlparse(self.url)

        if url_components.scheme != 'https':
            raise ValidationError(f'Not a YouTube url {self.url}')

        if url_components.netloc != 'www.youtube.com':
            raise ValidationError(f'Not a YouTube url {self.url}')

        if url_components.path != '/watch':
            raise ValidationError(f'Not a YouTube url {self.url}')

        #it knows where the query is !!!
        query_string = url_components.query
        if not query_string:
            raise ValidationError(f'Invalid YouTube url {self.url}')
        parameters = parse.parse_qs(query_string,strict_parsing = True)
        v_parameters_list = parameters.get('v') #return None if no key found (in the string the string will contain ?v=)
        if not v_parameters_list:
            #checking if none of empty list
            raise ValidationError(f'Invalid YouTube url, missing parameters {self.url}')

        #VIDEO_ID for the video_info page
        self.video_id = v_parameters_list[0] #string
        super().save(*args, **kwargs)


    #propagating to the db. Change db, don't forget to migrate
    def __str__(self) -> str:
        return f'ID: {self.pk}. Name: {self.name}. URL: {self.url}. Video ID: {self.video_id}. Notes: {self.notes[:200]} '

