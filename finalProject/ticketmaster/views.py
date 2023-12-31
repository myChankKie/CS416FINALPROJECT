from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# Make sure to install requests using 'pip install requests' on your terminal, otherwise 'requests' will not work
import requests
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime

from ticketmaster.forms import Favorites_Library_Form
from ticketmaster.models import Favorites_Library, Event_Search


def ticketmaster(request):
    return HttpResponse("Hello, world!")


@login_required(login_url='/login/1/')
def index(request):
    # if the request method is a post
    if request.method == 'POST':
        # get the search term and location
        classification = request.POST['classificationName']
        city = request.POST['city']
        # number_of_users = request.POST['number-of-users']
        # gender = request.POST['gender']

        # Check if either number_of_users or gender is empty
        if not classification or not city:
            # Set up an error message using Django's message utility to inform the user
            messages.info(request, 'Both classification and city are required fields.')
            # redirect user to the index page
            return redirect('ticketmaster-index')
            # Add code to handle or display the error_message as needed.

        # call get_random_users function() to get the data from the API
        random_events = get_events(classification, city)

        # If the request to fetch data from randomuser was unsuccessful or returned None
        if random_events is None:
            # Set up an error message using Django's message utility to inform the user
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            # redirect user to the index page
            return redirect('ticketmaster-index')
        elif random_events['page']['totalElements'] == 0:
                messages.info(request, 'No Events were Found.')
                return redirect('ticketmaster-index')

        else:

            # print the response for testing purpose (open "Run" at the bottom to see what is printed)
            print(random_events)
            # Store each user's information in a variable
            events = random_events['_embedded']['events']

            # Initialize an empty list to store user data
            event_list = []
            # eventsArr = events['_embedded']['events']

            # Iterate through each user in the 'users' list coming from the api
            # Rather than directly passing the "users" array to the template,
            # the following approach allows server-side processing and formatting of specific data (e.g., date).
            # So, the template only needs to plug in the preprocessed information.

            Event_Search.objects.all().delete()
            for event in events:
                # Extract relevant information from the event dictionary
                eventName = event['name']
                print(eventName)
                eventImage = event['images'][0]['url']
                print(eventImage)
                if event['dates'] is None:
                    startDate = 'none'
                else:
                    startDate = event['dates']['start']['localDate']

                if event['dates']['start']['noSpecificTime'] is True:
                    localTime = 'none'
                else:
                    localTime = datetime_from_utc_to_local(event['dates']['start']['localTime'])
                # startDate = event['dates']['start']['dateTime']
                # localTime = event['dates']['start']['localTime']
                # startDate = 'none'
                # localTime = 'none'
                venueName = event['_embedded']['venues'][0]['name']
                venueCity = event['_embedded']['venues'][0]['city']['name']
                venueState = event['_embedded']['venues'][0]['state']['name']
                venueAddress = event['_embedded']['venues'][0]['address']['line1']
                eventUrl = event['url']
                # first_name = user['name']['first']
                # last_name = user['name']['last']
                # email = user['email']
                # phone = user['phone']
                # picture = user['picture']['large']
                # registration_date = user['registered']['date']

                # Format the registration date from "2004-03-12T17:05:44.193Z" to "2004"
                # Extract the first 10 characters to get the date portion, then convert to a datetime object
                # date_object = datetime.strptime(registration_date[:10], "%Y-%m-%d")

                # Format the date object to a more readable format, e.g., "Sat Nov 03 2023"
                # registration_date = date_object.strftime("%a %b %d %Y")

                # Create a new dictionary to store user details
                event_details = {
                    'eventName': eventName,
                    'eventImage': eventImage,
                    'startDate': startDate,
                    'localTime': localTime,
                    'venueName': venueName,
                    'venueCity': venueCity,
                    'venueState': venueState,
                    'venueAddress': venueAddress,
                    'eventUrl': eventUrl
                    #  'registration_date': registration_date
                }
                currentSearch = Event_Search()
                currentSearch.eventName = eventName
                currentSearch.eventImage = eventImage
                currentSearch.startDate = startDate
                currentSearch.localTime = localTime
                currentSearch.venueName = venueName
                currentSearch.venueCity = venueCity
                currentSearch.venueState = venueState
                currentSearch.venueAddress = venueAddress
                currentSearch.eventUrl = eventUrl
                currentSearch.save()

                # Append the user details dictionary to the user_list
                event_list.append(event_details)
            allEventsSearch = Event_Search.objects.all()
            # Create a context dictionary with the user_list and render the 'thanks.html' template
            context = {'events': allEventsSearch}
            return render(request, 'ticketmaster/index.html', context)

    # all other cases, just render the page without sending/passing any context to the template
    return render(request, 'ticketmaster/index.html')

