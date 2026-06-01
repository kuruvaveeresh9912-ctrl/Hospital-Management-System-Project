from django.db.models import Q

from datetime import date


# Django shortcuts import
from django.shortcuts import render, redirect, get_object_or_404

# Login authentication kosam
from django.contrib.auth import authenticate, login, logout


# Used for grouping patients date-wise
from collections import defaultdict


# Login lekunte dashboard open kakudadhu
from django.contrib.auth.decorators import login_required

# Pagination kosam
from django.core.paginator import Paginator

# CSV export kosam
from django.http import HttpResponse

# CSV module
import csv

# Models import
from .models import Patient, Doctor


# ================= LOGIN FUNCTION =================

def login_user(request):

    # Form submit ayithe
    if request.method == "POST":

        # Username and password collect chestham
        username = request.POST['username']
        password = request.POST['password']

        # User authenticate chestham
        user = authenticate(request, username=username, password=password)

        # Correct credentials ayithe
        if user is not None:

            # Login chestham
            login(request, user)

            # Dashboard ki redirect
            return redirect('/patients/')

    # Login page open chestham
    return render(request, 'login.html')


# ================= LOGOUT FUNCTION =================

def logout_user(request):

    # User logout
    logout(request)

    # Login page ki redirect
    return redirect('/login/')




# ================= RECEPTION ADD PATIENT =================

@login_required
def home(request):

    # Doctors list fetch chestham
    doctors = Doctor.objects.all()

    # Form submit ayithe
    if request.method == "POST":

        booking_date = request.POST['date']

        # Same date bookings count
        today_count = Patient.objects.filter(
            date=booking_date
        ).count() + 1

        # Patient create
        patient = Patient.objects.create(

            token=today_count,

            name=request.POST['name'],
            age=request.POST['age'],
            gender=request.POST['gender'],
            phone=request.POST['phone'],
            date=booking_date,
            time=request.POST['time'],
            doctor_id=request.POST['doctor'],
            status="Pending"

        )

        # Session save
        request.session['token'] = patient.token
        request.session['patient_id'] = patient.id

        return redirect('/success/')

    # Home page render
    return render(request, 'home.html', {

        'doctors': doctors

    })




# ================= PATIENTS DASHBOARD =================


@login_required
def patients(request):

    query = request.GET.get('q', '').strip()

    all_patients = Patient.objects.all().order_by('date', 'id')

    grouped_patients = defaultdict(list)

    for patient in all_patients:
        grouped_patients[patient.date].append(patient)

    dates = list(grouped_patients.keys())

    if query:

        page_patients = []

        for patient in Patient.objects.all():

            date1 = patient.date.strftime("%Y-%m-%d")
            date2 = patient.date.strftime("%d-%m-%Y")
            date3 = patient.date.strftime("%d/%m/%Y")
            date4 = patient.date.strftime("%b %d, %Y")
            date5 = patient.date.strftime("%B %d, %Y")
            date6 = patient.date.strftime("%B")
            date7 = patient.date.strftime("%b")

            if (
            query.lower() in patient.name.lower()
            or query == str(patient.token)
            or query == str(patient.phone)
            or query.lower() == date1.lower()
            or query.lower() == date2.lower()
            or query.lower() == date3.lower()
            or query.lower() == date4.lower()
            or query.lower() == date5.lower()
            or query.lower() == date6.lower()
            or query.lower() == date7.lower()
            ):
             page_patients.append(patient)

        current_date = None
        page = 1

    else:

        page = request.GET.get('page', 1)

        if page == '' or page == 'None':
            page = 1

        page = int(page)

        if page > len(dates):
            page = 1

        if page < 1:
            page = 1

        current_date = dates[page - 1]
        page_patients = grouped_patients[current_date]

    total_patients = Patient.objects.count()

    male_patients = Patient.objects.filter(
        gender="Male"
    ).count()

    female_patients = Patient.objects.filter(
        gender="Female"
    ).count()

    context = {
        'patients': page_patients,
        'current_date': current_date,
        'page': page,
        'total_pages': len(dates),

        'total_patients': total_patients,
        'male_patients': male_patients,
        'female_patients': female_patients,

        'query': query,
    }

    return render(
        request,
        'patients.html',
        context
    )






