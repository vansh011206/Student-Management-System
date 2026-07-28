import calendar
from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.accounts.decorators import teacher_required, student_required
from apps.students.models import Student, Teacher
from apps.academics.models import Class
from .models import Attendance

@teacher_required
def teacher_dashboard(request):
    user = request.user
    if user.is_admin():
        teacher = Teacher.objects.first()
    else:
        try:
            teacher = user.teacher_profile
        except Teacher.DoesNotExist:
            messages.error(request, "Teacher profile not found.")
            return redirect('login')

    assigned_class = teacher.assigned_class if teacher else None
    students_count = Student.objects.filter(student_class=assigned_class, is_active=True).count() if assigned_class else 0
    today = date.today()
    today_marked = Attendance.objects.filter(student__student_class=assigned_class, date=today).exists() if assigned_class else False

    context = {
        'teacher': teacher,
        'assigned_class': assigned_class,
        'students_count': students_count,
        'today_marked': today_marked,
        'today': today,
    }
    return render(request, 'accounts/teacher_dashboard.html', context)

@teacher_required
def mark_attendance(request):
    user = request.user
    classes = Class.objects.all()

    selected_class_id = request.GET.get('class_id')
    selected_date_str = request.GET.get('date', date.today().strftime('%Y-%m-%d'))

    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = date.today()

    teacher = getattr(user, 'teacher_profile', None)

    if selected_class_id:
        assigned_class = get_object_or_404(Class, id=selected_class_id)
    elif teacher and teacher.assigned_class:
        assigned_class = teacher.assigned_class
    else:
        assigned_class = classes.first()

    students = Student.objects.filter(
        student_class=assigned_class,
        is_active=True
    ).select_related('user').order_by('roll_number') if assigned_class else []

    already_marked = Attendance.objects.filter(
        student__in=students, date=selected_date
    ).exists() if students else False

    existing_attendance = {}
    if already_marked:
        existing_attendance = {
            att.student_id: att.status
            for att in Attendance.objects.filter(student__in=students, date=selected_date)
        }

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'absent')
            Attendance.objects.update_or_create(
                student=student,
                date=selected_date,
                defaults={
                    'status': status,
                    'marked_by': teacher
                }
            )
        messages.success(request, f'Attendance for {assigned_class.name} on {selected_date} saved successfully!')
        return redirect('attendance_report')

    context = {
        'students': students,
        'selected_date': selected_date,
        'already_marked': already_marked,
        'existing_attendance': existing_attendance,
        'assigned_class': assigned_class,
        'classes': classes,
        'teacher': teacher,
    }
    return render(request, 'attendance/mark_attendance.html', context)

@teacher_required
def attendance_report(request):
    user = request.user
    teacher = getattr(user, 'teacher_profile', None)

    month = int(request.GET.get('month', date.today().month))
    year  = int(request.GET.get('year', date.today().year))
    class_id = request.GET.get('class_id')

    classes = Class.objects.all()

    if class_id:
        class_obj = get_object_or_404(Class, id=class_id)
    elif teacher and teacher.assigned_class:
        class_obj = teacher.assigned_class
    else:
        class_obj = classes.first()

    students = Student.objects.filter(student_class=class_obj, is_active=True).select_related('user').order_by('roll_number') if class_obj else []

    report = []
    for student in students:
        total_days = Attendance.objects.filter(student=student, date__month=month, date__year=year).count()
        present_days = Attendance.objects.filter(student=student, date__month=month, date__year=year, status='present').count()
        absent_days = Attendance.objects.filter(student=student, date__month=month, date__year=year, status='absent').count()
        late_days = Attendance.objects.filter(student=student, date__month=month, date__year=year, status='late').count()

        percentage = round((present_days / total_days) * 100, 1) if total_days else 0
        report.append({
            'student': student,
            'total': total_days,
            'present': present_days,
            'absent': absent_days,
            'late': late_days,
            'percentage': percentage,
            'status': 'Good' if percentage >= 75 else 'Low'
        })

    months = [(i, calendar.month_name[i]) for i in range(1, 13)]

    context = {
        'report': report,
        'month': month,
        'year': year,
        'class_obj': class_obj,
        'classes': classes,
        'months': months,
        'current_year': date.today().year,
    }
    return render(request, 'attendance/report.html', context)

@student_required
def my_attendance(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('login')

    month = int(request.GET.get('month', date.today().month))
    year  = int(request.GET.get('year', date.today().year))

    attendances = Attendance.objects.filter(student=student, date__month=month, date__year=year)
    attendance_map = {att.date.day: att.status for att in attendances}

    # Generate calendar days matrix
    num_days = calendar.monthrange(year, month)[1]
    first_weekday = calendar.monthrange(year, month)[0] # 0 = Monday

    calendar_days = []
    # empty slots for padding
    for _ in range(first_weekday):
        calendar_days.append({'day': '', 'status': 'none'})

    for day in range(1, num_days + 1):
        status = attendance_map.get(day, 'not_marked')
        calendar_days.append({'day': day, 'status': status})

    total_days = Attendance.objects.filter(student=student).count()
    present_days = Attendance.objects.filter(student=student, status='present').count()
    absent_days = Attendance.objects.filter(student=student, status='absent').count()
    late_days = Attendance.objects.filter(student=student, status='late').count()
    percentage = round((present_days / total_days) * 100, 1) if total_days else 0

    months = [(i, calendar.month_name[i]) for i in range(1, 13)]

    context = {
        'student': student,
        'calendar_days': calendar_days,
        'month': month,
        'month_name': calendar.month_name[month],
        'year': year,
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'late_days': late_days,
        'percentage': percentage,
        'months': months,
    }
    return render(request, 'attendance/my_attendance.html', context)
