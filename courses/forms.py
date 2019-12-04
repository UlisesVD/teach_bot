from django import forms
from .models import Course, Unity
from datetime import datetime
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'date_start', 'date_end']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'date_start':forms.DateInput(
                format = "%Y-%m-%d",
                attrs={'class':'form-control', 'type':'date'}),
            'date_end':forms.DateInput(
                format = "%Y-%m-%d",
                attrs={'class':'form-control', 'type':'date'}),
            }

class UnityForm(forms.ModelForm):
    class Meta:
        model = Unity
        fields = ['name', 'description', 'date_start', 'date_end', 'id_course']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'id_course': forms.TextInput(attrs={'class':'form-control', 'type':'hidden'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'date_start':forms.DateInput(
                format = "%Y-%m-%d",
                attrs={'class':'form-control', 'type':'date'}),
            'date_end':forms.DateInput(
                format = "%Y-%m-%d",
                attrs={'class':'form-control', 'type':'date'}),
        }