# ================= EDIT PATIENT =================

@login_required
def edit_patient(request, id):
    
    page = request.GET.get('page', 1)

    # Particular patient fetch chestham
    patient = get_object_or_404(Patient, id=id)

    # Doctors fetch chestham
    doctors = Doctor.objects.all()

    # Form submit ayithe
    if request.method == "POST":

        # Updated values assign chestham
        patient.name = request.POST['name']
        patient.age = request.POST['age']
        patient.gender = request.POST['gender']
        patient.phone = request.POST['phone']
        patient.date = request.POST['date']
        patient.time = request.POST['time']

        # Doctor update
        patient.doctor = Doctor.objects.get(id=request.POST['doctor'])

        # Status update
        patient.status = request.POST['status']

        # Save changes
        patient.save()

        # Dashboard ki redirect
    
        page = request.GET.get('page', 1)

        if page == '':
         page = 1
    
        return redirect(f'/patients/?page={page}')
    # Edit page render
    return render(request, 'edit.html', {

        'patient': patient,
        'doctors': doctors,
            'page': page
    
    })


# ================= DELETE PATIENT =================

@login_required
def delete_patient(request, id):

    # Patient fetch chestham
    patient = get_object_or_404(Patient, id=id)

    # Delete chestham
    patient.delete()

    # Dashboard redirect
    page = request.GET.get('page', 1)

    if page == '':
     page = 1
    return redirect(f'/patients/?page={page}')

# ================= EXPORT CSV =================

@login_required
def export_csv(request):

    # CSV response create chestham
    response = HttpResponse(content_type='text/csv')

    # CSV file name
    response['Content-Disposition'] = 'attachment; filename="patients.csv"'

    # CSV writer create chestham
    writer = csv.writer(response)

    # Heading row
    writer.writerow([

        'Name',
        'Age',
        'Gender',
        'Phone',
        'Date',
        'Time',
        'Doctor',
        'Status'

    ])

    search = request.GET.get('q')

    patients = Patient.objects.all()

    if search:

     patients = patients.filter(

        name__icontains=search

    ) | Patient.objects.filter(

        phone__icontains=search

    ) | Patient.objects.filter(

        token__icontains=search

    ) | Patient.objects.filter(

        date__icontains=search

    )

    # Row by row data write chestham
    for patient in patients:

        writer.writerow([

            patient.name,
            patient.age,
            patient.gender,
            patient.phone,
            patient.date,
            patient.time,
            patient.doctor.name,
            patient.status

        ])

    # CSV return chestham
    return response




# ================= PUBLIC BOOKING =================

def public_booking(request):

    # Doctors fetch chestham
    doctors = Doctor.objects.all()

    # Form submit ayithe
    if request.method == "POST":

        # Same date ki token count
        today_count = Patient.objects.filter(
            date=request.POST['date']
        ).count() + 1

        # Patient create chestham
        patient = Patient.objects.create(

            token=today_count,

            name=request.POST['name'],
            age=request.POST['age'],
            gender=request.POST['gender'],
            phone=request.POST['phone'],
            date=request.POST['date'],
            time=request.POST['time'],
            doctor_id=request.POST['doctor'],
            status="Pending"

        )

        # Token session lo save chestham
        request.session['token'] = today_count

        # Patient id save chestham
        request.session['patient_id'] = patient.id

        # Success page ki redirect
        return redirect('/success/')

    # Booking page render
    return render(request, 'book.html', {

        'doctors': doctors

    })



# ================= SUCCESS PAGE =================

from datetime import date, timedelta

def success(request):

    patient_id = request.session.get('patient_id')

    patient = Patient.objects.get(id=patient_id)

    booking_date = patient.date
    today = date.today()

    # Day text
    if booking_date == today:
        day_text = "Today"

    elif booking_date == today + timedelta(days=1):
        day_text = "Tomorrow"

    else:
        day_text = booking_date.strftime("%A")

    context = {

        'patient': patient,
        'token': patient.token,
        'day_text': day_text,
        'current_page': request.session.get('current_page'),

    }

    return render(request, 'success.html', context)


# ================= THANK YOU PAGE =================

def thank_you(request):

    # Thank you page render
    return render(request, 'thankyou.html')

def index(request):

    return render(request, 'index.html')