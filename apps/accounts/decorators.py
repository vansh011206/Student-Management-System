from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            return redirect('login')
        if not request.user.is_admin():
            messages.error(request, 'Unauthorized access. Admin privilege required.')
            if request.user.is_teacher():
                return redirect('teacher_dashboard')
            elif request.user.is_student():
                return redirect('student_dashboard')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def teacher_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            return redirect('login')
        if not (request.user.is_teacher() or request.user.is_admin()):
            messages.error(request, 'Unauthorized access. Teacher privilege required.')
            if request.user.is_student():
                return redirect('student_dashboard')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            return redirect('login')
        if not (request.user.is_student() or request.user.is_admin()):
            messages.error(request, 'Unauthorized access. Student portal only.')
            if request.user.is_teacher():
                return redirect('teacher_dashboard')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
