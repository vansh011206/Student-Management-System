import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from apps.accounts.models import CustomUser
from apps.academics.models import Class, Subject
from apps.students.models import Teacher, Student
from apps.attendance.models import Attendance
from apps.exams.models import Exam, Result

class Command(BaseCommand):
    help = "Seed database with realistic initial EduManage data for demonstration"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        # 1. Create Admin User
        admin_user, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'System',
                'last_name': 'Administrator',
                'email': 'admin@edumanage.edu',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write("Created admin user (admin / admin123)")

        # 2. Create Classes
        classes_data = ['Class 9', 'Class 10', 'Class 11', 'Class 12']
        classes_objs = {}
        for c_name in classes_data:
            cls, _ = Class.objects.get_or_create(name=c_name)
            classes_objs[c_name] = cls

        # 3. Create Subjects
        subjects_data = [
            ('Mathematics', 'MATH10', 'Class 10'),
            ('Physics', 'PHYS10', 'Class 10'),
            ('Chemistry', 'CHEM10', 'Class 10'),
            ('English Literature', 'ENG10', 'Class 10'),
            ('Computer Science', 'CS10', 'Class 10'),
            ('Mathematics', 'MATH12', 'Class 12'),
            ('Physics', 'PHYS12', 'Class 12'),
        ]
        subjects_objs = {}
        for s_name, code, c_name in subjects_data:
            subj, _ = Subject.objects.get_or_create(
                code=code,
                defaults={'name': s_name, 'class_name': classes_objs[c_name]}
            )
            subjects_objs[code] = subj

        # 4. Create Teachers
        teachers_data = [
            ('teacher1', 'Dr. Sarah', 'Jenkins', 'sarah@edumanage.edu', 'MATH10', 'Class 10', 'Ph.D in Applied Mathematics'),
            ('teacher2', 'Prof. Robert', 'Miller', 'robert@edumanage.edu', 'PHYS10', 'Class 10', 'M.Sc in Theoretical Physics'),
        ]
        teachers_objs = []
        for uname, fname, lname, email, sub_code, c_name, qual in teachers_data:
            t_user, u_created = CustomUser.objects.get_or_create(
                username=uname,
                defaults={
                    'first_name': fname,
                    'last_name': lname,
                    'email': email,
                    'role': 'teacher',
                    'phone': '+1 555-0192',
                }
            )
            if u_created:
                t_user.set_password('pass123')
                t_user.save()

            teacher, _ = Teacher.objects.get_or_create(
                user=t_user,
                defaults={
                    'employee_id': f"EMP{random.randint(10000, 99999)}",
                    'subject': subjects_objs[sub_code],
                    'assigned_class': classes_objs[c_name],
                    'joining_date': date(2022, 1, 15),
                    'qualification': qual,
                }
            )
            teachers_objs.append(teacher)
            self.stdout.write(f"Created teacher {uname} (pass123)")

        # 5. Create Students
        students_raw = [
            ('student1', 'Alex', 'Rivera', 'Class 10', 101, 'A+', 'David Rivera', '+1 555-0101', '124 Maple Street, NY'),
            ('student2', 'Sophia', 'Chen', 'Class 10', 102, 'B+', 'Wei Chen', '+1 555-0102', '58 Park Avenue, NY'),
            ('student3', 'Ethan', 'Patel', 'Class 10', 103, 'O+', 'Rajesh Patel', '+1 555-0103', '89 Broadway Hill, NY'),
            ('student4', 'Emma', 'Watson', 'Class 10', 104, 'AB+', 'John Watson', '+1 555-0104', '12 Baker Street, NY'),
            ('student5', 'Liam', 'Davis', 'Class 10', 105, 'O-', 'Mark Davis', '+1 555-0105', '45 Pine Lane, NY'),
            ('student6', 'Olivia', 'Garcia', 'Class 10', 106, 'A-', 'Carlos Garcia', '+1 555-0106', '77 Sunset Blvd, NY'),
            ('student7', 'Noah', 'Kim', 'Class 10', 107, 'B-', 'Min Kim', '+1 555-0107', '33 Washington Sq, NY'),
            ('student8', 'Ava', 'Taylor', 'Class 10', 108, 'A+', 'James Taylor', '+1 555-0108', '90 Lincoln Rd, NY'),
            ('student9', 'Lucas', 'Brown', 'Class 12', 201, 'O+', 'Thomas Brown', '+1 555-0109', '14 Ocean Drive, NY'),
            ('student10', 'Mia', 'Wilson', 'Class 12', 202, 'AB-', 'Robert Wilson', '+1 555-0110', '67 Highland Ave, NY'),
        ]

        students_objs = []
        for uname, fname, lname, c_name, roll, bg, p_name, p_phone, addr in students_raw:
            s_user, su_created = CustomUser.objects.get_or_create(
                username=uname,
                defaults={
                    'first_name': fname,
                    'last_name': lname,
                    'email': f"{uname}@student.edumanage.edu",
                    'role': 'student',
                    'phone': p_phone,
                }
            )
            if su_created:
                s_user.set_password('pass123')
                s_user.save()

            adm_no = f"ADM2026{roll:04d}"
            student, _ = Student.objects.get_or_create(
                user=s_user,
                defaults={
                    'admission_number': adm_no,
                    'student_class': classes_objs[c_name],
                    'roll_number': roll,
                    'date_of_birth': date(2008, (roll % 12) + 1, 15),
                    'blood_group': bg,
                    'parent_name': p_name,
                    'parent_phone': p_phone,
                    'address': addr,
                    'is_active': True,
                }
            )
            students_objs.append(student)

        self.stdout.write(f"Created {len(students_objs)} students (pass123)")

        # 6. Generate Attendance records for the last 30 days
        today = date.today()
        primary_teacher = teachers_objs[0]
        status_choices = ['present', 'present', 'present', 'present', 'absent', 'late']

        for day_offset in range(30):
            att_date = today - timedelta(days=day_offset)
            if att_date.weekday() in [5, 6]: # Skip weekends
                continue

            for student in students_objs:
                status = random.choice(status_choices)
                Attendance.objects.get_or_create(
                    student=student,
                    date=att_date,
                    defaults={
                        'status': status,
                        'marked_by': primary_teacher,
                        'remark': 'Regular class' if status == 'present' else ('Medical leave' if status == 'absent' else '15 mins late')
                    }
                )

        self.stdout.write("Created attendance history for past 30 days.")

        # 7. Create Exams & Results
        exams_data = [
            ('Unit Test 1 - Mathematics', 'unit_test', 'MATH10', 'Class 10', today - timedelta(days=15), 100),
            ('Unit Test 1 - Physics', 'unit_test', 'PHYS10', 'Class 10', today - timedelta(days=10), 100),
            ('Mid Term - Mathematics', 'midterm', 'MATH10', 'Class 10', today - timedelta(days=5), 100),
        ]

        for e_name, e_type, sub_code, c_name, e_date, t_marks in exams_data:
            exam, _ = Exam.objects.get_or_create(
                name=e_name,
                subject=subjects_objs[sub_code],
                class_name=classes_objs[c_name],
                defaults={
                    'exam_type': e_type,
                    'exam_date': e_date,
                    'total_marks': t_marks,
                    'created_by': primary_teacher.user
                }
            )

            # Add results for class 10 students
            c10_students = [s for s in students_objs if s.student_class.name == 'Class 10']
            for s in c10_students:
                marks = random.randint(45, 98)
                Result.objects.get_or_create(
                    student=s,
                    exam=exam,
                    defaults={
                        'marks_obtained': float(marks),
                        'remarks': 'Good performance' if marks >= 75 else 'Needs practice'
                    }
                )

        self.stdout.write("Created exams and student result records.")
        self.stdout.write(self.style.SUCCESS("EduManage database seeding completed successfully!"))
