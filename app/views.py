import json
import random
import string
from datetime import datetime
import requests
from django.conf import settings
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from app.models import *
from .models import Subject, Branch


def home(request):
    return render(request, 'home/home.html')


def userlogout(request):
    request.session['alogin'] = False
    request.session['tlogin'] = False
    request.session['slogin'] = False
    logout(request)  # Call the built-in logout function
    request.session.flush()  # Clear the session
    return redirect('home')  # Redirect to the login page


def teacher_panel(request):
    if 'tlogin' in request.session and request.session['tlogin']:
        # Retrieve the student data from the session
        id = request.session.get('id')
        request.session['id'] = id
        print(id)
        teacher = get_object_or_404(Teacher, id=id)
    return render(request, 'teacher/teacher_dash.html', {'teacher': teacher})


def teacher_profile(request):
    if 'tlogin' in request.session and request.session['tlogin']:
        # Retrieve the student data from the session
        print("profile")
        id = request.session.get('id')

        teacher = get_object_or_404(Teacher, id=id)
        print(teacher)
    return render(request, 'teacher/teacher_profile.html', {'teacher': teacher})


def student_panel(request):
    # Check if the student is logged in
    if 'slogin' in request.session and request.session['slogin']:
        # Retrieve the student data from the session
        id = request.session.get('id')
        student = get_object_or_404(Student, id=id)
    return render(request, 'student/student_dash.html', {'student': student})


def student_profile(request):
    print("request")
    if 'slogin' in request.session and request.session['slogin']:
        print("s login")
        # Retrieve the student data from the session
        id = request.session.get('id')
        print(id)
        student = get_object_or_404(Student, id=id)
        print(student)
    return render(request, 'student/student_profile.html', {'student': student})


def admin_profile(request):
    if 'alogin' in request.session and request.session['alogin']:
        id = request.session.get('id')
        college = get_object_or_404(College, id=id)
        C_B = college.branches.all()
        print(college.image)
        return render(request, 'admin/admin_profile.html', {
            'College': college,
            'C_B': C_B
        })


def admin_panel(request):
    if 'alogin' in request.session and request.session['alogin']:
        id = request.session.get('id')
        college = get_object_or_404(College, id=id)
        return render(request, 'admin/admin_dash.html', {'Admin': college})


def login(request):
    try:
        message = ""
        if request.method == 'POST':
            email = str(request.POST.get("email")).strip()
            password = str(request.POST.get("password")).strip()
            # print(email)
            # print(password)
            role = str(request.POST.get("role")).strip()
            if role == 'College':
                college = College.objects.filter(email=email).first()
                if college.password == password and college.status == '1':
                    request.session['alogin'] = True
                    request.session['id'] = college.id
                    request.session['id'] = college.id
                    request.session['code'] = college.code
                    return redirect(admin_panel)
            elif role == 'teacher':
                print("hi")
                teacher = Teacher.objects.get(email=email)
                college = College.objects.get(code=teacher.code)
                if teacher.password == password and college.status == '1':
                    request.session['tlogin'] = True
                    request.session['id'] = teacher.id
                    return redirect(teacher_panel)
            elif role == 'student':
                student = Student.objects.get(email=email)
                college = College.objects.get(code=student.code)
                if student.password == password and college.status == '1':
                    request.session['slogin'] = True
                    request.session['id'] = student.id
                    return redirect(student_panel)
            message = 'Invalid username or password'
            return render(request, 'home/login.html', {'message': message})
        else:
            request.session['alogin'] = False
            request.session['tlogin'] = False
            request.session['slogin'] = False
            return render(request, 'home/login.html', {'message': message})
    except College.DoesNotExist:
        message = 'Invalid username or password'
    except Teacher.DoesNotExist:
        message = 'Invalid username or password'
    except Student.DoesNotExist:
        message = 'Invalid username or password'
    except Exception as ex:
        message = ex
    return render(request, 'home/login.html', {'message': message})


