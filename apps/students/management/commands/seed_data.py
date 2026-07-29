import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from apps.accounts.models import CustomUser
from apps.academics.models import Class, Subject
from apps.students.models import Teacher, Student
from apps.attendance.models import Attendance
from apps.exams.models import Exam, Result

class Command(BaseCommand):
    help = "Seed database with realistic Indian initial EduManage data for demonstration"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding with Indian names..."))

        # 1. Create/Update Admin User
        admin_user, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Rajesh',
                'last_name': 'Sharma',
                'email': 'admin@edumanage.edu',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.first_name = 'Rajesh'
        admin_user.last_name = 'Sharma'
        admin_user.email = 'admin@edumanage.edu'
        admin_user.set_password('admin123')
        admin_user.save()
        self.stdout.write("Configured admin user (admin / admin123)")

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

        # 4. Create/Update Teachers with Indian names
        teachers_data = [
            ('teacher1', 'Dr. Sunita', 'Sharma', 'sunita@edumanage.edu', 'MATH10', 'Class 10', 'Ph.D in Applied Mathematics'),
            ('teacher2', 'Prof. Rajesh', 'Verma', 'rajesh@edumanage.edu', 'PHYS10', 'Class 10', 'M.Sc in Theoretical Physics'),
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
                    'phone': '+91 98765-43200',
                }
            )
            t_user.first_name = fname
            t_user.last_name = lname
            t_user.email = email
            t_user.phone = '+91 98765-43200'
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
            teacher.subject = subjects_objs[sub_code]
            teacher.assigned_class = classes_objs[c_name]
            teacher.qualification = qual
            teacher.save()

            teachers_objs.append(teacher)
            self.stdout.write(f"Updated teacher {uname} ({fname} {lname})")

        # 5. Create/Update Students with Indian names
        students_raw = [
            ('student1', 'Aarav', 'Sharma', 'Class 10', 101, 'A+', 'Sanjay Sharma', '+91 98765-43210', '12 Park Street, New Delhi'),
            ('student2', 'Ananya', 'Patel', 'Class 10', 102, 'B+', 'Vikram Patel', '+91 98765-43211', '45 MG Road, Mumbai'),
            ('student3', 'Rohan', 'Gupta', 'Class 10', 103, 'O+', 'Rajesh Gupta', '+91 98765-43212', '89 Ring Road, Ahmedabad'),
            ('student4', 'Isha', 'Verma', 'Class 10', 104, 'AB+', 'Alok Verma', '+91 98765-43213', '12 Civil Lines, Jaipur'),
            ('student5', 'Vihaan', 'Singh', 'Class 10', 105, 'O-', 'Manish Singh', '+91 98765-43214', '45 Model Town, Delhi'),
            ('student6', 'Diya', 'Joshi', 'Class 10', 106, 'A-', 'Ramesh Joshi', '+91 98765-43215', '77 Jubilee Hills, Hyderabad'),
            ('student7', 'Kabir', 'Reddy', 'Class 10', 107, 'B-', 'Manoj Reddy', '+91 98765-43216', '33 MG Road, Pune'),
            ('student8', 'Saisha', 'Mehta', 'Class 10', 108, 'A+', 'Jayesh Mehta', '+91 98765-43217', '90 Banjara Hills, Hyderabad'),
            ('student9', 'Arjun', 'Kapoor', 'Class 12', 201, 'O+', 'Tushar Kapoor', '+91 98765-43218', '14 Salt Lake, Kolkata'),
            ('student10', 'Kavya', 'Nair', 'Class 12', 202, 'AB-', 'Rakesh Nair', '+91 98765-43219', '67 Indiranagar, Bengaluru'),
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
            s_user.first_name = fname
            s_user.last_name = lname
            s_user.email = f"{uname}@student.edumanage.edu"
            s_user.phone = p_phone
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
            student.parent_name = p_name
            student.parent_phone = p_phone
            student.address = addr
            student.blood_group = bg
            student.save()

            students_objs.append(student)

        self.stdout.write(f"Updated {len(students_objs)} student records with Indian names.")

        # 5b. Generate Avatar Images for All Users
        import os
        from PIL import Image, ImageDraw
        os.makedirs('media/profile_pics', exist_ok=True)
        colors = [
            ('#4F46E5', '#FFFFFF'), ('#7C3AED', '#FFFFFF'), ('#059669', '#FFFFFF'),
            ('#2563EB', '#FFFFFF'), ('#D97706', '#FFFFFF'), ('#E11D48', '#FFFFFF'),
            ('#0D9488', '#FFFFFF'), ('#0891B2', '#FFFFFF'), ('#EA580C', '#FFFFFF'),
            ('#4338CA', '#FFFFFF')
        ]
        for idx, u in enumerate(CustomUser.objects.all()):
            if not u.profile_pic or u.profile_pic.name == 'default_avatar.png' or not os.path.exists(u.profile_pic.path):
                bg_color, text_color = colors[idx % len(colors)]
                img = Image.new('RGB', (160, 160), color=bg_color)
                d = ImageDraw.Draw(img)
                f_char = u.first_name[0].upper() if u.first_name else u.username[0].upper()
                l_char = u.last_name[0].upper() if u.last_name else ''
                initials = f'{f_char}{l_char}'
                d.ellipse([10, 10, 150, 150], fill=bg_color, outline='#FFFFFF', width=3)
                d.text((80, 80), initials, fill=text_color, anchor='mm', font_size=54)
                rel_path = f'profile_pics/avatar_{u.username}.png'
                img.save(os.path.join('media', rel_path))
                u.profile_pic = rel_path
                u.save()

        # 6. Generate Attendance records for the last 30 days
        today = date.today()
        primary_teacher = teachers_objs[0]
        status_choices = ['present', 'present', 'present', 'present', 'absent', 'late']

        for day_offset in range(30):
            att_date = today - timedelta(days=day_offset)
            if att_date.weekday() in [5, 6]:
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

        self.stdout.write("Created/updated attendance history.")

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

        self.stdout.write("Updated exam results.")
        self.stdout.write(self.style.SUCCESS("EduManage Indian names database seeding completed successfully!"))
