from django.urls import path
from . import views
urlpatterns = [
    path('', views.root_page,name='root-registration-page'),
    path('build-registration',views.build_registration_form_page,name='build-registration'),
    path('event-registration',views.event_registration_form_page,name='event-registration'),
    path('vapp-registration',views.vapp_registration_form_page,name='vapp-registration'),
    
    path('submit-event-registration',views.submit_event_registration,name='submit-event-registration'),
    path('submit-build-registration',views.submit_build_registration,name='submit-build-registration'),
    path('submit-vapp-registration',views.submit_vapp_registration,name='submit-vapp-registration'),
    
    path('send-success-mail',views.send_success_mail,name='send-success-mail'),
    
    path('success',views.success_page,name='success-page'),
    path('event-success',views.event_success,name='event-success'),
    path('build-success',views.build_success,name='build-success'),
     path('vapp-success',views.vapp_success,name='vapp-success'),

    
]
