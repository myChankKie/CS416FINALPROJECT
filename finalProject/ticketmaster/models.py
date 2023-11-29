from django.db import models

# Create your models here.

class Event_Search(models.Model):
    eventName = models.CharField(max_length=60)
    eventImage = models.CharField(max_length=60)
    startDate = models.CharField(max_length=60)
    localTime = models.CharField(max_length=60)
    venueName = models.CharField(max_length=60)
    venueCity = models.CharField(max_length=60)
    venueState = models.CharField(max_length=60)
    venueAddress = models.CharField(max_length=60)
    eventUrl = models.CharField(max_length=60)

class Favorites_Library(models.Model):
    accountUser = models.CharField(max_length=60)
    eventUrl = models.CharField(max_length=60)
    eventName = models.CharField(max_length=60)
    eventImage = models.CharField(max_length=60)
    startDate = models.CharField(max_length=60)
    localTime = models.CharField(max_length=60)
    venueName = models.CharField(max_length=60)
    venueCity = models.CharField(max_length=60)
    venueState = models.CharField(max_length=60)
    venueAddress = models.CharField(max_length=60)
    eventUrl = models.CharField(max_length=60)

# 'eventName': eventName,
# 'eventImage': eventImage,
# 'startDate': startDate,
# 'localTime': localTime,
# 'venueName': venueName,
# 'venueCity': venueCity,
# 'venueState': venueState,
# 'venueAddress': venueAddress,
# 'eventUrl': eventUrl