def add_student(request):
    try:

        teacher = Teacher.objects.get(id=request.session['id'])
        branch = teacher.branch.all()
        if 'tlogin' in request.session and request.session['tlogin']:
            message = ""
            if request.method == 'POST':
                student = Student()
                student.code = teacher.code
                student.id = datetime.now().strftime('%d%m%y%I%M%S')
                student.name = request.POST.get('name')
                student.email = request.POST.get("email")
                student.PRN = request.POST.get('PRN')
                student.mobile = request.POST.get('phone')
                student.dob = request.POST.get('dob')
                student.image = request.FILES.get('image')
                student.year = request.POST.get('year')
                student.semester = request.POST.get('semester')
                student.division = request.POST.get('division')
                student.address = request.POST.get('address')
                student.password = generate_password()
                student.save(force_insert=True)

                branch_obj = Branch.objects.get(branch=request.POST.get('branch'))
                student.branch.add(branch_obj.id)

                message = 'New student details added successfully...'
                # send_mail_user(student.email,student.password)
                return render(request, 'teacher/add_student.html', {'message': message, "branch": branch})
            else:
                return render(request, 'teacher/add_student.html', {'message': "", "branch": branch})
    except Exception as ex:
        print(ex)
    return render(request, 'teacher/add_student.html', {'message': message, "branch": branch})


def add_hod(request):
    print("add_hod")
    try:
        if 'alogin' in request.session and request.session['alogin']:
            print("valid")
            id = request.session.get('id')
            print(id)
            college = get_object_or_404(College, id=id)
            C_B = college.branches.all()
            print(C_B)
            message = ""
            if request.method == 'POST':
                print("POST")
                teacher = Teacher()
                teacher.code = request.session.get('code')
                teacher.id = datetime.now().strftime('%d%m%y%I%M%S')
                teacher.name = request.POST.get('name')
                teacher.mobile = request.POST.get('mobile')
                teacher.email = request.POST.get("email")
                teacher.post = request.POST.get('post')
                teacher.image = request.FILES.get('image')
                teacher.qualification = request.POST.get('qualification')
                teacher.experience = request.POST.get('experience')
                teacher.address = request.POST.get('address')
                teacher.password = generate_password()
                teacher.save(force_insert=True)
                print("clg save")
                if request.POST.get('post') == 'HOD':
                    branches = request.POST.get("branch")
                    print(branches)
                    teacher.branch.add(branches)
                else:
                    branches = request.POST.getlist("branches[]")
                    for branch_name in branches:
                        branch = Branch.objects.get_or_create(branch=branch_name)
                        print(branch)
                        teacher.branch.add(branch)
                message = 'New teacher details added successfully...'
                # send_mail_user(teacher.email,teacher.password)
                return render(request, 'admin/add_hod.html', {'message': message, 'branches': C_B})
            else:
                return render(request, 'admin/add_hod.html', {'message': message, 'branches': C_B})
    except Exception as ex:
        print(ex)
    return render(request, 'admin/add_hod.html', {'message': message})


