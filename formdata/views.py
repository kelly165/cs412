from django.shortcuts import render, redirect

# Create your views here.
def show_form(request):
    '''show the contact form'''

    template_name = "formdata/form.html"

    return render(request, template_name)


def submit(request):
    '''
    Handle the form submission
    Read the form data from the request,
    and send it back to a template
    '''

    template_name = 'formdata/confirmation.html'
    print(request)
    #read the form data iinto python vars
    if request.POST:
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']
    # package the form data up as context variables for the template
        context = {
            'name': name,
            'favorite_color': favorite_color,
        }
        return render(request, template_name, context)

#template_name = "formdata/form.html"
#return render(request, template_name)

    return redirect("show_form")