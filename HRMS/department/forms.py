from django import forms
from .models import Department
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['Dept_Name', 'Description']
        widgets = {
            'Dept_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Confirm Password'}))
    class Meta:
        model =User
        fields = ['username','first_name','last_name','email','password1','password2']
        labels ={'email':'Email'}
        widgets= {'username':forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Username'}),
                  'email':forms.TextInput(attrs={'class':'form-control','placeholder': 'Email'}),
                  'first_name':forms.TextInput(attrs={'class':'form-control','placeholder': 'First Name'}),
                  'last_name':forms.TextInput(attrs={'class':'form-control','placeholder': 'Last Name'}),
                  }