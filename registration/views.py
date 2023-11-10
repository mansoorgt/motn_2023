from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from motn_2023 import settings
from portal.models import *
from django.template.loader import render_to_string
from django.core import mail 
from django.utils.html import strip_tags
import json
# Create your views here.
def root_page(request):
    # try:
    #     validate_email('mansoordev00@gmail.com')
    # except ValidationError as e:
    #     print("bad email, details:", e)
    # else:
    #     data={"name":'registration.first_name'+' '+'registration.last_name'}
        
    #     # html_contect=render_to_string("email/success.html",data)
    #     # email_from = settings.EMAIL_HOST_USER
    #     # subject = 'Registration Status – Pending'
    #     # msg= mail.EmailMultiAlternatives(subject,'From info-events ',email_from,['mansoordev000@gmail.com'])
    #     # msg.attach_alternative(html_contect,"text/html")
        
    #     # #mail.send_mail(subject, strip_tags(html_contect), email_from, [registration.email], html_message=html_contect,fail_silently=False)
    #     # msg.send()
    #     html_contect=render_to_string("email/success.html",data)
    #     email_from = settings.EMAIL_HOST_USER
    #     subject = 'Application Has Been Rejected !'
    #     msg= mail.EmailMultiAlternatives(subject,'From info-events ',email_from,['athulvsabu6@gmail.com','mansoorgt007@gmail.com'])
    #     msg.attach_alternative(html_contect,"text/html")
    #     msg.send()
        
    return render(request,'root-registration.html')

def build_registration_form_page(request):
    cardtypes=BuildCardType.objects.filter(active=True).order_by('name')
    event_cardtypes=EventCardType.objects.filter(active=True).order_by('name')
    locations=Locations.objects.filter(active=True).order_by('-id')
    return render(request,'build_reg.html',{'cardtypes':cardtypes,'event_cardtypes':event_cardtypes,'locations':locations})

def event_registration_form_page(request):
    cardtypes=EventCardType.objects.filter(active=True).order_by('name')
    locations=Locations.objects.filter(active=True).order_by('-id')
    return render(request,'event_reg.html',{'cardtypes':cardtypes,'locations':locations})

def vapp_registration_form_page(request):
    cardtypes=VappCardType.objects.filter(active=True).order_by('name')
    vehicletype=VehicleType.objects.filter(active=True).order_by('name')
    locations=Locations.objects.filter(active=True).order_by('-id')
    return render(request,'vapp_reg.html',{'cardtypes':cardtypes,'vehicletype':vehicletype,'locations':locations})

def submit_event_registration(request):
    
    first_name=request.POST.get('first-name')
    last_name=request.POST.get('last-name')
    mobile=request.POST.get('mobile')
    email=request.POST.get('email')
    date_of_birth=request.POST.get('date-of-birth')
    
    locations=request.POST.get('locations')
    
    company=request.POST.get('company')
    nationality=request.POST.get('nationality')
    id_proof_type=request.POST.get('id-proof-type')
    id_proof_number=request.POST.get('id-proof-number')
    id_proof_expiry=request.POST.get('id-expiry-date')

    card_type_id=request.POST.get('card-type')
    
    id_proof_front=request.FILES.get('id-proof-front-file')
    id_proof_back=request.FILES.get('id-proof-back-file')
    badge_photo=request.FILES.get('badge-photo-file')
    

     
    data={'success':False}
    try:
        
        for location in json.loads(locations):
            
            location_instance=Locations.objects.get(id=location)
            cardType=EventCardType.objects.get(id=card_type_id)
            obj=EventRegistrations.objects.create(first_name=first_name,last_name=last_name,mobile=mobile,email=email,dob=date_of_birth,id_proof_expiry=id_proof_expiry,location=location_instance,
                                            nationality=nationality,id_proof_number=id_proof_number,badge_photo=badge_photo,company=company,id_proof_type=id_proof_type,id_proof_front=id_proof_front,id_proof_back=id_proof_back,cardtype=cardType)
        data['success']=True
        data['id']=obj.id
    except Exception as e:
        data['success']=False
        data['reason']=str(e)

    return JsonResponse(data)

def submit_build_registration(request):

    first_name=request.POST.get('first-name')
    last_name=request.POST.get('last-name')
    mobile=request.POST.get('mobile')
    email=request.POST.get('email')
    date_of_birth=request.POST.get('date-of-birth')
    company=request.POST.get('company')
    nationality=request.POST.get('nationdality')
    id_proof_type=request.POST.get('id-proof-type')
    id_proof_number=request.POST.get('id-proof-number')
    id_proof_expiry=request.POST.get('id-expiry-date')

    locations=request.POST.get('locations')
    card_type_id=request.POST.get('card-type')
    
    id_proof_front=request.FILES.get('id-proof-front-file')
    id_proof_back=request.FILES.get('id-proof-back-file')
    badge_photo=request.FILES.get('badge-photo-file')
    
    event_card_type_id=request.POST.get('event-card-type')

    need_event_pass=request.POST.get('needEventPass')

    data={'success':False}
    try:
        
        buildcardType=BuildCardType.objects.get(id=card_type_id)
            
        obj=BuildRegistrations.objects.create(first_name=first_name,last_name=last_name,mobile=mobile,email=email,company=company,location=Locations.objects.get(id=4),
                                                dob=date_of_birth,cardtype=buildcardType)
        
        if need_event_pass == 'Yes':
        
            for location in json.loads(locations):
                location_instance=Locations.objects.get(id=location)
                
                EventcardType=EventCardType.objects.get(id=event_card_type_id)
                EventRegistrations.objects.create(first_name=first_name,last_name=last_name,mobile=mobile,email=email,dob=date_of_birth,id_proof_expiry=id_proof_expiry,location=location_instance,
                                                    nationality=nationality,id_proof_number=id_proof_number,badge_photo=badge_photo,company=company,id_proof_type=id_proof_type,id_proof_front=id_proof_front,id_proof_back=id_proof_back,cardtype=EventcardType)
        
        data['success']=True
        data['id']=obj.id
        
    except Exception as e:
        data['success']=False
        data['reason']=str(e)
        
    return JsonResponse(data)

