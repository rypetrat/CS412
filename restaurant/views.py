from django.shortcuts import render
import random
import time
from datetime import datetime, timedelta

# Create your views here.
def main(request):
    '''Show HTML form to the client.''' 

    template_name = 'restaurant/main.html'
    return render(request, template_name)

def order(request):
    '''Show HTML form to the client.''' 
    # List of daily specials
    daily_specials = ["Chicken Bracciola", "Chicken Marsala", "Baked Ziti", "Veal Picatta"]
    selected_daily_special = random.choice(daily_specials)  # Randomly select a daily special

    template_name = 'restaurant/order.html'
    return render(request, template_name, {'selected_daily_special': selected_daily_special})


def submit(request):
    '''Process the form submission, and generate a result.'''
    template_name = "restaurant/confirmation.html"

    # Initialize context dictionary
    context = {}

    # Check if the request method is POST
    if request.method == "POST":
        # Capture selected food items
        selected_food_items = request.POST.getlist('Food')

        # Capture the daily special
        daily_special = request.POST.get('daily', '')

        # Capture selected toppings if pizza is ordered
        selected_toppings = request.POST.getlist('toppings')

        # Capture the name field
        name = request.POST.get('name')

        # Capture the phone number field
        phone = request.POST.get('phone')

        # Capture the email field
        email = request.POST.get('email')

        # Capture the special instructions field
        special_instructions = request.POST.get('Special_Instructions', 'None')

        # Generate a random wait time between 30 and 60 minutes
        wait_time = random.randint(30, 60)

        # Get the current time and calculate the ready time
        current_time = datetime.now()
        ready_time = current_time + timedelta(minutes=wait_time)
        
        # Format the ready time for display in 12-hour format
        formatted_ready_time = ready_time.strftime("%I:%M %p")

        # Update the context with the submitted data
        context.update({
            'selected_food_items': selected_food_items,
            'daily_special': daily_special,
            'selected_toppings': selected_toppings,
            'name': name,
            'phone': phone,
            'email': email,
            'special_instructions': special_instructions,
            'ready_time': formatted_ready_time,
        })
    return render(request, template_name, context=context)

