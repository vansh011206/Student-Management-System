# 🎓 Student Management System (SMS)

A modern, full-featured **Student Management System** built with **Django 5** and standard **HTML5/CSS3/JavaScript** styled using a custom modern design system (Bootstrap 5, FontAwesome 6, and Google Poppins typography). 

Designed to streamline school and academic institution administration, this system offers **role-based access control** for **Admins**, **Teachers**, and **Students**, complete with attendance tracking, examination grading, PDF report card generation, CSV data export, and real-time performance analytics.

---

## ✨ Features Breakdown

### 🛡️ 1. Authentication & Role-Based Access Control (RBAC)
- **Custom User Model (`CustomUser`)**: Unified account structure supporting Admin, Teacher, and Student roles with custom profiles.
- **Strict View Decorators**: Specialized access decorators (`@admin_required`, `@teacher_required`, `@student_required`) ensuring domain security across all endpoints.
- **Profile & Password Management**: Users can update personal details, phone numbers, avatars, and security credentials from their profile dashboard.

### 📊 2. Admin Portal & Real-time Analytics
- **Executive Dashboard**: Live statistical cards displaying total enrolled students, faculty teachers, academic classes, subjects, and today's attendance summary.
- **Quick Overview Cards**: Recent student registrations, recent exam result submissions, and shortcut navigation.

### 👨‍🎓 3. Student Management Subsystem
- **Student Directory**: Paginated directory with multi-field search (by name, username, or admission number) and class filtering.
- **Student Profile Management**: Full CRUD operations for student records, including roll numbers, date of birth, blood group, parent/guardian contacts, and residential addresses.
- **📄 PDF Report Card Generation**: One-click download of styled PDF report cards featuring attendance summaries and academic result transcripts (powered by `xhtml2pdf`).
- **📥 CSV Data Export**: Instant export of active student records into CSV format for external reporting.

### 👩‍🏫 4. Faculty & Teacher Management
- **Teacher Directory**: Manage faculty members with employee IDs, assigned subjects, assigned class sections, joining dates, and academic qualifications.
- **Class Teacher Assignment**: Link faculty teachers to specific academic classes for automated roll-call views.

### 📚 5. Academic Classes & Subjects Setup
- **Class Configuration**: Create and manage academic grades/sections (e.g., *Class 10-A*, *Class 11-B*).
- **Subject Association**: Configure academic subjects (e.g., *Mathematics*, *Physics*) and map them to designated classes with unique subject codes.

### 📝 6. Attendance Management Subsystem
- **Daily Roll Call**: Interactive attendance portal allowing class teachers to mark students as **Present**, **Absent**, or **Late** for any selected date.
- **Attendance Breakdown Reports**: Monthly attendance breakdown per student with automatically computed attendance percentage and performance alerts (`Good` >= 75%, `Low` < 75%).
- **Student Attendance Grid**: Visual monthly calendar view for students highlighting daily attendance status.

### 🎓 7. Examination & Results Subsystem
- **Exam Scheduling**: Create and schedule exams specifying subject, target class, exam date, total marks, and passing criteria.
- **Batch Result Entry**: Teacher portal to enter and update student marks and performance remarks in a batch interface.
- **Student Results Dashboard**: Interactive student transcript view displaying individual exam scores, pass/fail status, overall average percentage, pass rate, and subject performance breakdown.

---

## 🛠️ Technology Stack

| Layer | Technology Used |
| :--- | :--- |
| **Backend Framework** | Python 3.10+ / Django 5.x |
| **Database** | SQLite3 (Development / Production ready for PostgreSQL/MySQL) |
| **Frontend UI** | HTML5, Vanilla CSS3 (Custom Design System), JavaScript (ES6+) |
| **CSS Framework & Icons**| Bootstrap 5.3, FontAwesome 6 Pro Free Icons |
| **Typography** | Google Fonts (Poppins & Inter) |
| **Document Generation** | `xhtml2pdf`, `reportlab`, `Pillow` |

---

## 📁 Project Structure

```
Student-Management-System/
│
├── apps/
│   ├── accounts/         # Custom User Model, Authentication & RBAC views
│   ├── academics/        # Classes & Subjects models, forms, and views
│   ├── students/         # Student & Teacher directories, forms, PDF & CSV utils
│   ├── attendance/       # Roll call, attendance reports & student calendar grid
│   └── exams/            # Exam scheduling, batch grading & student result transcripts
│
├── config/               # Django project settings, WSGI/ASGI & root URL routing
├── templates/            # Django HTML templates organized by application module
├── static/               # CSS stylesheets, JavaScript files & brand assets
├── media/                # User uploaded profile pictures & uploaded media
├── manage.py             # Django management CLI entry point
└── requirements.txt      # Python dependencies list
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** and `pip` installed on your machine.

### 2. Clone Repository & Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/vansh011206/Student-Management-System.git
cd Student-Management-System

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

### 5. Seed Demo Data *(Recommended)*
Populate the database with demo classes, subjects, teachers, students, attendance logs, and exam results:
```bash
python manage.py seed_data
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --no-input
```

### 7. Launch Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to **`http://127.0.0.1:8000/`**.

---

## 🔑 Pre-Seeded Demo Credentials

If you ran `python manage.py seed_data`, you can log in using any of the following accounts (Password for all seeded users: **`Password123`**):

| Role | Username | Password | Access Rights |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `Password123` | Full access to Admin Panel, Student/Teacher CRUD, Academics configuration |
| **Teacher** | `john_teacher` | `Password123` | Access to Teacher Portal, Roll Call attendance, Exam scheduling & Grading |
| **Student** | `alex_student` | `Password123` | Access to Student Portal, Attendance calendar, Transcripts & PDF Report Card |

---

## 📄 License & Credits
Developed as an open-source Django Web Application. Feel free to customize and extend for academic or commercial use.