def add_teacher(request):
    print("Add_teacher")
    message = ""
    try:
        if 'tlogin' in request.session and request.session['tlogin']:
            print("valid")
            id = request.session.get('id')
            print("teacher", id)
            teacher_logged_in = get_object_or_404(Teacher, id=id)
            C_B = teacher_logged_in.branch.all()
            print("branch", C_B)
            c_code = teacher_logged_in.code
            branch = C_B.first()  # or a single Branch instance
            print(type(branch))
            print(branch.id)
            print("branch-", branch)
            branch = Branch.objects.get(id=branch.id)  # or any filter
            print(branch)
            subjects = Subject.objects.filter(branches=branch)
            print(subjects)
            if request.method == 'POST':
                print("POST")

                email = request.POST.get("email")
                mobile = request.POST.get("mobile")

                # Check if teacher already exists
                existing_teacher = Teacher.objects.filter(email=email, mobile=mobile).first()

                if existing_teacher:
                    print("Existing teacher found: updating branches and subjects")

                    # Add branches
                    branch_ids = request.POST.getlist("branch")  # allow multiple branches
                    for branch_id in branch_ids:
                        branch = Branch.objects.get(id=branch_id)
                        if branch not in existing_teacher.branch.all():
                            existing_teacher.branch.add(branch)

                    # Add subjects (multi-select support)
                    subject_ids = request.POST.getlist("subject")
                    for subject_id in subject_ids:
                        subject = Subject.objects.get(id=subject_id)
                        if subject not in existing_teacher.subject.all():
                            existing_teacher.subject.add(subject)

                    message = "Existing teacher updated with new branches/subjects."
                else:
                    print("New teacher: creating entry")
                    new_teacher = Teacher()
                    new_teacher.code = c_code
                    new_teacher.id = datetime.now().strftime('%d%m%y%I%M%S')
                    new_teacher.name = request.POST.get('name')
                    new_teacher.mobile = mobile
                    new_teacher.email = email
                    new_teacher.post = request.POST.get('post')
                    new_teacher.image = request.FILES.get('image')
                    new_teacher.qualification = request.POST.get('qualification')
                    new_teacher.experience = request.POST.get('experience')
                    new_teacher.address = request.POST.get('address')
                    new_teacher.division = request.POST.get('division')
                    new_teacher.password = generate_password()
                    new_teacher.save(force_insert=True)

                    # Add branches
                    branch_ids = request.POST.getlist("branch")
                    for branch_id in branch_ids:
                        branch = Branch.objects.get(id=branch_id)
                        new_teacher.branch.add(branch)

                    # Add subjects (if Assistant Professor or any relevant post)
                    subject_ids = request.POST.getlist("subject")
                    print(subject_ids)
                    for subject_id in subject_ids:
                        subject = Subject.objects.get(id=subject_id)
                        new_teacher.subject.add(subject)
                        print("subject added")
                    message = "New teacher details added successfully."

                return render(request, 'teacher/add_teacher.html', {
                    'message': message,
                    'branches': C_B,
                    'subjects': subjects
                })

            return render(request, 'teacher/add_teacher.html', {
                'message': message,
                'branches': C_B,
                'subjects': subjects
            })

    except Exception as ex:
        print("Exception:", ex)
        message = "An error occurred. Please try again."

    return render(request, 'teacher/add_teacher.html', {
        'message': message
    })


def student_master_cc(request):
    try:
        if 'tlogin' in request.session and request.session['tlogin']:
            action = "NONE"
            id = request.session.get('id')
            teacher = get_object_or_404(Teacher, id=id)
            s_b = teacher.branch.all().first()
            a_b = teacher.branch.all()
            code = teacher.code

            if request.method == 'POST':

                bid = request.POST.get('branch_id')
                branch = Branch.objects.filter(id=bid).first()
                YEAR = request.POST.get('year')
                DIVISION = request.POST.get('div')

                if bid and DIVISION == '0' and YEAR == '0':
                    students = Student.objects.filter(code=code, branch=s_b)
                else:

                    students = Student.objects.filter(code=code, division=DIVISION, year=YEAR, branch=branch)

                if action == "Delete":
                    id_ = str(request.POST.get('id')).strip()
                    teacher = Teacher.objects.get(id=id_)
                    teacher.delete()

            else:

                students = Student.objects.filter(code=code, branch=s_b)
        return render(request, 'teacher/student_master_cc.html', {'students': students, 'b_all': a_b})
    except Exception as ex:
        return render(request, 'teacher/student_master_cc.html', {'message': ex})


