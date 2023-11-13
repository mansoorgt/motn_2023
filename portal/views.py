from django.shortcuts import render ,redirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .essantails import getTable ,getTableRow
from .models import *
from django.template.loader import render_to_string
from django.core import mail 
from django.utils.html import strip_tags
from django.db.models import Q, Count

from motn_2023 import settings
import json

from django.utils import timezone
# Create your views here.


def empty_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')
######LOGIN

def login_page(request):
    return render(request,'login.html')

def validate_login(request):
    
    username=request.POST.get('username')
    password=request.POST.get('password')
    user =authenticate(username=username,password=password)
     
    if user is not None:
        login(request,user)
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})
     
    
    
    return JsonResponse({})
def logout_user(request):
    logout(request)
    return redirect('login')

#######PORTAL
@login_required
def dashboard(request):
    
  
    locations=Locations.objects.filter(active=True)
    
    dashboard_data=[]
    for loc in locations:
        event_count=EventRegistrations.objects.filter(active=True,location=loc).count()
        build_count=BuildRegistrations.objects.filter(active=True,location=loc).count()
        vapp_count=VappRegistrations.objects.filter(active=True,location=loc).count()
        total_count=sum([event_count,build_count,vapp_count])

        dashboard_data.append({'loc':loc,'event_count':event_count,'build_count':build_count,'vapp_count':vapp_count,'total_loc_count':total_count})
    
    data={'username':request.user.username,'locations':locations,'dashboard_data':dashboard_data}
    return render(request,'dashboard.html',data)
@login_required
def registrations(request):
    table=request.GET.get('table-name')
    location_id=request.GET.get('loc')
    # if table == ''
     
    locations=Locations.objects.filter(active=True)
    location_instance=locations.get(id=location_id)
    
    if table == 'build':
        
        registrations=BuildRegistrations.objects.filter(active=True,location=location_instance)
        page_path='build-registrations.html'
        cardtyes=BuildCardType.objects.filter(active=True)
    elif table == 'event':
        registrations=EventRegistrations.objects.filter(active=True,location=location_instance)
        page_path='event-registrations.html'
        cardtyes=EventCardType.objects.filter(active=True)
    elif table == 'vapp':
        registrations=VappRegistrations.objects.filter(active=True,location=location_instance)
        page_path='vapp-registrations.html'
        cardtyes=VappCardType.objects.filter(active=True)
    else:
        registrations=BuildRegistrations.objects.filter(active=True)
        page_path='build-registrations.html'
        cardtyes=BuildCardType.objects.filter(active=True)
   
    
    
    data={'username':request.user.username,'registrations':registrations,'cardtypes':cardtyes,'current_location':location_instance,'locations':locations}
    return render(request,page_path,data)


def submit_add_registrations(request):
    name=request.POST.get('name')
    company=request.POST.get('company')
    job_title=request.POST.get('job-title')
    card_type_id=request.POST.get('card-type')
    
    
    success=False
    
    try:
        cardtype_obj=EventCardType.objects.get(id=card_type_id)
        obj=BuildRegistrations.objects.create(name=name,company=company,jobtitle=job_title,cardtype=cardtype_obj)
        
        row=render_to_string('tables/table-rows/registrations-row.html',{'r':obj})
        success=True
    except Exception as e:
        row=''
        success=False
        print(e)
        
        
    data={'success':success,'row':row}
    
    return JsonResponse(data)

####### EDITS STARTS HERE
def get_registration_details(request):
    edit_id=request.GET.get('edit_id')
    
    data={'success':False}
    
    try:
        print(edit_id)
        locations=Locations.objects.filter(active=True)
        if getTable(request) == EventRegistrations:

            obj=EventRegistrations.objects.get(id=edit_id)
            cardtypes=EventCardType.objects.filter(active=True).order_by('name')
            
            modal_html=render_to_string('includes/edit-models/event-edit-modal-content.html',{"r":obj,'cardtypes':cardtypes,'locations':locations})
        elif getTable(request) == BuildRegistrations:
            obj=BuildRegistrations.objects.get(id=edit_id)
            cardtypes=BuildCardType.objects.filter(active=True).order_by('name')
            
            modal_html=render_to_string('includes/edit-models/build-edit-modal-content.html',{"r":obj,'cardtypes':cardtypes,'locations':locations})
        elif getTable(request) == VappRegistrations:
            obj=VappRegistrations.objects.get(id=edit_id)
            cardtypes=VappCardType.objects.filter(active=True)
            category=VehicleType.objects.filter(active=True)
        
            modal_html=render_to_string('includes/edit-models/vapp-edit-modal-content.html',{"r":obj,'cardtypes':cardtypes,'category':category,'locations':locations})

        data['content_html']=modal_html   
        data['success']=True 
        
    except Exception as e:
        print(e)
        data['success']=False
 
    return JsonResponse(data) 
