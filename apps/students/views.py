import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.accounts.decorators import admin_required, teacher_required, student_required
from apps.accounts.models import CustomUser
from apps.academics.models import Class, Subject
from .models import Student, Teacher
from .forms import StudentForm, TeacherForm
from .utils import generate_admission_number, generate_employee_id, render_to_pdf
from apps.attendance.models import Attendance
from apps.exams.models import Result

@admin_required
def student_list(request):
    query = request.GET.get('q', '').strip()
    class_filter = request.GET.get('class', '')

    students = Student.objects.select_related('user', 'student_class').filter(is_active=True)

    if query:
        students = students.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(admission_number__icontains=query) |
            Q(user__username__icontains=query)
        )

    if class_filter:
        students = students.filter(student_class_id=class_filter)

    students = students.order_by('student_class__name', 'roll_number')
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    classes = Class.objects.all()

    context = {
        'students': page_obj,
        'classes': classes,
        'query': query,
        'selected_class': class_filter,
    }
    return render(request, 'students/student_list.html', context)

@admin_required
def add_student(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        username   = request.POST.get('username', '').strip()
        email      = request.POST.get('email', '').strip()
        password   = request.POST.get('password', '').strip()
        phone      = request.POST.get('phone', '').strip()
        profile_pic = request.FILES.get('profile_pic')

        student_form = StudentForm(request.POST)

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
        elif student_form.is_valid():
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                role='student'
            )
            if profile_pic:
                user.profile_pic = profile_pic
                user.save()

            student = student_form.save(commit=False)
            student.user = user
            student.admission_number = generate_admission_number()
            student.save()

            messages.success(request, f'Student {user.get_full_name() or user.username} added successfully! (Admission: {student.admission_number})')
            return redirect('student_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        student_form = StudentForm()

    context = {
        'student_form': student_form,
    }
    return render(request, 'students/add_student.html', context)

@admin_required
def student_detail(request, student_id):
    student = get_object_or_404(Student.objects.select_related('user', 'student_class'), id=student_id)
    attendances = Attendance.objects.filter(student=student).order_by('-date')[:10]
    total_days = Attendance.objects.filter(student=student).count()
    present_days = Attendance.objects.filter(student=student, status='present').count()
    attendance_pct = round((present_days / total_days) * 100, 1) if total_days else 0

    results = Result.objects.filter(student=student).select_related('exam', 'exam__subject').order_by('-created_at')

    context = {
        'student': student,
        'recent_attendance': attendances,
        'attendance_pct': attendance_pct,
        'total_attendance_days': total_days,
        'present_days': present_days,
        'results': results,
    }
    return render(request, 'students/student_detail.html', context)

@admin_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name  = request.POST.get('last_name', '').strip()
        user.email      = request.POST.get('email', '').strip()
        user.phone      = request.POST.get('phone', '').strip()

        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES.get('profile_pic')

        password = request.POST.get('password', '').strip()
        if password:
            user.set_password(password)

        user.save()

        student_form = StudentForm(request.POST, instance=student)
        if student_form.is_valid():
            student_form.save()
            messages.success(request, f'Student {user.get_full_name() or user.username} updated successfully!')
            return redirect('student_list')
        else:
            messages.error(request, 'Error updating student details.')
    else:
        student_form = StudentForm(instance=student)

    context = {
        'student': student,
        'user_obj': user,
        'student_form': student_form,
    }
    return render(request, 'students/edit_student.html', context)

@admin_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user = student.user
    name = user.get_full_name() or user.username
    user.delete() # cascading deletes student profile
    messages.success(request, f'Student {name} was deleted successfully.')
    return redirect('student_list')

@admin_required
def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['Admission No', 'Full Name', 'Username', 'Class', 'Roll No', 'DOB', 'Blood Group', 'Parent Name', 'Parent Phone', 'Admission Date'])

    students = Student.objects.select_related('user', 'student_class').filter(is_active=True)
    for s in students:
        writer.writerow([
            s.admission_number,
            s.user.get_full_name() or s.user.username,
            s.user.username,
            s.student_class.name,
            s.roll_number,
            s.date_of_birth,
            s.blood_group,
            s.parent_name,
            s.parent_phone,
            s.admission_date
        ])
    return response

