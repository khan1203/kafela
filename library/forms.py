from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BookRequest

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=255)
    student_id = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'name', 'student_id', 'email', 'phone', 'password1', 'password2']

class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = ['phone', 'borrow_duration']