def submit_edit_registration(request):
    # name=request.POST.get('name')
    # company=request.POST.get('company')
    # jobtitle=request.POST.get('job-title')
    # cardtype=request.POST.get('card-type')
    # edit_id=request.POST.get('edit-id')
    # print(edit_id)
    
    data={'success':False}
    try:
        if getTable(request) == EventRegistrations:
            
            first_name=request.POST.get('first-name')
            last_name=request.POST.get('last-name')
            company=request.POST.get('company')
            dob=request.POST.get('dob')
            mobile=request.POST.get('mobile')
            email=request.POST.get('email')
            nationality=request.POST.get('nationality')
            id_proof_number=request.POST.get('id-proof-number')
            
            id_proof_front=request.FILES.get('id-front-photo')
            id_proof_back=request.FILES.get('id-back-photo')
            
            badge_photo=request.FILES.get('badge-photo')
            
            location=request.POST.get('location')
            # jobtitle=request.POST.get('job-title')
            cardtype=request.POST.get('card-type')
            edit_id=request.POST.get('edit-id')
            
            
            
            print(badge_photo)
            obj=EventRegistrations.objects.filter(id=edit_id)
            obj.update(first_name=first_name,last_name=last_name,company=company,dob=dob,nationality=nationality,email=email,mobile=mobile,cardtype=cardtype,id_proof_number=id_proof_number,updated_at=timezone.now(),location=location)
            
            instance_obj=obj.first()
            if badge_photo != None:
                instance_obj.badge_photo=badge_photo
            
            if id_proof_front != None:
                instance_obj.id_proof_front=id_proof_front
            if id_proof_back != None:
                instance_obj.id_proof_back=id_proof_back
        
            instance_obj.save()
            
            
            
            row=render_to_string(getTableRow(request),{'r':obj.first()})
        
        if getTable(request) == BuildRegistrations:
        
            first_name=request.POST.get('first-name')
            last_name=request.POST.get('last-name')
            company=request.POST.get('company')
            dob=request.POST.get('dob')
            mobile=request.POST.get('mobile')
            email=request.POST.get('email')

            edit_id=request.POST.get('edit-id')
            cardtype=request.POST.get('card-type')
            
            location=request.POST.get('location')
            
            obj=BuildRegistrations.objects.filter(id=edit_id)
            obj.update(first_name=first_name,last_name=last_name,company=company,dob=dob,email=email,cardtype=cardtype,mobile=mobile,updated_at=timezone.now(),location=location)
            row=render_to_string(getTableRow(request),{'r':obj.first()})
        
        if getTable(request) == VappRegistrations:
            first_name=request.POST.get('first-name')
            last_name=request.POST.get('last-name')
            company=request.POST.get('company')
            vehicle_number=request.POST.get('vehicle_number')
            mobile=request.POST.get('mobile')
            email=request.POST.get('email')
            category=request.POST.get('vehicle-type')
            card_type=request.POST.get('card-type')
           
            vehicle_pass=request.FILES.get('vehicle-pass-photo')
            id_proof_front=request.FILES.get('id-front-photo')
            id_proof_back=request.FILES.get('id-back-photo')
            
            location=request.POST.get('location')
            
            edit_id=request.POST.get('edit-id')

            delivery_from_date=request.POST.get('from-delivery-date')
            delivery_to_date=request.POST.get('to-delivery-date')
            
            obj=VappRegistrations.objects.filter(id=edit_id)
            obj.update(first_name=first_name,last_name=last_name,company=company,vehicle_number=vehicle_number,mobile=mobile,email=email,cardtype=card_type,vehicletype=category,location=location,updated_at=timezone.now(),delivery_to_date=delivery_to_date,delivery_date=delivery_from_date)
            
            instance_obj=obj.first()
            if vehicle_pass != None:
                instance_obj.vehicle_pass=vehicle_pass
            if id_proof_front!=None:
                instance_obj.id_proof_front=id_proof_front
            if id_proof_back!=None:
                instance_obj.id_proof_back=id_proof_back
            instance_obj.save()
            
            row=render_to_string(getTableRow(request),{'r':obj.first()})
         
        data['success']=True
        data['row']=row
    except Exception as e:
        print(e)
        data['success']=False     
        
    return JsonResponse(data)

