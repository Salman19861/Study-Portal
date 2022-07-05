from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields=['title','description']




class DateInput(forms.DateInput):
    input_type='date'
class HomeworkForm(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields=['subject','chapter','topic','due','is_finished']

class DashbaordForm(forms.Form):
    search=forms.CharField(max_length=200,label='Enter your Search ')
    

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','is_finished']
 

class registrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        def clean(self):
            cleaned_data=super().clean()
            pVar=self.cleaned_data['password']
            pVar2=self.cleaned_data['password2']
            if pVar!=pVar2:
                raise forms.ValidationError("Password doesn't match, try again !")