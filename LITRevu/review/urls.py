from django.urls import path

from . import views

urlpatterns = [
    path('', views.RewiewFluxView.as_view(), name='flux'),
    path('ticket/add/', views.CreateTicketView.as_view(), name='create_ticket'),
    path('review/add/', views.CreateReviewView.as_view(), name='create_review'),
    path('posts/', views.PostsView.as_view(), name='posts'),
    path('follow/', views.FollowView.as_view(), name='follows'),
    path('unfollow/<int:id>', views.UnfollowView.as_view(), name='unfollow'),
]