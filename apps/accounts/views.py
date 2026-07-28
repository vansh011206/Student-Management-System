from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CustomUser
from .decorators import admin_required
from .forms import ProfileUpdateForm
from apps.students.models import Student, Teacher
from apps.academics.models import Class, Subject
from apps.attendance.models import Attendance
from apps.exams.models import Result
from apps.students.utils import get_monthly_attendance_chart, get_class_wise_students

def root_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_admin():
        return redirect('admin_dashboard')
    elif request.user.is_teacher():
        return redirect('teacher_dashboard')
    elif request.user.is_student():
        return redirect('student_dashboard')
    return redirect('login')

def login_view(request):
    if request.user.is_authenticated:
        return root_redirect(request)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        selected_role = request.POST.get('role', 'admin')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            if user.is_admin():
                return redirect('admin_dashboard')
            elif user.is_teacher():
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_profile':
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            password_form = PasswordChangeForm(user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error in the profile form.')
        elif action == 'change_password':
            profile_form = ProfileUpdateForm(instance=user)
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was updated successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error in the password change form.')
    else:
        profile_form = ProfileUpdateForm(instance=user)
        password_form = PasswordChangeForm(user)

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'user_obj': user,
    }
    return render(request, 'accounts/profile.html', context)

@admin_required
def admin_dashboard(request):
    today = date.today()
    total_students = Student.objects.filter(is_active=True).count()
    total_teachers = Teacher.objects.count()
    total_classes = Class.objects.count()
    total_subjects = Subject.objects.count()
    today_attendance = Attendance.objects.filter(date=today, status='present').count()

    recent_students = Student.objects.select_related('user', 'student_class').order_by('-admission_date')[:5]
    recent_results = Result.objects.select_related('student__user', 'exam__subject').order_by('-created_at')[:5]

    monthly_attendance_data = get_monthly_attendance_chart()
    class_wise_data = get_class_wise_students()

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
        'today_attendance': today_attendance,
        'recent_students': recent_students,
        'recent_results': recent_results,
        'monthly_attendance_data': monthly_attendance_data,
        'class_wise_labels': class_wise_data['labels'],
        'class_wise_counts': class_wise_data['counts'],
    }
    return render(request, 'accounts/admin_dashboard.html', context)
