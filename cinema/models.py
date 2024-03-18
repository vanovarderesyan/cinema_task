from django.db import models
from django.urls import reverse

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=500)
    row_count = models.PositiveIntegerField(null=True,blank=True)
    seat_count = models.PositiveIntegerField(null=True,blank=True)

    def get_absolute_url(self):
        return reverse('room-detail', args=[str(self.id)])

    def __str__(self) -> str:
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=500)
    poster = models.ImageField()
    duration = models.PositiveIntegerField(verbose_name="Please write duration of movie with in minute",null=True)

   
    def __str__(self) -> str:
        return self.name
    
class Schedule(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)


    def get_absolute_url(self):
        return reverse('schedule-detail', args=[str(self.id)])

    def __str__(self) -> str:
        return f'{self.movie.name}  {self.start_date.isoformat()}'

class Booking(models.Model):
    schedule = models.ForeignKey(Schedule,on_delete=models.SET_NULL,null=True)
    email = models.EmailField()
    row_index = models.PositiveIntegerField()
    seat_index = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.email