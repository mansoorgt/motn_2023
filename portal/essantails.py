from .models import *

def getTable(request):
    
    table_name=request.headers.get('table-name')
    if table_name == None:
        table_name=request.GET.get('table-name')
            
    if table_name=='build':
        return BuildRegistrations
    elif table_name=='event':
        return EventRegistrations
    elif table_name =='vapp':
        return VappRegistrations
    else:
        
        return BuildRegistrations 
    
def getTableRow(request):
    table_name=request.headers.get('table-name')
    if table_name == None:
        table_name=request.GET.get('table-name')
            
    if table_name=='build':
        return 'tables/table-rows/build-registrations-row.html'
    elif table_name=='event':
        return 'tables/table-rows/event-registrations-row.html'
    elif table_name =='vapp':
        return 'tables/table-rows/vapp-registrations-row.html'
    else:
        
        return 'tables/table-rows/registrations-row.html'