def submit_bulk_edit_registration(request):
    
    data={'success':False}
    
    try:
        ids=json.loads(request.POST.get('edit-ids'))
        cardtype_id=request.POST.get('card-type')
        company=request.POST.get('company')
        if getTable(request) == EventRegistrations:
            
            
            registrations=EventRegistrations.objects.filter(id__in=ids)
            if cardtype_id != '0':
                
                cardtype=EventCardType.objects.get(id=cardtype_id)
            
                registrations.update(cardtype=cardtype,updated_at=timezone.now())
            if company != '':
                registrations.update(company=company,updated_at=timezone.now())
        if getTable(request) == BuildRegistrations:
            
            
            registrations=BuildRegistrations.objects.filter(id__in=ids)
            if cardtype_id != '0':
                
                cardtype=BuildCardType.objects.get(id=cardtype_id)
            
                registrations.update(cardtype=cardtype,updated_at=timezone.now())
            if company != '':
                registrations.update(company=company,updated_at=timezone.now())
                
        if getTable(request) == VappRegistrations:
            
            
            registrations=VappRegistrations.objects.filter(id__in=ids)
            if cardtype_id != '0':
                
                cardtype=VappCardType.objects.get(id=cardtype_id)
            
                registrations.update(cardtype=cardtype,updated_at=timezone.now())
            if company != '':
                registrations.update(company=company,updated_at=timezone.now())
                  
        data['success']=True
    except Exception as e:
        print(e)
        data['reason']=str(e)
        data['success']=False    

    return JsonResponse(data)
###### EDITS ENDS HERE


def delete_registrtion(request):
    id=request.POST.get('id')
    
    data={'success':False}
    table=getTable(request)
    
    try:
        
        table.objects.filter(id=id).update(active=False)
        
        data['success']=True
        
    except Exception as e:
        data['success']=False
    
    return JsonResponse(data)
        
def collect_registration(request):
    id=request.POST.get('id')
    
    data={'success':False}
    
    table=getTable(request)
    try:
        obj=table.objects.filter(id=id)

        obj.update(collected=True)
        
        
        row=render_to_string(getTableRow(request),{'r':obj.first()})
        
        
        data['row']=row
        data['success']=True
        
    except Exception as e:
        data['success']=False
    
    return JsonResponse(data)

def change_remark(request):
    id=request.POST.get('id')
    content=request.POST.get('content')
    table=getTable(request)
    table.objects.filter(id=id).update(remark=content,updated_at=timezone.now())
    
    return JsonResponse({})

#changing - print count
def on_change_print_count(request):
    id=request.POST.get('id')
    method=request.POST.get('method')
    
    data={'success':False}
    table=getTable(request)
    try:
        obj=table.objects.get(id=id)
        
        if method=='plus':
            obj.print_count=obj.print_count+1
        if method =='minus':
            # print(obj.print_count)
            if obj.print_count != 0 and obj.print_count != None  and not obj.print_count < 0:
                obj.print_count=obj.print_count-1
            
        obj.save()
        # if table == BuildRegistrations
        row=render_to_string(getTableRow(request),{'r':obj})
        
        data['success']=True
        data['row']=row
    
    except Exception as e:
        
        data['success']=False
        
    return JsonResponse(data)
def on_change_bulk_print_count(request):
    ids=json.loads(request.POST.get('ids'))
    
    table=table=getTable(request)
    objs=table.objects.filter(id__in=ids)
    
    for obj in objs:
        obj.print_count=obj.print_count+1
        obj.save()
        
        
    return JsonResponse({})           
def registration_print_page(request):
    id=request.GET.get('reg-id')
    table=getTable(request)
    
    obj=table.objects.get(id=id)
    
    return render(request,f"print/{obj.cardtype.name}.html",{'registration':obj})

