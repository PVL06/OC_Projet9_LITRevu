from django.urls import path

from . import views

urlpatterns = [
    path('', views.RewiewFluxView.as_view(), name='review'),
]