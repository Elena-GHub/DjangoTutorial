# DjangoTutorial
Repo where I will be uploading the files as I follow the official Django tutorial.  
[Writing your first app (Polls)](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)

### My initial setup:
* Django 3.1.2
* Python 3.9
* IDE: VS Code
  
### Secret key exposed warning  
I received a notification about the secret key from this django project being exposed. Although this is not code for production whatsoever, I looked into it and I decided to set it as an env variable. Besides the [official django documentation](https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/) I found a clear [video tip](https://www.youtube.com/watch?v=IolxqkL7cD8) by Corey Schafer, right to the point.  
  
### Part 5 - Unit tests and a couple of extra
First I added the regular unit tests as per the tutorial.  
In the tutorial, they had a point when they suggested that only questions with choices should be displayed in the Polls index view. I actually thought that even questions with only one choice did not make sense. Therefore, I also reworked both the index view and the existing tests in order to make sure that only questions with at least two choices were displayed in the Polls index view.  
  
### Part 6 - Customize Polls app's look and feel
With the little I already knew about front-end, I found this part of the tutorial very succinct.  
So I went a little freestyle and I added the following:  
* __Template extension__: this [tutorial](https://tutorial.djangogirls.org/en/template_extending/) came in handy.  
* __css styling__: I added a dark background image and I made a __sticky footer__ (here is [the simplest solution I found for this](https://css-tricks.com/couple-takes-sticky-footer/#there-is-flexbox))  
  
### EXTRA Feature nav - Add a top navbar to the website
In order to be able to move around views without having to type the url, I added a home page to the website and a top navbar. I did it as another app called "common". I am not sure if this is the best way but it serves the purpose I wanted. The appropriate unit test has also been added.  
