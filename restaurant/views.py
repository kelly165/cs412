from django.shortcuts import render

# Create your views here.
from datetime import datetime, timedelta
import random

# View for the main page
def main(request):
    return render(request, 'restaurant/main.html')

# View for the ordering page
def order(request):
    # Randomly choose a "daily special" from a list
    daily_specials = ['Pizza', 'Burger', 'Pasta', 'Salad', 'Sushi']
    daily_special = random.choice(daily_specials)
    
    # Add the daily special to the context
    context = {
        'daily_special': daily_special,
    }
    return render(request, 'restaurant/order.html', context)

# View for the confirmation page
def confirmation(request):
    if request.method == 'POST':
        # Get form data
        customer_name = request.POST.get('name', 'Customer')
        ordered_items = request.POST.getlist('items')
        
        # Prices for each item (simple dictionary for now)
        item_prices = {
            'Pizza': 10.00,
            'Burger': 8.50,
            'Pasta': 9.00,
            'Salad': 7.50,
            'Sushi': 12.00,
        }
        
        # Calculate total price for the order
        total_price = sum(item_prices[item] for item in ordered_items if item in item_prices)
        
        # Random ready time (30-60 minutes from now)
        ready_time_minutes = random.randint(30, 60)
        ready_time = datetime.now() + timedelta(minutes=ready_time_minutes)

        # Prepare context for confirmation page
        context = {
            'customer_name': customer_name,
            'ordered_items': ordered_items,
            'total_price': total_price,
            'ready_time': ready_time.strftime('%I:%M %p'),
        }
        
        # Render confirmation.html
        return render(request, 'restaurant/confirmation.html', context)
    else:
        # If accessed via GET (shouldn't happen), redirect to the order page
        return render(request, 'restaurant/order.html')