def student_master(request):
    try:
        if 'alogin' in request.session and request.session['alogin']:
            b_all = Branch.objects.all()
            code = request.session.get('code')
            if request.method == 'POST':
                if request.POST.get('branch_id'):
                    bid = request.POST.get('branch_id')
                    if bid == '0':
                        branch = Branch.objects.all()
                        students = Student.objects.filter(code=code, branch__in=branch)
                    else:
                        branch = Branch.objects.filter(id=bid)
                        students = Student.objects.filter(code=code, branch__in=branch)
            else:
                branch = Branch.objects.all()
                students = Student.objects.filter(code=code, branch__in=branch)

        return render(request, 'admin/student_master.html', {'students': students, 'b_all': b_all})
    except Exception as ex:
        return render(request, 'admin/student_master.html', {'message': ex})


def teacher_master(request):
    try:
        branch = None
        b_all = None
        if 'alogin' in request.session and request.session['alogin']:
            action = "NONE"
            branch = Branch.objects.all()
            b_all = Branch.objects.all()
            code = request.session.get('code')
            if request.method == 'POST':
                if request.POST.get('branch_id'):

                    bid = request.POST.get('branch_id')
                    if bid == '0':

                        teachers = Teacher.objects.filter(code=code, branch__in=branch).exclude(post='HOD').distinct()
                    else:
                        branch = Branch.objects.filter(id=bid)
                        teachers = Teacher.objects.filter(code=code, branch__in=branch).exclude(post='HOD').distinct()

                if action == "Delete":
                    id_ = str(request.POST.get('id')).strip()
                    teacher = Teacher.objects.get(id=id_)
                    teacher.delete()

            else:
                branch = Branch.objects.all()
                teachers = Teacher.objects.filter(code=code, branch__in=branch).exclude(post='HOD')
        if 'tlogin' in request.session and request.session['tlogin']:
            id = request.session.get('id')
            teacher = Teacher.objects.get(id=id)
            print(teacher)
            teachers = Teacher.objects.filter(branch__in=teacher.branch.all()).distinct()
            print(teachers)
        return render(request, 'admin/teacher_master.html', {'teachers': teachers, 'branch': branch, 'b_all': b_all})

    except Exception as ex:
        print(ex)
        return render(request, 'admin/teacher_master.html', {'message': ex})


def hod_master(request):
    try:
        if 'alogin' in request.session and request.session['alogin']:
            print("hod show")

            if request.method == 'POST':
                id_ = str(request.POST.get('id')).strip()
                action = request.POST.get('action')
                teacher = Teacher.objects.get(id=id_)

                if action == 'Delete':
                    teacher.delete()
                elif action == 'Update':
                    print("update call")
                    request.session['tid'] = teacher.id
                    return redirect(update_hod)

            code = request.session.get('code')  # Get college code from session
            teachers = Teacher.objects.filter(code=code, post='HOD')

            return render(request, 'admin/hod_master.html', {'teachers': teachers})

        else:
            return redirect('adupdate_hodmin_login')  # redirect if session is invalid

    except Exception as ex:
        return render(request, 'admin/hod_master.html', {'message': ex})


def update_hod(request):
    print("update_hod")
    tid = request.session.get('tid')
    teacher = get_object_or_404(Teacher, id=tid)
    print("update_hod")

    try:
        if 'alogin' in request.session and request.session['alogin']:
            print("valid")

            admin_id = request.session.get('id')
            college = get_object_or_404(College, id=admin_id)
            C_B = college.branches.all()
            message = ""

            if request.method == 'POST':
                print("POST - Updating Teacher")

                teacher.name = request.POST.get('name')
                teacher.mobile = request.POST.get('mobile')
                teacher.email = request.POST.get('email')
                teacher.post = request.POST.get('post')
                teacher.qualification = request.POST.get('qualification')
                teacher.experience = request.POST.get('experience')
                teacher.address = request.POST.get('address')

                # Update image only if new one uploaded
                if request.FILES.get('image'):
                    teacher.image = request.FILES['image']

                teacher.save()

                # Update branches
                teacher.branch.clear()  # Clear existing relations

                if teacher.post == 'HOD':
                    branch_id = request.POST.get('branch')
                    if branch_id:
                        branch = Branch.objects.get(id=branch_id)
                        teacher.branch.add(branch)
                else:
                    branch_ids = request.POST.getlist('branches[]')
                    for bid in branch_ids:
                        branch = Branch.objects.get(id=bid)
                        teacher.branch.add(branch)

                message = "Teacher details updated successfully."
                return render(request, 'admin/update_hod.html', {
                    'teacher': teacher,
                    'branches': C_B,
                    'message': message
                })

            return render(request, 'admin/update_hod.html', {
                'teacher': teacher,
                'branches': C_B,
                'message': message
            })

        else:
            return redirect('admin_login')

    except Exception as ex:
        print(ex)
        return render(request, 'admin/update_hod.html', {
            'message': f"Error occurred: {ex}"
        })


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    return render(request, 'home/contact.html')


