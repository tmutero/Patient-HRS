from django.shortcuts import render, redirect
from patient_system.forms import *
from .models import Patient, Document, Prescription
import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password

@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def list(request):
    patient_list = Patient.objects.all()
    paginator = Paginator(patient_list, 5)
    page = request.GET.get('page')
    try:
        patients = paginator.page(page)
    except PageNotAnInteger:
        patients = paginator.page(1)
    except EmptyPage:
        patients = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'patients': patients})

@login_required
def create(request):
    if request.method == 'POST':
        member = Patient(
            firstname=request.POST['firstname'],
            lastname=request.POST['lastname'],
            mobile_number=request.POST['mobile_number'],
            gender=request.POST['gender'],
            address=request.POST['address'],
            date_of_birth=request.POST['date'],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(), )
        try:
            member.full_clean()
        except ValidationError as e:
            pass
        member.save()
        messages.success(request, 'Patient was created successfully!')
        return redirect('/list')
    else:
        return render(request, 'add.html')

@login_required
def edit(request, id):
    patients = Patient.objects.get(id=id)
    
    prescription_list = Prescription.objects.filter(patient=id).order_by('-created_at')
    documents = Document.objects.filter(patient=id).order_by('-uploaded_at')[:3]
    
    context = {'patients': patients, 'prescription_list': prescription_list, 'documents': documents}
    
    return render(request, 'edit.html', context)


@login_required
def update(request, id):
    member = Patient.objects.get(id=id)
    member.firstname = request.POST['firstname']
    member.lastname = request.POST['lastname']
    member.mobile_number = request.POST['mobile_number']
    member.description = request.POST['description']
    member.address = request.POST['address']
    member.date_of_birth = request.POST['date']
    member.save()
    messages.success(request, 'Patient was updated successfully!')
    return redirect('/list')

@login_required
def delete(request, id):
    member = Patient.objects.get(id=id)
    member.delete()
    messages.warning(request, 'Patient was deleted successfully!')
    return redirect('/list')


@login_required
def fileupload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        patient_id = request.POST['patient_id']
        patients = Patient.objects.get(id=patient_id)
        document = Document(
            description=request.POST['description'],
            document=myfile.name,
            uploaded_at=datetime.datetime.now(),
            patient = patients
        )
        document.save()
        messages.success(request, 'File uploaded successfully!')
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return redirect('/list')
    else:
        documents = Document.objects.order_by('-uploaded_at')[:3]
        context = {'documents': documents}
    return render(request, 'fileupload.html', context)

def is_prescription(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def prescription(request):
    if request.method == 'POST':
        if is_prescription(request):
            patient_id = request.POST['patient_id']
            patients = Patient.objects.get(id=patient_id)
            
            data = Prescription(
                text=request.POST['text'],
                medication=request.POST['medication'],
                dosage=request.POST['dosage'],
                frequency=request.POST['frequency'],
                expiration_at = request.POST['review_date'],
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
                patient= patients
            )
            data.save()
            astr = "<html><b> you sent an ajax post request </b> <br> returned data: %s</html>" % data
            return JsonResponse({'data': 'success'})
    else:
        prescription_list = Prescription.objects.order_by('-created_at')
        context = {'prescription_list': prescription_list}
    return render(request, 'ajax.html', {'prescription_list': prescription_list})


@csrf_protect
def getprescription(request):
    if request.method == 'GET':
        if is_prescription(request):
            data = Prescription.objects.order_by('-created_at').first()
            created = data.created_at.strftime('%m-%d-%Y %H:%M:%S')
            datas = {"id": data.id, "text": data.text, "medication": data.medication, "dosage": data.dosage,
                     "frequency": data.frequency, "created_at": created,"expiration_at": data.expiration_at}
            return JsonResponse(datas)
    else:
        return JsonResponse({'data': 'failure'})


@csrf_protect
def delete_prescription(request):
    if request.method == 'GET':
        if is_prescription(request):
            id = request.GET['id']
            prescription = Prescription.objects.get(id=id)
            prescription.delete()
            return JsonResponse({'data': 'success'})
    else:
        return JsonResponse({'data': 'failure'})


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            users = User(
                username=form.cleaned_data['username'],
                password= make_password(form.cleaned_data['password1']),
                is_staff=True,
                is_active=True,
                is_superuser=True,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            try:
                users.full_clean()
            except ValidationError as e:
                pass
            users.save()
            messages.success(request, 'Patient was created successfully!')
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def register_success(request):
    return render(request, 'success.html')

@login_required
def users(request):
    users_list = User.objects.all()
    paginator = Paginator(users_list, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'users.html', {'users': users})

@login_required
def user_delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.warning(request, 'User was deleted successfully!')
    return redirect('/users')

@login_required
def changePassword(request):
    print('changepasword')
    return render(request, 'change_password.html')


@login_required
def deleteFiles(request, id, patient_id):
    file = Document.objects.get(id=id)
    file.delete()
    messages.warning(request, 'File was deleted successfully!')
    return redirect('/list')