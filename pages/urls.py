from django.urls import path
from .views import HomePageView, about

urlpatterns = [
    path('about/', about, name='about'),
    path('', HomePageView.as_view(), name='home'),
]