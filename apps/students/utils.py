import random, string, io
from datetime import date
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

def generate_admission_number():
    year = date.today().year
    random_part = ''.join(random.choices(string.digits, k=4))
    return f"ADM{year}{random_part}"

def generate_employee_id():
    random_part = ''.join(random.choices(string.digits, k=5))
    return f"EMP{random_part}"

def get_monthly_attendance_chart():
    from apps.attendance.models import Attendance
    data = []
    current_year = date.today().year
    for month in range(1, 13):
        total = Attendance.objects.filter(date__year=current_year, date__month=month).count()
        present = Attendance.objects.filter(date__year=current_year, date__month=month, status='present').count()
        pct = round((present / total) * 100, 1) if total else 0
        data.append(pct)
    return data

def get_class_wise_students():
    from apps.academics.models import Class
    from apps.students.models import Student
    labels = []
    counts = []
    for cls in Class.objects.all():
        labels.append(cls.name)
        counts.append(Student.objects.filter(student_class=cls, is_active=True).count())
    return {'labels': labels, 'counts': counts}

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
