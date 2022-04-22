
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from .models import Video
from django.contrib import messages
from django.core.exceptions import ValidationError
#reverse will convert the name of the url into an actual path when your server is running
# Create your tests here.
class TestHomePage(TestCase):
    def test_app_title_message_shown_on_homepage(self): #self needed because it is a method in a class
        url = reverse('home') #will generate right url
        response = self.client.get(url)
        #response is what your server responds with when you request a homepage
        self.assertContains(response, 'Dinner Collections')
    
class TestAddVideos(TestCase):
    #define test function
    def test_add_video(self):
        valid_video={
            'name': 'Comfort and Festive Dinner',
            'url': 'https://www.youtube.com/watch?v=kKiYVLIk_9s',
            'notes': ''
        }

        url = reverse('add_video')
        response= self.client.post(url, data = valid_video, follow= True) #making update to the db
        #follows allows redirects to happen without testsfailing because of a new http request from a redirect

        self.assertTemplateUsed('video_collection/video_list.html')
        self.assertContains(response,'Comfort and Festive Dinner')
        self.assertContains(response, 'https://www.youtube.com/watch?v=kKiYVLIk_9s')

        video_counts = Video.objects.count()
        self.assertEqual(1, video_counts)

        video = Video.objects.first() #will return the first result

        self.assertEqual('Comfort and Festive Dinner', video.name)
        self.assertEqual('https://www.youtube.com/watch?v=kKiYVLIk_9s', video.url)
        self.assertEqual('kKiYVLIk_9s', video.video_id)
    
    def test_invalid_url_not_valid(self):
        invalid_urls=[
            'https://www.youtube.com/watch?v=gcft',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch',
            'https://www.netflix.com/',
            'https://www.netflix.com/v=12342gerb'
        ]

        for invalid_url in invalid_urls:
            new_video ={
                'name':'qwerty',
                'url':invalid_url,
                'notes':'qwertyuiop'
            }

            url = reverse('add_video')
            response=self.client.post(url,new_video)

            #checking that we are still on the same page
            self.assertTemplateUsed('video_collections/add.html')

            #TODO: here i am getting an error
            messages=response.context['messages']
            message_texts=[message.message for message in messages]

            self.assertIn('Invalid YouTube url',message_texts)
            self.assertIn('Data is incomplete',message_texts)

            video_count= Video.objects.count()
            self.assertEqual(0,video_count)


class TestVideoList(TestCase):
    #are all the videos from the db displayed
    def test_all_videos_displayed_in_correct_order(self):

        v1 = Video.objects.create(name='ABC', notes='examples', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='obc', notes='examples', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(name='zoo', notes='examples', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(name='AAA', notes='examples', url='https://www.youtube.com/watch?v=126')

        expected_video_order=[v4,v1,v2,v3]

        url=reverse('video_list')
        response=self.client.get(url)

        videos_in_templates = list(response.context['videos']) #converting query set to a list
        #rendering is combining html and data
        
        #!!!!!!!!!!!!!!!!!!confusing: if I name v3 XYZ the test fails because the videos in template show XYZ before obc, which is incorrect order if we are using the Lower method
        self.assertEqual(expected_video_order,videos_in_templates)

    def test_no_video_message(self):
        url=reverse('video_list')
        response=self.client.get(url)
        self.assertContains(response, 'no matches, try again!')
        self.assertEqual(0,len(response.context['videos']))

    def test_video_number_message(self):
        v1 = Video.objects.create(name='ABC', notes='examples', url='https://www.youtube.com/watch?v=123')
        url=reverse('video_list')
        response=self.client.get(url)

        self.assertContains(response,'1 video')
        self.assertNotContains(response, '1 videos')

    def test_video_number_message_2_videos(self):
        v1 = Video.objects.create(name='ABC', notes='examples', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='obc', notes='examples', url='https://www.youtube.com/watch?v=124')

        url=reverse('video_list')
        response=self.client.get(url)

        self.assertContains(response,'2 video')
        self.assertNotContains(response, '2 videos')

class TestVideoSearch(TestCase):
    def test_video_search_matches(self):
        v1 = Video.objects.create(name='dinner', notes='examples', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='no', notes='examples', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(name='tasty dinNer', notes='examples', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(name='ooo Dinner', notes='examples', url='https://www.youtube.com/watch?v=126')

        searched_videos=[v1,v4,v3]

        url=reverse('video_list')
        response=self.client.get(reverse('video_list')+'?search_term=dinner')

        videos_in_templates = list(response.context['videos']) #converting query set to a list

        self.assertEqual(searched_videos,videos_in_templates)

    def test_video_search_no_matches(self):
        v1 = Video.objects.create(name='dinner', notes='examples', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='no', notes='examples', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(name='tasty dinNer', notes='examples', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(name='ooo Dinner', notes='examples', url='https://www.youtube.com/watch?v=126')

        expected_video_order =[]
        response=self.client.get(reverse('video_list')+'?search_term=dogs')
        videos_in_template=list(response.context['videos'])
        self.assertEqual(expected_video_order,videos_in_template) #no videos should be chosen
        self.assertContains(response,'no matches, try again!')


class testVideoModel(TestCase):
    def test_invalid_url_causes_Validation_Error(self):
        invalid_urls=[
            'https://www.youtube.com/watch?abc=123;',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch',
            'https://www.netflix.com/',
            'http://www.netflix.com/v=frrr'
        ]

        for invalid_url in invalid_urls:
            with self.assertRaises(ValidationError):
                Video.objects.create(name='qwerty',url=invalid_url,notes='qwertyuiop')
        
        self.assertEqual(0,Video.objects.count())
        

    #is integrity error raised when the video has been added 2ice?
    def test_duplicate_videos_raise_integrity_error(self):
        
        v1 = Video.objects.create(name='dinner', notes='examples', url='https://www.youtube.com/watch?v=123')
        #v2 = Video.objects.create(name='dinner', notes='examples', url='https://www.youtube.com/watch?v=123')
    #check for integrity error 
        with self.assertRaises(IntegrityError):
            Video.objects.create(name='dinner', notes='examples', url='https://www.youtube.com/watch?v=123')
