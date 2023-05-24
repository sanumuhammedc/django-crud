from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add Task Here...'}))
    user = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'style': 'display:none'}))

    class Meta:
        model = Task
        fields = ['title', 'user']


class UpdateTaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(required=False, widget=forms.TextInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Task
        fields = ['title', 'complete']

        