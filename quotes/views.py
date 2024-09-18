from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# defines global lists for the quotes and images, each has 5 elements
allQuotes = ["Love your Enemies for they tell you your Faults", "He that falls in love with himself will have no rivals.", "There never was a good war or a bad peace.", "He that lies down with Dogs, shall rise up with fleas.", "Better slip with foot than tongue."]
allImages = ["https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.britannica.com%2F72%2F110272-050-3CDD8564%2FBenjamin-Franklin.jpg&f=1&nofb=1&ipt=d2615f43a5b5faa9c5e2507ae2d16938856a8b2d68f07bf5fdcf43c80716acd2&ipo=images", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.thefamouspeople.com%2Fprofiles%2Fimages%2Fbenjamin-franklin.jpg&f=1&nofb=1&ipt=9a71df9f4761022f1a59b2da9ee34de069c8194d8c632750d08fcaf64f0b3062&ipo=images", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.timeforkids.com%2Fwp-content%2Fuploads%2F2018%2F08%2FFranklin-HERO.jpg&f=1&nofb=1&ipt=c2fa24896d8d7d16ceae39d47f8174e05eda9115554915dc1af2df2f440d0abf&ipo=images", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.ZLIrMKgQMbH6zhQLFvwQxAHaFG%26pid%3DApi&f=1&ipt=b8eeaacfe28848d2f7ca21643b3c5cc7e4eefa6e16a271e65ab105b0d23d3318&ipo=images", "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.historynet.com%2Fwp-content%2Fuploads%2F2022%2F04%2FBenjamin-Franklin-Portrait-scaled-1200x1567.jpeg&f=1&nofb=1&ipt=5c56855e8880326a79be6ca0e876fb1818aa342ada871b2e5584cd598d8b2631&ipo=images"]


def main(request):
    '''A function to respond to the / URl, will delegate to the base.html template file'''
    template_name = "quotes/base.html"

    # dictionary of context variables
    context = {
        'quote': allQuotes[random.randint(0, 4)],  # Randomly selected quote
        'image': allImages[random.randint(0, 4)],  # Randomly selected image
    }

    # delegate response to template
    return render(request, template_name, context)

def quotes(request):
    '''A function to respond to the /quote URl, will delegate to the quote.html template file'''
    template_name = "quotes/quote.html"

    # dictionary of context variables
    context = {
        'quote': allQuotes[random.randint(0, 4)],  # Randomly selected quote
        'image': allImages[random.randint(0, 4)],  # Randomly selected image
    }

    # delegate response to template
    return render(request, template_name, context)

def show_all(request):
    '''A function to respond to the /show_all URl, will delegate to the show_all.html template file'''
    template_name = "quotes/show_all.html"

    # dictionary of context variables 
    context = {
        'quotes': allQuotes[:], # all quotes
        'images': allImages[:], # all images
    }

    # delegate response to template
    return render(request, template_name, context)

def about(request):
    '''A function to respond to the /about URl, will delegate to the about.html template file'''
    template_name = "quotes/about.html"

    # delegate response to template
    return render(request, template_name)