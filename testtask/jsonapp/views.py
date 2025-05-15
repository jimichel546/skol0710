from django.shortcuts import render, redirect
from django.contrib import messages
import json
from datetime import datetime

from .forms import JsonUploadForm
from .models import JsonData

def upload_json(request):
    if request.method == 'POST':
        form = JsonUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = request.FILES['json_file']
            file_content = json_file.read().decode('utf-8')
            data = json.loads(file_content)


            for item in data:
                name = item['name']

                date_str = item['date']
                date_obj = datetime.strptime(date_str, '%Y-%m-%d_%H:%M')


                JsonData.objects.create(
                    name=name,
                    date=date_obj
                )

            messages.success(request, f'Успешно загружено {len(data)} записей')
            return redirect('data_list')
    else:
        form = JsonUploadForm()

    return render(request, 'jsonapp/upload.html', {'form': form})


def data_list(request):
    data = JsonData.objects.all()
    return render(request, 'jsonapp/data_list.html', {'data': data})
