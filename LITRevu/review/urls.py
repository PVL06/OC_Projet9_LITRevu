from django.urls import path

from . import views

urlpatterns = [
    path('', views.RewiewFluxView.as_view(), name='review'),
    path('follow/', views.FollowView.as_view(), name='follows'),
    path('unfollow/<int:id>', views.UnfollowView.as_view(), name='unfollow'),
]