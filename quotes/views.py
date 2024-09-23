
from django.shortcuts import render
import random
from django.templatetags.static import static  # Import static function


#Da Vinci's quotes and images
quotes = [
    "Learning never exhausts the mind.",
    "Simplicity is the ultimate sophistication.",
    "Art is never finished, only abandoned."
]


images = [
    static('images/da_vinci_1.jpg'),
    static('images/da_vinci_2.jpg'),
    static('images/da_vinci_3.jpg')
]

# View to show one random quote and image
def quote(request):
    random_quote = random.choice(quotes)
    random_image = random.choice(images)
    context = {
        'quote': random_quote,
        'image': random_image
    }
    return render(request, 'quotes/quote.html', context)

# View to show all quotes and images
def show_all(request):
    context = {
        'quotes': quotes,
        'images': images
    }
    
    zipped_quotes = list(zip(quotes, images))  # Zip quotes and images
    return render(request, 'quotes/show_all.html', {'zipped_quotes': zipped_quotes})

# View to show information about Leonardo da Vinci
def about(request):
    context = {
        'name': "Leonardo da Vinci",
        'biography': "Leonardo da Vinci (1452–1519) was an Italian polymath of the Renaissance, known for his contributions to art, science, engineering, and anatomy. He is celebrated for masterpieces like the Mona Lisa and The Last Supper."
    }
    return render(request, 'quotes/about.html', context)
