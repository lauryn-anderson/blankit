from django.urls import path
from .views import HomePageView, TextInputView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('text/', TextInputView.as_view(), name='text'),
    # path('blank/', BlankView.as_view(), name='blank'),
]
