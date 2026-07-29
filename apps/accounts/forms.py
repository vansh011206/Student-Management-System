from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'role', 'profile_pic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'profile_pic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'profile_pic':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