def generate_password(length=8):
    letters_digits = string.ascii_letters + string.digits
    special_chars = '#$@'

    password = random.choices(letters_digits, k=length - 1) + [random.choice(special_chars)]
    random.shuffle(password)

    return ''.join(password)


def send_mail_user(mail, password):
    try:
        context = {}

        address = mail
        subject = 'Your LMS Credentials Are Here – Student ID & Password '
        message = f"""
    Dear Student,
    Welcome to LMS!

    Your Learning Management System (LMS) credentials have been created. Please find your login details below:

    - Student ID: {mail}
    - Password: {password}
    - LMS Portal Link:https://lms-4nfs.onrender.com/

    To ensure the security of your account, please log in as soon as possible and change your password.

    If you have any issues accessing your account, please contact support at lmssystem1011@gmail.com

    Best regards.
    """

        if address and subject and message:
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                context['result'] = 'Email sent successfully'
            except Exception as e:
                context['result'] = f'Error sending email: {e}'

        else:
            context['result'] = 'All fields are required'

    except  Exception as ex:
        print(e)


def reset(request):
    try:
        message = ""

        if request.method == 'POST':
            email = request.POST.get("email", "").strip().lower()
            role = request.POST.get("role", "").strip().lower()

            if not email or not role:
                return render(request, 'home/reset.html', {'message': "Email and Role are required."})

            user = None
            if role == 'admin':
                user = College.objects.filter(email__iexact=email).first()
            elif role == 'teacher':
                user = Teacher.objects.filter(email__iexact=email).first()
            elif role == 'student':
                user = Student.objects.filter(email__iexact=email).first()

            if user:
                send_mail_user(user.email, user.password)
                message = "A password  has been sent to your email."
            else:
                message = "Invalid username or role."

        return render(request, 'home/reset.html', {'message': message})

    except Exception as ex:
        return render(request, 'home/reset.html', {'message': f"Error: {str(ex)}"})


def update_teacher_profile(request):
    try:
        message = ""
        teacher = get_object_or_404(Teacher, id=request.session.get('id'))  # Fetch the teacher instance
        if 'tlogin' in request.session and request.session['tlogin']:
            if request.method == 'POST':
                try:

                    teacher.name = request.POST.get('name', teacher.name)
                    teacher.mobile = request.POST.get('mobile', teacher.mobile)
                    teacher.email = request.POST.get("email", teacher.email)
                    teacher.qualification = request.POST.get('qualification', teacher.qualification)
                    teacher.experience = request.POST.get('experience', teacher.experience)  # Fixed key
                    teacher.address = request.POST.get('address', teacher.address)
                    teacher.image = request.FILES.get('image', teacher.image)
                    teacher.password = request.POST.get('password', teacher.password)

                    teacher.save()  # Save the updated instance
                    message = 'Teacher details updated successfully...'

                except Exception as ex:
                    message = 'An error occurred while updating the teacher details.'

            # Render the form with the current teacher data

            return render(request, 'teacher/update_teacher.html', {'teacher': teacher, 'message': message})

        # If the user is not logged in, show an error message
        message = 'You need to be logged in to update your profile.'
        return render(request, 'teacher/update_teacher.html', {'message': message, 'teacher': teacher})

    except Exception as ex:
        print(ex)


