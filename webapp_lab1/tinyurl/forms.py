from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label = "Username",
        max_length = 150,
        required = True,
        help_text="150 characters or fewer. Letters, digits and @/./+/-/_ only"
        )
    email = forms.EmailField(
        label = "Email",
        required = True
    )
    gender = forms.ChoiceField(
        label = "Genger",
        choices=Profile.GENDERS
        )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type':'date',
        }))
    class Meta:
        model = User
        fields = ('username', 'email', 'date_of_birth','gender' ,'password1', 'password2', )
