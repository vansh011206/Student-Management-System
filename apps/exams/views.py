from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.accounts.decorators import teacher_required, student_required
from apps.students.models import Student
from apps.academics.models import Class, Subject
from .models import Exam, Result
from .forms import ExamForm

@teacher_required
def exam_list(request):
    class_id = request.GET.get('class_id')
    exams = Exam.objects.select_related('subject', 'class_name', 'created_by').all()

    if class_id:
        exams = exams.filter(class_name_id=class_id)

    classes = Class.objects.all()

    context = {
        'exams': exams,
        'classes': classes,
        'selected_class': class_id,
    }
    return render(request, 'exams/exam_list.html', context)

@teacher_required
def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()
            messages.success(request, f'Exam "{exam.name}" created successfully!')
            return redirect('exam_list')
        else:
            messages.error(request, 'Please correct errors in the exam form.')
    else:
        form = ExamForm()

    return render(request, 'exams/create_exam.html', {'form': form})

@teacher_required
def enter_results(request, exam_id):
    exam = get_object_or_404(Exam.objects.select_related('subject', 'class_name'), id=exam_id)
    students = Student.objects.filter(
        student_class=exam.class_name,
        is_active=True
    ).select_related('user').order_by('roll_number')

    if request.method == 'POST':
        saved_count = 0
        for student in students:
            marks_val = request.POST.get(f'marks_{student.id}', '').strip()
            remark_val = request.POST.get(f'remark_{student.id}', '').strip()

            if marks_val != '':
                try:
                    marks = float(marks_val)
                    if marks > exam.total_marks:
                        marks = exam.total_marks
                    elif marks < 0:
                        marks = 0

                    Result.objects.update_or_create(
                        student=student,
                        exam=exam,
                        defaults={
                            'marks_obtained': marks,
                            'remarks': remark_val
                        }
                    )
                    saved_count += 1
                except ValueError:
                    pass

        messages.success(request, f'Results for {saved_count} students saved successfully!')
        return redirect('exam_list')

    existing_results = {
        r.student_id: r
        for r in Result.objects.filter(exam=exam)
    }

    context = {
        'exam': exam,
        'students': students,
        'existing_results': existing_results,
    }
    return render(request, 'exams/enter_results.html', context)

@student_required
def my_results(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('login')

    results = Result.objects.filter(student=student).select_related('exam', 'exam__subject').order_by('-exam__exam_date')

    if results:
        percentages = [r.percentage for r in results]
        avg_percentage = round(sum(percentages) / len(percentages), 2)
        best_result = max(results, key=lambda r: r.percentage)
        worst_result = min(results, key=lambda r: r.percentage)
        pass_count = sum(1 for r in results if r.is_pass)
        pass_rate = round((pass_count / len(results)) * 100, 1)
    else:
        avg_percentage = 0
        best_result = None
        worst_result = None
        pass_rate = 0

    chart_labels = [f"{r.exam.subject.name} ({r.exam.name})" for r in results[:8]]
    chart_data = [r.percentage for r in results[:8]]

    context = {
        'student': student,
        'results': results,
        'avg_percentage': avg_percentage,
        'best_result': best_result,
        'worst_result': worst_result,
        'pass_rate': pass_rate,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'exams/my_results.html', context)
