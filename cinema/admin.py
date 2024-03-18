from django.contrib import admin
from django.contrib.admin import AdminSite
from  .models import  Room,Movie,Schedule,Booking
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import (
    ValidationError,
)
from django import forms
from django.db import IntegrityError
from datetime import datetime
import dateutil.parser
class CinemaAdminSite(AdminSite):

    site_title = 'Cinema admin'
    #
    site_header = 'Cinema admin'
    #
    index_title = 'Cinema admin'

class MyAdminForm(forms.ModelForm):
    def clean(self) -> None:
        if self.instance.pk is None:
            movie = Movie.objects.get(pk=self.data.get('movie'))
            start_date = dateutil.parser.parse(f"{self.data.get('start_date_0')} {self.data.get('start_date_1')}")
            end_date =  start_date + timedelta(minutes=movie.duration)
            if Schedule.objects.filter(room_id=self.data.get('room'),end_date__gt=start_date,start_date__lt=end_date).exists():
                raise ValidationError({"start_date": "This identifier is already in use."})
        super().clean()

class ScheduleAdmin(admin.ModelAdmin):
    form = MyAdminForm
    list_display = ['room', 'movie','start_date','end_date']
    readonly_fields=('end_date',)

    def save_model(self, request, obj, form, change):
        obj.end_date= obj.start_date + timedelta(minutes=obj.movie.duration)
        obj.save()

class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'row_count', 'seat_count']

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.save()

class BookingAdmin(admin.ModelAdmin):
    list_display = ['schedule', 'email','row_index', 'seat_index']

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.save()


cinema_admin_site = CinemaAdminSite()
cinema_admin_site.register(Room,RoomAdmin)
cinema_admin_site.register(Movie)
cinema_admin_site.register(Schedule,ScheduleAdmin)
cinema_admin_site.register(Booking,BookingAdmin)
