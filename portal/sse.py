import json
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from django.views.generic import View
import time
from .models import *
from django.utils import timezone
from django.template.loader import render_to_string
from .essantails import getTable,getTableRow
class SSEView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        # # response['Connection'] = 'keep-alive'

        def event_stream():
           
            while True:
            # for update in UpdateData.objects.all():
                
                checktime_range=[timezone.now()-timezone.timedelta(seconds=5),timezone.now()]
                # print(checktime_range)
             
                updatedQuery=getTable(request).objects.filter(updated_at__range=checktime_range,location=location)

                if updatedQuery.exists():
                    try:
                        updated_ids=updatedQuery.filter(updated_at__range=checktime_range).values_list('id',flat=True)
                        updated_rows=[]
                        for i in updatedQuery:
                            html=render_to_string(getTableRow(request),{'r':i})
                            updated_rows.append(html)
                    
                        data={'ids':list(updated_ids),'rows':updated_rows} 
                    except Exception as e:
                        data={'error':str(e)}
                    
                    yield f"data: {json.dumps(data)}\n\n"

               # yield f"data: {json.dumps({'ids':'daw'})}\n\n"
                    
                # else:
                #     yield f"data: {json.dumps({'content': 'no contect'})}\n\n"
                time.sleep(5)
        # return response
        
        response.content={'da':'da'}
        return StreamingHttpResponse(event_stream(),content_type='text/event-stream')

    
    