from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from applications.globals.models import ExtraInfo

from .models import (Ambulance_request, Appointment, Complaint, Constants,
                     Doctor, Hospital_admit, Medicine, Prescribed_medicine,
                     Prescription, Stock, Stockinventory)


@login_required
def healthcenter(request):

    if request.method == 'POST':
        if 'Submit' in request.POST:
            user_id = ExtraInfo.objects.get(user=request.user)
            doctor = request.POST.get('doctor_id')
            doctor_id = Doctor.objects.get(id=doctor)
            description = request.POST.get('description')
            date = request.POST.get('appointment_date')
            time = request.POST.get('appointment_time')
            Appointment.objects.create(
                user_id=user_id,
                doctor_id=doctor_id,
                description=description,
                appointment_date=date,
                appointment_time=time
            )
            return HttpResponseRedirect("/healthcenter")
        elif 'Submit2' in request.POST:
            user_id = ExtraInfo.objects.get(user=request.user)
            reason = request.POST.get('reason')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            Ambulance_request.objects.create(
                 user_id=user_id,
                 date_request=datetime.now(),
                 start_date=start_date,
                 end_date=end_date,
                 reason=reason
             )
            return HttpResponseRedirect("/healthcenter")

        elif 'feed' in request.POST:
            pk = request.POST.get('id')
            feedback = request.POST.get('feedback')
            Prescription.objects.filter(id=pk).update(feedback=feedback)
            return HttpResponseRedirect("/healthcenter")
        elif 'feed_com' in request.POST:
            pk = request.POST.get('id')
            feedback = request.POST.get('feedback')
            Complaint.objects.filter(id=pk).update(feedback=feedback)
            return HttpResponseRedirect("/healthcenter")
        elif 'medicine_name' in request.POST:
            quantity = int(request.POST.get('quantity'))
            medicine_id = request.POST.get('medicine_name')
            medicine = Stock.objects.get(id=medicine_id)
            Medicine.objects.create(
                medicine_id=medicine,
                quantity=quantity
            )
            data = {
                    'status': 1
                    }
            return JsonResponse(data)
        elif 'complaint' in request.POST:
            user_id = ExtraInfo.objects.get(user=request.user)
            complaint = request.POST.get('Complaint')
            Complaint.objects.create(
                user_id=user_id,
                complaint=complaint,
                date=datetime.now()
            )
            return HttpResponseRedirect("/healthcenter")
        elif 'approve' in request.POST:
            pk = request.POST.get('id')
            Appointment.objects.filter(id=pk).update(approval=True)
            return HttpResponseRedirect("/healthcenter")
        elif 'disapprove' in request.POST:
            pk = request.POST.get('id')
            Appointment.objects.filter(id=pk).update(approval=False)
            return HttpResponseRedirect("/healthcenter")
        elif 'add_stock' in request.POST:
            medicine = request.POST.get('medicine_id')
            medicine_name = Stock.objects.get(id=medicine)
            qty = int(request.POST.get('quantity'))
            Stockinventory.objects.create(
                medicine_id=medicine_name,
                quantity=qty,
                date=datetime.now()
            )
            quantity = (Stock.objects.get(id=medicine)).quantity
            quantity = quantity + qty
            Stock.objects.filter(id=medicine).update(quantity=quantity)
            return HttpResponseRedirect("/healthcenter")
        elif 'add_medicine' in request.POST:
            medicine = request.POST.get('new_medicine')
            quantity = request.POST.get('new_quantity')
            Stock.objects.create(
                medicine_name=medicine,
                quantity=quantity
            )
            medicine_id = Stock.objects.get(medicine_name=medicine)
            Stockinventory.objects.create(
                medicine_id=medicine_id,
                quantity=quantity,
                date=datetime.now()
            )
            return HttpResponseRedirect("/healthcenter")

        elif 'end' in request.POST:
            pk = request.POST.get('id')
            Ambulance_request.objects.filter(id=pk).update(end_date=datetime.now())
            return HttpResponseRedirect("/healthcenter")

        elif 'discharge' in request.POST:
            pk = request.POST.get('id')
            Hospital_admit.objects.filter(id=pk).update(discharge_date=datetime.now())
            return HttpResponseRedirect("/healthcenter")

        elif 'prescribe' in request.POST:
            user_id = request.POST.get('user')
            user = ExtraInfo.objects.get(id=user_id)
            doctor_id = request.POST.get('doctor')
            doctor = Doctor.objects.get(id=doctor_id)
            details = request.POST.get('details')
            extra_meds = request.POST.get('extra_meds')
            Prescription.objects.create(
                user_id=user,
                doctor_id=doctor,
                details=details,
                date=datetime.now(),
                extra_meds=extra_meds
            )
            query = Medicine.objects.all()
            prescribe = Prescription.objects.all().last()
            for medicine in query:
                medicine_id = medicine.medicine_id
                quantity = medicine.quantity

                Prescribed_medicine.objects.create(
                    prescription_id=prescribe,
                    medicine_id=medicine_id,
                    quantity=quantity
                )
                qty = Stock.objects.get(medicine_name=medicine_id).quantity
                qty = qty-quantity
                Stock.objects.filter(medicine_name=medicine_id).update(quantity=qty)
                Medicine.objects.all().delete()
            return HttpResponseRedirect("/healthcenter")

        elif 'admission' in request.POST:
            user = request.POST.get('user_id')
            user_id = ExtraInfo.objects.get(id=user)
            doctor = request.POST.get('doctor_id')
            doctor_id = Doctor.objects.get(id=doctor)
            admission_date = request.POST.get('admission_date')
            reason = request.POST.get('description')
            hospital_name = request.POST.get('hospital_name')
            Hospital_admit.objects.create(
                 user_id=user_id,
                 doctor_id=doctor_id,
                 hospital_name=hospital_name,
                 admission_date=admission_date,
                 discharge_date=None,
                 reason=reason
             )
            return HttpResponseRedirect("/healthcenter")
        else:
            return HttpResponse("secon")

    else:
        users = ExtraInfo.objects.all()
        doctors = Doctor.objects.all()
        user_id = ExtraInfo.objects.get(user=request.user)
        prescription = Prescription.objects.filter(user_id=user_id).order_by('-date')
        medicines = Prescribed_medicine.objects.all()
        stocks = Stock.objects.all()
        ambulances = Ambulance_request.objects.filter(user_id=user_id).order_by('-date_request')
        all_ambulances = Ambulance_request.objects.filter(user_id=user_id).order_by('-date_request')
        hospitals = Hospital_admit.objects.filter(user_id=user_id).order_by('-admission_date')
        all_hospitals = Hospital_admit.objects.all().order_by('-admission_date')
        appointments = Appointment.objects.filter(user_id=user_id).order_by('-appointment_date')
        appointments_today = Appointment.objects.filter(approval=True,
                                                        appointment_date=datetime.now())
        appointments_approve = Appointment.objects.filter(approval=None
                                                          ).order_by('-appointment_date')
        inventories = Stockinventory.objects.all().order_by('-date')
        complaints = Complaint.objects.filter(user_id=user_id).order_by('-date')
        all_complaints = Complaint.objects.all()
        ch = Constants.TIME
        return render(request, 'phcModule/phc.html',
                      {'all_hospitals': all_hospitals,
                       'all_ambulances': all_ambulances, 'appointments_today': appointments_today,
                       'ch': ch, 'inventories': inventories, 'stocks': stocks, 'users': users,
                       'doctors': doctors, 'appointments_approve': appointments_approve,
                       'all_complaints': all_complaints, 'complaints': complaints,
                       'appointments': appointments, 'hospitals': hospitals, 'medicines': medicines,
                       'prescription': prescription, 'medicines': medicines,
                       'ambulances': ambulances})