def update_student_profile(request):
    try:
        message = ""
        student = get_object_or_404(Student, id=request.session.get('id'))  # Fetch the teacher instance
        if 'slogin' in request.session and request.session['slogin']:
            if request.method == 'POST':
                try:

                    student.name = request.POST.get('name', student.name)
                    student.mobile = request.POST.get('mobile', student.mobile)
                    student.email = request.POST.get("email", student.email)
                    student.course = request.POST.get('course', student.PRN)
                    student.dob = request.POST.get('dob', student.dob)
                    student.PRN = request.POST.get('PRN', student.PRN)
                    student.address = request.POST.get('address', student.address)
                    student.image = request.FILES.get('image', student.image)
                    student.password = request.POST.get('password', student.password)

                    student.save()  # Save the updated instance
                    message = 'Student details updated successfully...'

                except Exception as ex:
                    message = 'An error occurred while updating the teacher details.'

            # Render the form with the current student data
            return render(request, 'student/student_update.html', {'student': student, 'message': message})

        # If the user is not logged in, show an error message
        message = 'You need to be logged in to update your profile.'
        return render(request, 'student/student_update.html', {'message': message, 'student': student})

    except Exception as ex:
        print(ex)


def update_admin_profile(request):
    try:
        message = ""
        college = get_object_or_404(College, id=request.session.get('id'))  # Fetch the college instance
        if 'alogin' in request.session and request.session['alogin']:
            if request.method == 'POST':
                try:

                    college.name = request.POST.get('name', college.name)
                    college.affiliation = request.POST.get('affiliation', college.affiliation)
                    college.email = request.POST.get("email", college.email)
                    college.password = request.POST.get('password', college.password)
                    college.principal = request.POST.get('principal', college.principal)
                    college.mobile = request.POST.get('mobile', college.mobile)
                    college.website = request.POST.get('website', college.website)
                    college.address = request.POST.get('address', college.address)
                    college.city = request.POST.get('city', college.address)
                    college.state = request.POST.get('state', college.address)
                    college.pincode = request.POST.get('pincode', college.address)
                    college.image = request.FILES.get('image', college.image)
                    college.save()  # Save the updated instance
                    message = 'College details updated successfully...'

                except Exception as ex:
                    message = 'An error occurred while updating the teacher details.'

            # Render the form with the current student data
            return render(request, 'admin/admin_profile_update.html', {'college': college, 'message': message})

        # If the user is not logged in, show an error message
        message = 'You need to be logged in to update your profile.'
        return render(request, 'admin/admin_profile_update.html', {'message': message, 'college': college})

    except Exception as ex:
        print(ex)


def add_notes(request):
    print("HII")
    try:
        message = ""
        # Make sure teacher is logged in and session exists
        if 'tlogin' in request.session and request.session['tlogin']:
            teacher = get_object_or_404(Teacher, id=request.session.get('id'))
            T_B = teacher.branch.all()
            if request.method == 'POST':
                try:
                    notes = Notes()
                    notes.id = datetime.now().strftime('%d%m%y%I%M%S')

                    notes.year = request.POST.get('year')
                    notes.semester = request.POST.get('semester')
                    notes.unit = request.POST.get('unit')
                    notes.subpoint = request.POST.get('subpoint')
                    notes.date = request.POST.get('date')
                    notes.c_code = teacher.code
                    notes.teacher = teacher

                    sub_id = request.POST.get('subject')
                    subject = get_object_or_404(Subject, id=sub_id)
                    br = request.POST.get('branch')
                    print("br", br)
                    notes.branch_id = br
                    notes.subject = subject

                    if 'File' in request.FILES:
                        file = request.FILES['File']
                        notes.file = file
                    else:
                        return render(request, 'teacher/add_notes.html', {
                            'message': 'Please upload a file.',
                            'error': True
                        })

                    notes.save(force_insert=True)
                    message = 'Notes uploaded successfully!'


                except Exception as ex:
                    print(f"Error saving notes: {ex}")
                    message = f'An error occurred while uploading the notes: {str(ex)}'
                    return render(request, 'teacher/add_notes.html', {'message': message, 'error': True})

            # For both GET and POST requests, render the form
            return render(request, 'teacher/add_notes.html', {
                'message': message,
                'T_B': T_B,
            })
        else:
            # Redirect to login if not logged in
            return redirect('teacher_login')  # Assuming you have a named URL pattern

    except Exception as ex:
        print(f"Exception in add_notes: {ex}")
        return render(request, 'teacher/add_notes.html', {'message': f'An error occurred: {str(ex)}', 'error': True})