@login_required
def generate_student_pdf(request, student_id):
    student = get_object_or_404(Student.objects.select_related('user', 'student_class'), id=student_id)
    
    # Check permissions: Admin, Teacher, or the Student themselves
    if not (request.user.is_admin() or request.user.is_teacher() or (request.user.is_student() and request.user.student_profile.id == student.id)):
        messages.error(request, 'Unauthorized PDF download.')
        return redirect('root_redirect')

    results = Result.objects.filter(student=student).select_related('exam', 'exam__subject')
    total_days = Attendance.objects.filter(student=student).count()
    present_days = Attendance.objects.filter(student=student, status='present').count()
    attendance_pct = round((present_days / total_days) * 100, 1) if total_days else 0

    context = {
        'student': student,
        'results': results,
        'attendance_pct': attendance_pct,
        'total_days': total_days,
        'present_days': present_days,
    }

    pdf = render_to_pdf('students/student_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Report_Card_{student.admission_number}.pdf"
        content = f"inline; filename='{filename}'"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error generating PDF", status=500)

# Teacher Views
@admin_required
def teacher_list(request):
    query = request.GET.get('q', '').strip()
    teachers = Teacher.objects.select_related('user', 'subject', 'assigned_class').all()

    if query:
        teachers = teachers.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(qualification__icontains=query)
        )

    context = {
        'teachers': teachers,
        'query': query,
    }
    return render(request, 'students/teacher_list.html', context)

@admin_required
def add_teacher(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        username   = request.POST.get('username', '').strip()
        email      = request.POST.get('email', '').strip()
        password   = request.POST.get('password', '').strip()
        phone      = request.POST.get('phone', '').strip()
        profile_pic = request.FILES.get('profile_pic')

        teacher_form = TeacherForm(request.POST)

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
        elif teacher_form.is_valid():
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                role='teacher'
            )
            if profile_pic:
                user.profile_pic = profile_pic
                user.save()

            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.employee_id = generate_employee_id()
            teacher.save()

            messages.success(request, f'Teacher {user.get_full_name() or user.username} added successfully!')
            return redirect('teacher_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        teacher_form = TeacherForm()

    context = {
        'teacher_form': teacher_form,
    }
    return render(request, 'students/add_teacher.html', context)

@admin_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    user = teacher.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name  = request.POST.get('last_name', '').strip()
        user.email      = request.POST.get('email', '').strip()
        user.phone      = request.POST.get('phone', '').strip()

        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES.get('profile_pic')

        password = request.POST.get('password', '').strip()
        if password:
            user.set_password(password)

        user.save()

        teacher_form = TeacherForm(request.POST, instance=teacher)
        if teacher_form.is_valid():
            teacher_form.save()
            messages.success(request, f'Teacher {user.get_full_name() or user.username} updated successfully!')
            return redirect('teacher_list')
        else:
            messages.error(request, 'Error updating teacher details.')
    else:
        teacher_form = TeacherForm(instance=teacher)

    context = {
        'teacher': teacher,
        'user_obj': user,
        'teacher_form': teacher_form,
    }
    return render(request, 'students/edit_teacher.html', context)

@admin_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    user = teacher.user
    name = user.get_full_name() or user.username
    user.delete()
    messages.success(request, f'Teacher {name} was deleted successfully.')
    return redirect('teacher_list')

# Student Dashboard View
@student_required
def student_dashboard(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('login')

    results = Result.objects.filter(student=student).select_related('exam', 'exam__subject').order_by('-created_at')
    total_days = Attendance.objects.filter(student=student).count()
    present_days = Attendance.objects.filter(student=student, status='present').count()
    attendance_pct = round((present_days / total_days) * 100, 1) if total_days else 0

    if results:
        avg_percentage = sum(r.percentage for r in results) / len(results)
    else:
        avg_percentage = 0

    context = {
        'student': student,
        'attendance_pct': attendance_pct,
        'total_days': total_days,
        'present_days': present_days,
        'avg_percentage': round(avg_percentage, 1),
        'recent_results': results[:5],
    }
    return render(request, 'accounts/student_dashboard.html', context)
