from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('drive', views.drive, name='drive'),
    path('generate', views.generateReport, name='generateReport'),
    path('how', views.howToUse, name='howToUse'),
    path('register/<int:tripID>', views.registerTrip, name='registerTrip'),
    path('inspect/<int:reportID>', views.inspectRegistration, name='inspectRegistration'),
    path('unregistered/<int:reportID>', views.unregister, name='unregister'),
    path('makepdf', views.makePDF, name='makepdf')
]