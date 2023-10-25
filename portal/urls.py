from django.urls import path

from . import views

from .sse import SSEView
urlpatterns = [
    path('',views.empty_page,name='empty-page'),
    
    path('login',views.login_page,name='login'),
    path('validate',views.validate_login,name='validate'),
    path('logout',views.logout_user,name='logout'),
    ####portal
    
    ##dashboard
    path('dashboard',views.dashboard,name='dashboard'),
    
    
    ##registraions
    path('registrations',views.registrations,name='registrations'),
    path('submit-add-registration',views.submit_add_registrations,name='submit-add-registration'),
    path('get-registration-details',views.get_registration_details,name='get-registration-details'),
    path('submit-edit-registration',views.submit_edit_registration,name='submit-edit-registration'),
    path('delete-registration',views.delete_registrtion,name='delete-registration'),
    path('collect-registration',views.collect_registration,name='collect-registration'),
    path('change-registration-remark',views.change_remark,name='change-registration-remark'),
    
    path('on-change-print-count',views.on_change_print_count,name='on-change-print-count'),
    path('on-change-bulk-print-count',views.on_change_bulk_print_count,name='on-change-bulk-print-count'),
    path('registration-print-page',views.registration_print_page,name='registration-print-page'),
    path('registration-bulk-print-page',views.registration_bulk_print_page,name='registration-bulk-print-page'),
    path('submit-upload-excel-data',views.submit_excel_data,name='submit-upload-excel-data'),
    path('send-mail-in-portal',views.send_mail,name='send-mail-in-portal'),
    
    
    path('get-profile-data',views.get_profile_data,name='get-profile-data'),
    path('change-verification',views.change_verifcation,name='change-verification'),    
    
    path('sse', SSEView.as_view(), name='sse'),
    
    path('print-page',views.print_page,name='print-page'),
]
