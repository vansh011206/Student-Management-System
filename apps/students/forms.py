from django import forms
from .models import Student, Teacher

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_class', 'roll_number', 'date_of_birth',
            'blood_group', 'parent_name', 'parent_phone', 'address'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['subject', 'assigned_class', 'joining_date', 'qualification']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