def submit_excel_data(request):
    list_data=json.loads(request.POST.get('data'))
    table=getTable(request)
    # print(list_data)
    instaces=[]
    for i in list_data:
        if len(i) < 4:
            print(i)
            
        try:
            
            company=i[1] if i[1] !=None else '' 
            jobtitle=i[2] if i[2] !=None else '' 
            name=i[0] if i[0] !=None else '' 
            _type=i[3] if i[3] !=None else '' 
            type=EventCardType.objects.filter(name=_type).first()
            
            
            instaces.append(table(name=i[0],company=company,jobtitle=jobtitle,cardtype=type))
        except Exception as e:
            print(i)
            print(e)
            
        
    table.objects.bulk_create(instaces)
    return JsonResponse({})

def get_profile_data(request):
    id=request.GET.get('id')
    table=getTable(request)
    
    obj=table.objects.get(id=id)

    if table == BuildRegistrations:
        profile_view_template='includes/profiles/build-profile-view.html'
    elif table == EventRegistrations:
        profile_view_template='includes/profiles/event-profile-view.html'
    elif table == VappRegistrations:
        profile_view_template='includes/profiles/vapp-profile-view.html'
    html=render_to_string(profile_view_template,{'registration':obj})

    data={'html':html}
    return JsonResponse(data) 
def change_verifcation(request):
    method=request.POST.get('method')
    id=request.POST.get('id')
    data={'success':False}
    table=getTable(request)
    try:
        obj=table.objects.get(id=id)
        obj.verification=method
        obj.save()
        
        row=render_to_string(getTableRow(request),{'r':obj})
        data['row']=row
        data['success']=True
    except Exception as e:
        data['success']=False
        data['reason']=str(e)
    return JsonResponse(data)

def print_page(request):
    table=request.GET.get('table-name')
    id=request.GET.get('reg-id')
    if table == 'build':
        
        registration=BuildRegistrations.objects.get(id=id)
        return render(request,f"print/{registration.location.name}/build_print/{registration.cardtype.name}.html",{'registration':registration})
    elif table == 'event':
        registration=EventRegistrations.objects.get(id=id)
        
        return render(request,f"print/{registration.location.name}/event_print/{registration.cardtype.name.replace('/','OR')}.html",{'registration':registration})
    elif table == 'vapp':
        registration=VappRegistrations.objects.get(id=id)
        
        # cardtyes=VappCardType.objects.filter(active=True)
        return render(request,f"print/vapp_print/{registration.cardtype.name}.html",{'registration':registration})
    else:
        registration=BuildRegistrations.objects.get(id=id)
        return render(request,f"print/{registration.location.name}/build_print/{registration.cardtype.name}.html",{'registration':registration})


def registration_bulk_print_page(request):
    ids=json.loads(request.GET.get('reg-ids'))
    table=request.GET.get('table-name')
    location_id=request.GET.get('loc')
    location_instance=Locations.objects.get(id=location_id)
    
    
    objs=getTable(request).objects.filter(id__in=ids)
    
    print(table)
    if table =='build':
        return render(request,f'print/{location_instance.name}/build_print/bulk_print.html',{'registrations':objs})

    if table =='event':
        return render(request,f'print/{location_instance.name}/event_print/bulk_print.html',{'registrations':objs})
    
    
    if table =='vapp':
        return render(request,f'print/vapp_print/bulk_print.html',{'registrations':objs})
    

def send_mail(request):
    method=request.POST.get('method')
    id=request.POST.get('id')
   
    
    if getTable(request) == EventRegistrations:
        registration=EventRegistrations.objects.get(id=id)
        uid='EVP-'+str(registration.id)
    if getTable(request) == BuildRegistrations:
        registration=BuildRegistrations.objects.get(id=id)
        uid='BUP-'+str(registration.id)
    if getTable(request) == VappRegistrations:
        registration=VappRegistrations.objects.get(id=id)
        uid='VAP-'+str(registration.id)
     
    if method == 'Approved':

      
        data={"name":registration.first_name+' '+registration.last_name,'uid':uid,'location_id':registration.location.id}
        html_contect=render_to_string("email/approved.html",data)
        email_from = settings.EMAIL_HOST_USER
        subject = 'Registration Status – Approved'
        # msg= mail.EmailMultiAlternatives(subject,'From info-events ',email_from,[registration.email])
        # msg.attach_alternative(html_contect,"text/html")
        
        mail.send_mail(subject, strip_tags(html_contect), email_from, [registration.email], html_message=html_contect,fail_silently=False)
    
    if method == 'Rejected':

        reason=request.POST.get('reason')
        print(reason)
        data={"name":registration.first_name+' '+registration.last_name,'reason':reason,'uid':uid}
        html_contect=render_to_string("email/rejected.html",data)
        email_from = settings.EMAIL_HOST_USER
        subject = 'Registration Status – Rejected'
        # msg= mail.EmailMultiAlternatives(subject,'From info-events ',email_from,[registration.email])
        # msg.attach_alternative(html_contect,"text/html")
        
        mail.send_mail(subject, strip_tags(html_contect), email_from, [registration.email], html_message=html_contect,fail_silently=False)
    
    
    return JsonResponse({})


