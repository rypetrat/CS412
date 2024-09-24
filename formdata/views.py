from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def show_form(request):
    '''Show HTML form to the client.''' 

    template_name = 'formdata/form.html'
    return render(request, template_name)

def submit(request):
    '''Process the form submission, and generate a result.'''
    template_name = "formdata/confirmation.html"
    # read the form data into python variables:
    if request.POST:
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']
        context = {
            'name': name,
            'favorite_color':  favorite_color,
            
        }
        return render(request, template_name, context=context)