@login_required(login_url='/login/1/')
def add_favorite(request, event_id):
    clickedEvent = Event_Search.objects.get(id=event_id)

    currentFavorite = Favorites_Library()
    currentFavorite.accountUser = request.user.username
    currentFavorite.eventName = clickedEvent.eventName
    currentFavorite.eventImage = clickedEvent.eventImage
    currentFavorite.startDate = clickedEvent.startDate
    currentFavorite.localTime = clickedEvent.localTime
    currentFavorite.venueName = clickedEvent.venueName
    currentFavorite.venueCity = clickedEvent.venueCity
    currentFavorite.venueState = clickedEvent.venueState
    currentFavorite.venueAddress = clickedEvent.venueAddress
    currentFavorite.eventUrl = clickedEvent.eventUrl
    currentFavorite.save()
    return render(request, 'ticketmaster/index.html')

@login_required(login_url='/login/1/')
def create_favorite(request):
    # Create a form instance and populate it with data from the request
    form = Favorites_Library_Form(request.POST or None)
    # check whether it's valid:
    if form.is_valid():
        obj = form.save(commit=False)
        obj.accountUser = request.user.username
        # save the record into the db
        obj.save()
        form.save()
        # after saving redirect to view_product page
        return redirect('ticketmaster-favorites')

    # if the request does not have post data, a blank form will be rendered
    return render(request, 'ticketmaster/favorite-form.html', {'form': form})
@login_required(login_url='/login/1/')
def update_favorite(request, event_id):
    favorite = Favorites_Library.objects.get(id=event_id)

    form = Favorites_Library_Form(request.POST or None, instance=favorite)
    if form.is_valid():
        form.save()
        return redirect('ticketmaster-favorites')
    return render(request, 'ticketmaster/favorite-form.html', {'form': form})

@login_required(login_url='/login/1/')
def delete_favorite(request, event_id):
    favorite = Favorites_Library.objects.get(id=event_id)

    if request.method == 'POST':
        favorite.delete()
        return redirect('ticketmaster-favorites')
    return render(request, 'ticketmaster/delete-confirm.html', {'favorite': favorite})


@login_required(login_url='/login/1/')
def favorites_view(request):
    userFavoritesLibrary = Favorites_Library.objects.filter(accountUser=request.user.username)
    context = {'events': userFavoritesLibrary}
    print(context)
    return render(request, 'ticketmaster/favorites.html', context)


def get_events(classification, city):
    try:
        # Construct the URL with parameters
        url = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=v9I9u0Cd8x7LBlYmhCoNH8SodUerO9vn"

        # The query parameters will be appended to the url such as https://randomuser.me/api/?results=5&gender=female&nat=us
        params = {
            "sort": 'date,asc',
            "classificationName": classification,
            "city": city
        }

        # Send a GET request to the specified URL with parameters
        response = requests.get(url, params=params)

        # Raise an exception for 4xx and 5xx status codes
        response.raise_for_status()

        # Parse the JSON data from the response
        data = response.json()

        # Return the parsed data
        return data
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        print(f"Request failed: {e}")

        # Return None to indicate failure
        return None


def datetime_from_utc_to_local(utc_datetime):
    from datetime import datetime as dt
    date_obj = dt.strptime(utc_datetime, '%H:%M:%S')

    return dt.strftime(date_obj, '%I:%M %p')
