from django.urls import path
from .views import GetAllData, ReceiveAgentData, index

urlpatterns = [
    path('receive/', ReceiveAgentData.as_view()),
    path('data/', GetAllData.as_view()),
    path('', index),
]