def get_subjects(request):
    try:
        year = request.GET.get('year')
        semester = request.GET.get('semester')
        branch_id = request.GET.get('branch')

        # Filter by ManyToMany field (branches) + year + semester
        subjects = Subject.objects.filter(
            branches__id=branch_id,
            year=year,
            semester=semester
        ).values('id', 'name')

        return JsonResponse(list(subjects), safe=False)
    except Exception as ex:
        print(f"Error in get_subjects: {ex}")
        return JsonResponse({'error': str(ex)}, status=500)


def teacher_note_master(request):
    try:
        if 'tlogin' in request.session and request.session['tlogin']:
            if request.method == 'POST':
                if 'action' in request.POST:
                    action = request.POST['action']
                    if action == 'Delete':
                        id_ = str(request.POST.get('id')).strip()
                        note = Notes.objects.get(id=id_)
                        note.delete()

                    # elif action == 'Update':
                    #     id_ = str(request.POST.get('id')).strip()
                    #     return redirect('update_subject', id=id_)  # Redirect to the update view

            notes = Notes.objects.filter(teacher_id=request.session.get('id'))
            return render(request, 'teacher/teacher_note_master.html', {'notes': notes})

        message = 'You need to be logged in to update your profile.'
        return render(request, 'teacher/teacher_note_master.html', {'message': message})

    except Exception as ex:
        print(ex)
        return render(request, 'teacher/teacher_note_master.html', {'message': str(ex)})


#
# from django.http import HttpResponse
# import os
#
# def check_file(request):
#     file_path = os.path.join(settings.MEDIA_ROOT, 'notes', 'LMS_USECASE.pdf')
#     if os.path.exists(file_path):
#         return HttpResponse(f"File exists at: {file_path}")
#     else:
#         return HttpResponse(f"File does NOT exist at: {file_path}")
# Backend Controller Function for Student Notes Access

# Backend Controller Function for Student Notes Access

