from django import forms
from .models import Room, Message

class RoomForm(forms.ModelForm):
    expiry_time = forms.ChoiceField(choices=[
        ('300', '5 minute'),
        ('600', '10 minute'),
        ('900', '15 minutes'),
        ('1800','30 minute'),
        ('3600', '1 hour'),
        ('7200','2 hours'),
        ('86400', '1 day'),
        ('604800', '1 week'),
        ('2592000', '1 month'),
        ('7889238','3 months'),
        ('15552000', '6 months'),

    ])

    class Meta:
        model = Room
        fields = ['room_name', 'password', 'expiry_time']

class PublicMessageForm(forms.ModelForm):
    expiry_time = forms.ChoiceField(choices=[
        ('60','1 minute'),
        ('300', '5 minutes'),
        ('600', '10 minutes'),
        ('900', '15 minutes'),
        ('1800','30 minutes'),
        ('2700','45 minutes'),
        ('3600', '1 hour'),
        ('7200','2 hours'),
        ('86400', '1 day'),

    ])

    class Meta:
        model = Message
        fields = ['content', 'image', 'expiry_time']

class RoomMessageForm(forms.ModelForm):
    expiry_time = forms.ChoiceField(choices=[
        ('60', '1 minute'),
        ('300', '5 minutes'),
        ('600', '10 minutes'),
        ('900', '15 minutes'),
        ('1800','30 minutes'),
        ('2700','45 minutes'),
        ('3600', '1 hour'),
        ('7200','2 hours'),
        ('86400', '1 day'),
    ])

    class Meta:
        model = Message
        fields = ['content', 'image', 'expiry_time']
