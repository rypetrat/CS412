## hw/views.py
## logic to handle URL requests
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.

# def home(request):
#     '''A function to respond to the /hw URl'''

#     ## create text
#     responseText = f'''
#     <html>
#     <h1> Hello World. </h1>
#     <p> django web page </p>
#     <hr> 
#     This page was generated at {time.ctime()}.
#     </html>
#     '''

#     ## return to client
#     return HttpResponse(responseText)

def home(request):
    '''A function to respond to the /hw URl, will delegate to the HTML template'''
    template_name = "hw/home.html"

    # create a dictionary of context variables 
    context = {
        'current_time': time.ctime(),
        'letter1': chr(random.randint(65,90)), # random Letter A-Z
        'letter2': chr(random.randint(65,90)), # random letter A-Z
        'number': random.randint(1,10), # random number 1-10
    }

    # delegate response to template
    return render(request, template_name, context)
