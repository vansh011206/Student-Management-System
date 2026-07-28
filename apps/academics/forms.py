from django import forms
from .models import Class, Subject

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g. Class 10-A'
        })

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'class_name', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g. Mathematics'
        })
        self.fields['class_name'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['code'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g. MATH10'
        })