#Get latest update 

def get_latest_data(request):
    checktime_range=[timezone.now()-timezone.timedelta(seconds=5),timezone.now()]
    # print(checktime_range)
    location=request.GET.get('loc')
    updatedQuery=getTable(request).objects.filter(updated_at__range=checktime_range,location__id=location)
    # location=Locations.objects.get(id=request.GET.get('loc'))
    # print(location.name)
    if updatedQuery.exists():
        try:
            updated_ids=updatedQuery.filter(updated_at__range=checktime_range).values_list('id',flat=True)
            updated_rows=[]
            for i in updatedQuery:
                html=render_to_string(getTableRow(request),{'r':i})
                updated_rows.append(html)
        
            data={'ids':list(updated_ids),'rows':updated_rows,'new_data':True} 
        except Exception as e:
            data={'error':str(e),'new_data':False}
        
        return JsonResponse(data)
    
    return JsonResponse({'new_data':False})


# REPORT 
def report(request):
    loc_id=request.GET.get('loc')
    location=Locations.objects.get(id=loc_id)
    report_data={}
    
    event=EventRegistrations.objects.filter(active=True,location=location)
    build=BuildRegistrations.objects.filter(active=True,location=location)
    vapp=VappRegistrations.objects.filter(active=True,location=location)
    
    report_data['event']={'total_entries':event.count(),'total_accepted':event.filter(verification='Approved').count(),'total_rejected':event.filter(verification='Rejected').count(),'total_printed_count':event.filter(print_count__gt=0).count()}
    
    report_data['build']={'total_entries':build.count(),'total_accepted':build.filter(verification='Approved').count(),'total_rejected':build.filter(verification='Rejected').count(),'total_printed_count':build.filter(print_count__gt=0).count()}
    
    report_data['vapp']={'total_entries':vapp.count(),'total_accepted':vapp.filter(verification='Approved').count(),'total_rejected':vapp.filter(verification='Rejected').count(),'total_printed_count':vapp.filter(print_count__gt=0).count()}
    
    event_categorys=[]
    for evc in EventCardType.objects.filter(active=True):
        event_categorys.append({'name':evc.name,'total_entries':event.filter(cardtype=evc).count(),'total_accepted':event.filter(cardtype=evc).filter(verification='Approved').count(),'total_rejected':event.filter(cardtype=evc).filter(verification='Rejected').count(),'total_printed_count':event.filter(cardtype=evc).filter(print_count__gt=0).count()})
    
    build_categorys=[]
    for buc in BuildCardType.objects.filter(active=True):
        build_categorys.append({'name':buc.name,'total_entries':build.filter(cardtype=buc).count(),'total_accepted':build.filter(cardtype=buc).filter(verification='Approved').count(),'total_rejected':build.filter(cardtype=buc).filter(verification='Rejected').count(),'total_printed_count':build.filter(cardtype=buc).filter(print_count__gt=0).count()})
        
    vapp_categorys=[]
    for vac in VappCardType.objects.filter(active=True):
        vapp_categorys.append({'name':vac.name,'total_entries':vapp.filter(cardtype=vac).count(),'total_accepted':vapp.filter(cardtype=vac).filter(verification='Approved').count(),'total_rejected':vapp.filter(cardtype=vac).filter(verification='Rejected').count(),'total_printed_count':vapp.filter(cardtype=vac).filter(print_count__gt=0).count()})
        
        
    report_data['event']['categorys']=event_categorys
    report_data['vapp']['categorys']=vapp_categorys
    report_data['build']['categorys']=build_categorys
    
    data={'location':location,'report_data':report_data,'locations':Locations.objects.filter(active=True)}
    return render(request,'report.html',data)

    