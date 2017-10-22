
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from applications.globals.models import ExtraInfo

from .forms import (Add_Medicine, Add_Stock, Hospital_Admission,
                    Lodge_Complaint, Request_Ambulance, Request_Appointment)
from .models import (Ambulance_request, Appointment, Complaint, Hospital_admit,
                     Stock, Stockinventory)

# views of compounder


@login_required
def approve_appointment(request):
    if request.method == 'POST':
        if 'approve' in request.POST:
            pk = request.POST.get('id')
            Appointment.objects.filter(id=pk).update(approval=True)
        if 'disapprove' in request.POST:
            pk = request.POST.get('id')
            Appointment.objects.filter(id=pk).update(approval=False)
        return HttpResponse("approved")
    else:
        template_name = 'health_center/approve_app.html'

        queryset = Appointment.objects.filter(approval=None)
        print(queryset)
        context = {"query": queryset}
        return render(request, template_name, context)


@login_required
def view_ambulance(request):
    if request.method == 'POST':
        if 'end' in request.POST:
            pk = request.POST.get('id')
            Ambulance_request.objects.filter(id=pk).update(end_date=datetime.now())
        query = Ambulance_request.objects.order_by('date_request')
        return render(request, 'health_center/view_amb.html', {'query': query})
    else:
        query = Ambulance_request.objects.order_by('date_request')
        return render(request, 'health_center/view_amb.html', {'query': query})


@login_required
def view_admissions(request):
    if request.method == 'POST':
        if 'discharge' in request.POST:
            pk = request.POST.get('id')
            Hospital_admit.objects.filter(id=pk).update(discharge_date=datetime.now())
        query = Hospital_admit.objects.order_by('admission_date')
        return render(request, 'health_center/view_admissions.html', {'query': query})
    else:
        query = Hospital_admit.objects.order_by('admission_date')
        return render(request, 'health_center/view_admissions.html', {'query': query})


@login_required
def add_hospital_admission(request):
    if request.method == 'POST':
        form = Hospital_Admission(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            doctor_id = form.cleaned_data['doctor_id']
            hospital_name = request.POST.get('hospital_name')
            admission_date = form.cleaned_data['admission_date']
            reason = request.POST.get('reason')

            Hospital_admit.objects.create(
                user_id=user_id,
                doctor_id=doctor_id,
                hospital_name=hospital_name,
                admission_date=admission_date,
                discharge_date=None,
                reason=reason
            )
            return HttpResponse("added admission successfully")
        elif form.errors:
            return HttpResponse(form.errors)
    else:
        form = Hospital_Admission
        return render(request, "health_center/hospital_admission.html", {"form": form})


@login_required
def view_complaints(request):
    if request.method == 'POST':
        if 'submit' in request.POST:
            pk = request.POST.get('id')
            feedback = request.POST.get('feedback')
            Complaint.objects.filter(id=pk).update(feedback=feedback)
        query = Complaint.objects.order_by('date')
        return render(request, 'health_center/view_com.html', {'query': query})
    else:
        query = Complaint.objects.order_by('date')
        return render(request, 'health_center/view_com.html', {'query': query})


@login_required
def add_stock(request):
    if request.method == 'POST':
        form = Add_Stock(request.POST)
        if form.is_valid():
            medicine_name = form.cleaned_data['medicine_id']
            medicine_id = (Stock.objects.get(medicine_name=medicine_name)).id
            qty = int(request.POST.get('quantity'))
            Stockinventory.objects.create(
                medicine_id=medicine_name,
                quantity=qty,
                date=datetime.now()
            )

            quantity = (Stock.objects.get(id=medicine_id)).quantity
            print(quantity)
            quantity = quantity + qty
            Stock.objects.filter(id=medicine_id).update(quantity=quantity)
            return HttpResponse("successfully updated stock")
    else:
        form = Add_Stock()
        return render(request, "health_center/add_stock.html", {"form": form})


def add_medicine(request):
    if request.method == 'POST':
        form = Add_Medicine(request.POST)
        if form.is_valid():
            quantity = int(request.POST.get('quantity'))
            medicine_name = request.POST.get('medicine_name')
            Stock.objects.create(
                medicine_name=medicine_name,
                quantity=quantity
            )
            medicine_id = Stock.objects.get(medicine_name=medicine_name)
            Stockinventory.objects.create(
                medicine_id=medicine_id,
                quantity=quantity,
                date=datetime.now()
            )
            return HttpResponse("succesfully added medicine")
    else:
        form = Add_Medicine()
        return render(request, "health_center/add_medicine.html", {"form": form})


# views of student
@login_required
def request_ambulance(request):
    if request.method == 'POST':
        form = Request_Ambulance(request.POST)
        if form.is_valid():
            user_id = ExtraInfo.objects.get(user=request.user)
            reason = request.POST.get('reason')
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            Ambulance_request.objects.create(
                user_id=user_id,
                date_request=datetime.now(),
                start_date=start_date,
                end_date=end_date,
                reason=reason
            )
            return HttpResponse("request placed successfully")
        elif form.errors:
            return HttpResponse(form.errors)
    else:
        form = Request_Ambulance()
        return render(request, "health_center/req_ambulance.html", {"form": form})


@login_required
def lodge_complaint(request):
    if request.POST:
        form = Lodge_Complaint(request.POST)
        if form.is_valid():
            user_id = ExtraInfo.objects.get(user=request.user)
            complaint = request.POST.get('complaint')
            Complaint.objects.create(
                user_id=user_id,
                complaint=complaint,
                date=datetime.now()
            )
            return HttpResponse("complaint registered successfully")
        elif form.errors:
            return HttpResponse(form.errors)
    else:
        form = Lodge_Complaint()
        return render(request, "health_center/lodge_complaint.html", {"form": form})


@login_required
def request_appointment(request):
    if request.method == 'POST':
        form = Request_Appointment(request.POST)
        if form.is_valid():
            user_id = ExtraInfo.objects.get(user=request.user)
            doctor_id = form.cleaned_data['doctor_id']
            description = request.POST.get('description')
            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']

            Appointment.objects.create(
                user_id=user_id,
                doctor_id=doctor_id,
                description=description,
                appointment_date=appointment_date,
                appointment_time=appointment_time
            )
            return HttpResponse("appointment successful")
        elif form.errors:
            return HttpResponse(form.errors)

    else:
        form = Request_Appointment()
        return render(request, 'health_center/appointment.html', {'form': form})


@login_required
def view_my_appointment(request):
    user_id = ExtraInfo.objects.get(user=request.user)
    query = Appointment.objects.filter(user_id=user_id).order_by('appointment_date_time')
    return render(request, 'health_center/view_my_appointment.html', {'query': query})


@login_required
def view_my_ambulance(request):
    user_id = ExtraInfo.objects.get(user=request.user)
    query = Ambulance_request.objects.filter(user_id=user_id).order_by('date_request')
    return render(request, 'health_center/view_my_ambulance.html', {'query': query})


@login_required
def view_my_complaint(request):
    user_id = ExtraInfo.objects.get(user=request.user)
    query = Complaint.objects.filter(user_id=user_id).order_by('date')
    return render(request, 'health_center/view_my_complaint.html', {'query': query})


@login_required
def view_my_admission(request):
    user_id = ExtraInfo.objects.get(user=request.user)
    query = Hospital_admit.objects.filter(user_id=user_id).order_by('admission_date')
    return render(request, 'health_center/view_my_admission.html', {'query': query})
