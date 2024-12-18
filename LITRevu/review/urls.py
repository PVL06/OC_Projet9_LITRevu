from django.urls import path

from . import views

urlpatterns = [
    path('flux/', views.FluxView.as_view(), name='flux'),
    path('posts/', views.PostsView.as_view(), name='posts'),
    path('follows/', views.FollowView.as_view(), name='follows'),
    path('ticket/create/', views.CreateTicketView.as_view(), name='create_ticket'),
    path('ticket/<int:id>/response/', views.ResponseToTicketView.as_view(), name='ticket_response'),
    path('review-complete/create/', views.CreateCompleteReviewView.as_view(), name='create_review'),
    path('<str:content_type>/<int:id>/update/', views.UpdateContentView.as_view(), name='update'),
    path('<str:content_type>/<int:id>/delete/', views.DeleteContentView.as_view(), name='delete'),
    path('unfollow/<int:id>', views.UnfollowView.as_view(), name='unfollow'),
]