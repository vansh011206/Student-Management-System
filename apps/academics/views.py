from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.accounts.decorators import admin_required
from .models import Class, Subject
from .forms import ClassForm, SubjectForm

@admin_required
def class_list_create(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            cls = form.save()
            messages.success(request, f'Class "{cls.name}" added successfully!')
            return redirect('class_list')
        else:
            messages.error(request, 'Error adding class. Please check the name.')
    else:
        form = ClassForm()

    context = {
        'classes': classes,
        'form': form,
    }
    return render(request, 'academics/class_list.html', context)

@admin_required
def delete_class(request, class_id):
    cls = get_object_or_404(Class, id=class_id)
    class_name = cls.name
    cls.delete()
    messages.success(request, f'Class "{class_name}" deleted successfully.')
    return redirect('class_list')

@admin_required
def subject_list_create(request):
    subjects = Subject.objects.select_related('class_name').all()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            messages.success(request, f'Subject "{subject.name}" created successfully!')
            return redirect('subject_list')
        else:
            messages.error(request, 'Error creating subject. Please check inputs.')
    else:
        form = SubjectForm()

    context = {
        'subjects': subjects,
        'form': form,
    }
    return render(request, 'academics/subject_list.html', context)

@admin_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    name = subject.name
    subject.delete()
    messages.success(request, f'Subject "{name}" deleted successfully.')
    return redirect('subject_list')
