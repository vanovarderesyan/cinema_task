from django.shortcuts import render
from django.urls import reverse
from django.views import View,generic
from django.http import HttpResponseRedirect
from datetime import timedelta
from django.utils import timezone
from .models import Room,Movie,Schedule,Booking
class RoomView(generic.ListView):
    model = Room
    context_object_name = 'room_list'   
    queryset = Room.objects.all()
    template_name = 'room_list.html' 

    def get_context_data(self, **kwargs):
        context = super(RoomView, self).get_context_data(**kwargs)
        context['room_list'] = self.queryset
        return context
    
class BookDetailView(generic.DetailView):
    model = Room
    context_object_name = 'room'   
    template_name = 'room_detail.html'

    def get_context_data(self, **kwargs):
        context = {}
        room = self.get_object()
        context['room']  = room
        thirty_minutes_ago = timezone.now() - timedelta(minutes=15)
        context['movies']  = Schedule.objects.filter(room=room,start_date__gte=thirty_minutes_ago)
        print(context['movies'] )


        return context
class ScheduleDetailView(generic.DetailView):
    model = Schedule
    context_object_name = 'schedule_detail'
    template_name = 'schedule_detail.html'

    def get_context_data(self, **kwargs):
        context = {}
        schedule = self.get_object()
        print(schedule)
        # booking_seats = Booking.objects.filter(schedule=self.get_object())
        seats_data = []
        for row_index in range(1,schedule.room.row_count+1):
            row_info = {
                "index" : row_index,
                "seats" : []
            }
            for seat_index in range(1,schedule.room.seat_count+1):
                seat_info = {
                    "index" : seat_index,
                    "free" : True
                }
                if Booking.objects.filter(row_index=row_index,seat_index=seat_index,schedule=self.get_object()).exists():
                    seat_info['free'] = False
                row_info['seats'].append(seat_info)
            seats_data.append(row_info)

        context['schedule']  =  schedule
        context['seats'] = seats_data
        return context
    

class BookinglView(generic.CreateView):
    model = Booking

    def get(self, request, *args, **kwargs):
        return  HttpResponseRedirect(redirect_to=f'/schedule/{kwargs["pk"]}')

    def post(self, request, *args, **kwargs):
        self.object = None
        Booking.objects.create(
            schedule_id = kwargs["pk"],
            email = request.POST.get('email'),
            row_index = request.POST.get('row_index'),
            seat_index = request.POST.get('seat_index')
        )
        return HttpResponseRedirect(redirect_to=f'/schedule/{kwargs["pk"]}')