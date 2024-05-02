from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Exists, OuterRef, Subquery, Count
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apexive.hotels.querysets import RoomQuerySet


# data model
class Hotel(models.Model):
    title = models.CharField(max_length=128)
    likes = models.PositiveIntegerField()
    dislikes = models.PositiveIntegerField()


class Room(models.Model):
    title = models.CharField(max_length=128)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')

    objects = RoomQuerySet.as_manager()


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    start = models.DateField()
    end = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
