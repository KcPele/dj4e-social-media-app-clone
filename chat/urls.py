from django.urls import path
from chat.views import (
    ChatView, 
   
)

app_name = 'chat'

urlpatterns = [
    path('message/<str:pk>/', ChatView.as_view(), name="message"),
    
]