import pandas as pd
from io import BytesIO
from django.http import HttpResponse

def create_excel(dic, filename):
   
    df = pd.DataFrame(dic)   
    buffer = BytesIO()
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer)
    
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
    
    return response
