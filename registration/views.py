from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from motn_2023 import settings
from portal.models import *
from django.template.loader import render_to_string
from django.core import mail 
from django.utils.html import strip_tags
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
    cardtypes=BuildCardType.objects.filter(active=True)
    return render(request,'build_reg.html',{'cardtypes':cardtypes})

def event_registration_form_page(request):
    cardtypes=EventCardType.objects.filter(active=True)
    return render(request,'event_reg.html',{'cardtypes':cardtypes})

def vapp_registration_form_page(request):
    cardtypes=VappCardType.objects.filter(active=True)
    vehicletype=VehicleType.objects.filter(active=True)
    return render(request,'vapp_reg.html',{'cardtypes':cardtypes,'vehicletype':vehicletype})

def submit_event_registration(request):
    
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

    card_type_id=request.POST.get('card-type')
    
    id_proof_front=request.FILES.get('id-proof-front-file')
    id_proof_back=request.FILES.get('id-proof-back-file')
    badge_photo=request.FILES.get('badge-photo-file')
    
    data={'success':False}
    try:
        cardType=EventCardType.objects.get(id=card_type_id)
        obj=EventRegistrations.objects.create(first_name=first_name,last_name=last_name,mobile=mobile,email=email,dob=date_of_birth,id_proof_expiry=id_proof_expiry,
                                        nationality=nationality,id_proof_number=id_proof_number,badge_photo=badge_photo,company=company,id_proof_type=id_proof_type,id_proof_front=id_proof_front,id_proof_back=id_proof_back,cardtype=cardType)
        data['success']=True
        data['id']=obj.id
    except Exception as e:
        data['success']=False
        data['reason']=str(e)

    return JsonResponse(data)


def submit_build_registration(request):
    print(request.POST)
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

    card_type_id=request.POST.get('card-type')
    
    id_proof_front=request.FILES.get('id-proof-front-file')
    id_proof_back=request.FILES.get('id-proof-back-file')
    badge_photo=request.FILES.get('badge-photo-file')
    
    need_event_pass=request.POST.get('needEventPass')
    
    data={'success':False}
    try:
        buildcardType=BuildCardType.objects.get(id=card_type_id)
        BuildRegistrations.objects.create(first_name=first_name,last_name=last_name,mobile=mobile,email=email,company=company,
                                          dob=date_of_birth,cardtype=buildcardType)
        if need_event_pass == 'Yes':
            EventcardType=EventCardType.objects.get(id=card_type_id)
            EventRegistrations.objects.create(first_name=first_name,last_name=last_name,mobile=mobile,email=email,dob=date_of_birth,id_proof_expiry=id_proof_expiry,
                                            nationality=nationality,id_proof_number=id_proof_number,badge_photo=badge_photo,company=company,id_proof_type=id_proof_type,id_proof_front=id_proof_front,id_proof_back=id_proof_back,cardtype=EventcardType)
        data['success']=True
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
    
    id_proof_front=request.FILES.get('id-proof-front-file')
    id_proof_back=request.FILES.get('id-proof-back-file')
    vehicle_pass=request.FILES.get('vehicle-pass')
    delivery_date=request.POST.get('delivery-date')
    print(vehicletype_id)
    data={'success':False}
    try:
        cardtype=VappCardType.objects.get(id=cardtype_id)
        vehicletype=VehicleType.objects.get(id=vehicletype_id)
        VappRegistrations.objects.create(first_name=first_name,last_name=last_name,company=company,email=email,vehicletype=vehicletype,mobile=mobile,cardtype=cardtype,id_proof_front=id_proof_front,id_proof_back=id_proof_back,vehicle_pass=vehicle_pass,vehicle_number=vehicle_number,
                                         delivery_date=delivery_date)
        data['success']=True
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
   
def success_page(request):
    return render(request,'success.html')
    