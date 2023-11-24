from django.shortcuts import render
from .forms import ContactForm


def contact(request):
    # Create a form instance and populate it with data from the request if request is a POST (request.POST parts works)
    # if not, create an empty form instance (None parts works below)
    form = ContactForm(request.POST or None)

    # Check to see if request is a POST
    # if this is a POST request, we need to process the form data and save the data
    if request.method == 'POST':
        # before saving check whether the form data is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # print (form.cleaned_data['email']) # for example,email can be accessed using form.cleaned_data['email']
            form.save()
            # redirect to a new URL:
            return render(request, 'contact/thanks.html')

    context = {'form': form}
    return render(request, 'contact/contact.html', context)
