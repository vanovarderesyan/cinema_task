from django.urls import path,include,reverse
from .views import RoomView,BookDetailView,ScheduleDetailView,BookinglView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RoomView.as_view(), name='rooms'),
    path('room/<int:pk>', BookDetailView.as_view(), name='room-detail'),
    path('schedule/<int:pk>',ScheduleDetailView.as_view(),name='schedule-detail'),
    path('booking/<int:pk>',BookinglView.as_view(),name='booking')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
