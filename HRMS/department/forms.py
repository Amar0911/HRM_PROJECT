from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['Dept_Name', 'Description']
        widgets = {
            'Dept_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Description': forms.Textarea(attrs={'class': 'form-control'}),
        }