def submit_vapp_registration(request):
    first_name=request.POST.get('first-name')
    last_name=request.POST.get('last-name')
    email=request.POST.get('email')
    vehicle_number=request.POST.get('vehicle-plate-number')
    mobile=request.POST.get('mobile')
    company=request.POST.get('company')
    cardtype_id=request.POST.get('card-type')
    vehicletype_id=request.POST.get('vehicle-type')
    locations=request.POST.get('locations')
    
    id_proof_front=request.FILES.get('id-proof-front-file')
    id_proof_back=request.FILES.get('id-proof-back-file')
    vehicle_pass=request.FILES.get('vehicle-pass')
    delivery_date=request.POST.get('delivery-date')

    data={'success':False}
    
    try:
        for location in json.loads(locations):
            cardtype=VappCardType.objects.get(id=cardtype_id)
            vehicletype=VehicleType.objects.get(id=vehicletype_id)
            location_instance=Locations.objects.get(id=location)
            obj=VappRegistrations.objects.create(first_name=first_name,last_name=last_name,company=company,email=email,vehicletype=vehicletype,mobile=mobile,cardtype=cardtype,id_proof_front=id_proof_front,id_proof_back=id_proof_back,vehicle_pass=vehicle_pass,vehicle_number=vehicle_number,location=location_instance,
                                            delivery_date=delivery_date)
            data['success']=True
            data['id']=obj.id
    except Exception as e:
        data['success']=False
        data['reason']=str(e)
        
    return JsonResponse(data)

def send_success_mail(request):
    id=request.POST.get('id')
    table=request.POST.get('table-name')
    
    
   
    if table == 'event':
        registration=EventRegistrations.objects.get(id=id)    
        uid='EVP-'+str(registration.id)
        
    if table == 'build':
        registration=BuildRegistrations.objects.get(id=id)    
        uid='BUP-'+str(registration.id)
    
    if table == 'vapp':
        registration=VappRegistrations.objects.get(id=id)    
        uid='VAP-'+str(registration.id)
        
    try:
        validate_email(registration.email)
    except ValidationError as e:
        print("bad email, details:", e)
    else:
        data={"name":registration.first_name+' '+registration.last_name,'uid':uid}
        html_contect=render_to_string("email/success.html",data)
        email_from = settings.EMAIL_HOST_USER
        subject = 'Registration Status – Pending'
        # msg= mail.EmailMultiAlternatives(subject,'From info-events ',email_from,[registration.email])
        # msg.attach_alternative(html_contect,"text/html")
        
        mail.send_mail(subject, strip_tags(html_contect), email_from, [registration.email], html_message=html_contect,fail_silently=False)
        # msg.send()
        #print('Succes mail sended')
    return JsonResponse({})

def build_excel_bulk_upload(request):
    final_data=json.loads(request.POST.get('final_data'))

    error_row_ids=[]
    for i in final_data:
        if validateData(i) == False:
            error_row_ids.append(i['row-id'])
    
    if len(error_row_ids) != 0:
        return JsonResponse ({'success':False,'error_rows_ids':error_row_ids}) 
    
    for data in final_data:
        
    
        buildcardType=BuildCardType.objects.get(name__icontain=data['designation'])
                
        obj=BuildRegistrations.objects.create(first_name=first_name,last_name=last_name,mobile=mobile,email=email,company=company,location=Locations.objects.get(id=4),
                                                dob=date_of_birth,cardtype=buildcardType)
    
    
    return JsonResponse({'success':True})
    
 
def validateData(data):
    print(len(data))
    if len(data) != 8:
        return False
    for key in data:
        
        if data[key] == None or data[key] == '':
            return False
    
    return True
def success_page(request):
    if request.GET.get('reg-form') == 'event':
        
        return render(request,'event_success.html')

    if request.GET.get('reg-form') == 'build':
    
        return render(request,'build_success.html')
    if request.GET.get('reg-form') == 'vapp':
    
        return render(request,'vapp_success.html')

def event_success(request):
    return render(request,'evnt_success.html')

def build_success(request):
    return render(request,'build_success.html')

def vapp_success(request):
    return render(request,'vapp_success.html')

def bulk_upload(request):
    return render(request,'bulk_upload.html')
    
    