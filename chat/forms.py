from chat.models import ChatMessage
from django.forms import ModelForm

class MessageForm(ModelForm):
    class Meta:
        model = ChatMessage  
        fields = ['body']