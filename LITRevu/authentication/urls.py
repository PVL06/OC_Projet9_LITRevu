from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]