def student_notes_view(request):
    try:
        if 'slogin' in request.session and request.session['slogin']:
            # Get the current student's year from session
            student = get_object_or_404(Student, id=request.session.get('id'))
            student_year = int(student.year)
            branch = student.branch.first()
            br = branch.id
            # Store student_year in session for use in AJAX requests
            request.session['student_year'] = student_year

            if not student_year:
                return render(request, 'student/student_notes.html',
                              {'message': 'Unable to determine your academic year. Please contact support.'})

            # Filter notes based on student's year (current and previous years only)
            accessible_notes = Notes.objects.filter(year__lte=student_year, branch_id=br, c_code=student.code)

            # Apply filters
            year_filter = request.GET.get('year')
            semester_filter = request.GET.get('semester')
            # Create a filtered queryset based on selected filters
            filtered_notes = accessible_notes

            if year_filter:
                year_filter = int(year_filter)
                # Prevent accessing future years
                if year_filter > student_year:
                    return render(request, 'student/student_notes.html',
                                  {'message': 'You cannot access notes for future academic years.'})
                filtered_notes = filtered_notes.filter(year=year_filter, branch_id=br, c_code=student.code)

            if semester_filter:
                filtered_notes = filtered_notes.filter(semester=semester_filter, branch_id=br, c_code=student.code)

            # Get the available subjects based on the current year and semester filters

            # Get unique years, semesters for filters
            available_years = list(range(1, student_year + 1))
            available_semesters = Notes.objects.filter(year__lte=student_year, branch_id=br,
                                                       c_code=student.code).values_list('semester',
                                                                                        flat=True).distinct()

            context = {
                'notes': filtered_notes,
                'student_year': student_year,
                'available_years': available_years,
                'available_semesters': available_semesters,
                'current_year_filter': year_filter,
                'current_semester_filter': semester_filter,
            }

            return render(request, 'student/student_notes.html', context)

        message = 'You need to be logged in to view notes.'
        return render(request, 'home/login.html', {'message': message})

    except Exception as ex:
        print(ex)
        return render(request, 'student/student_notes.html', {'message': str(ex)})


import base64
from django.shortcuts import render
from .models import video


def student_video(request):
    print("1")
    if 'slogin' in request.session and request.session['slogin']:
        videos = video.objects.all()
        print("2")
        video_list = []
        for v in videos:
            encoded_video = base64.b64encode(v.video_data).decode('utf-8')
            video_src = f"data:video/mp4;base64,{encoded_video}"
            video_list.append({
                "title": v.v_title,
                "description": v.v_description,
                "src": video_src,
                "apps": [
                    f"Subject: {v.v_subject}",
                    f"Unit: {v.v_unit}",
                    f"Subpoint: {v.v_subtopic}",
                ]
            })
        print("3")
        return render(request, 'student/student_video.html', {'videos_json': video_list, 'videos': video_list})


def student_video(request):
    print("1")
    if 'slogin' in request.session and request.session['slogin']:
        videos = video.objects.all()
        print("2")
        video_list = []

        for v in videos:
            encoded_video = base64.b64encode(v.video_data).decode('utf-8')
            video_src = f"data:video/mp4;base64,{encoded_video}"

            video_list.append({
                "subject": v.v_subject,  # ✅ required for tree
                "unit": v.v_unit,  # ✅ required for tree
                "subpoint": v.v_subtopic,  # ✅ required for tree
                "title": v.v_title,
                "description": v.v_description,
                "src": video_src,
                "apps": [
                    f"University: {v.university}",
                    f"Branch: {v.branch}",
                    f"Subject: {v.v_subject}",
                    f"Unit: {v.v_unit}",
                    f"Subtopic: {v.v_subtopic}",
                ]
            })

        print("3")
        ai_reply = ai_content()

        return render(request, 'student/student_video.html', {
            'videos_json': video_list,
            'videos': video_list,
            'ai_reply': ai_reply
        })


def ai_content():
    ai_reply = "Error loading AI content."
    videos = video.objects.all()
    subTopic = videos.values_list('v_subtopic', flat=True).distinct()

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Generate a professional technical summary about {subTopic} in industry and technology. Structure your response as follows:\n\n**APPLICATIONS**\n• [List 3 key applications where {subTopic} is used]\n\n**USES**\n• [List 3 main purposes/benefits of {subTopic}]\n\n**EXAMPLES**\n• [List 3 specific real-world examples of {subTopic}]\n\nProvide actual content about {subTopic}, not placeholder text. Keep each bullet point concise (under 20 words). Use the exact format with ** for headings and • for bullets."
                    }
                ],
            })
        )

        if response.status_code == 200:
            data = response.json()
            ai_reply = data["choices"][0]["message"]["content"]
        else:
            ai_reply = f"API Error: Status {response.status_code}"

    except Exception as e:
        ai_reply = f"Error: {str(e)}"

    print("AI says:", ai_reply)
    return ai_reply
