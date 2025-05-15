from django import forms
import json
import re
from datetime import datetime


class JsonUploadForm(forms.Form):
    json_file = forms.FileField(label='JSON файл')

    def clean_json_file(self):
        json_file = self.cleaned_data.get('json_file')

        if not json_file:
            raise forms.ValidationError('Файл не предоставлен')

        if not json_file.name.endswith('.json'):
            raise forms.ValidationError('Файл должен быть в формате JSON')

        try:

            file_content = json_file.read().decode('utf-8')

            data = json.loads(file_content)


            if not isinstance(data, list):
                raise forms.ValidationError('JSON файл должен содержать список объектов')


            for item in data:
                if not isinstance(item, dict):
                    raise forms.ValidationError('Каждый элемент в JSON должен быть объектом')


                if 'name' not in item:
                    raise forms.ValidationError('Отсутствует ключ "name" в одном из элементов')

                if 'date' not in item:
                    raise forms.ValidationError('Отсутствует ключ "date" в одном из элементов')


                if len(item['name']) >= 50:
                    raise forms.ValidationError(
                        f'Поле "name" должно содержать менее 50 символов. Найдено: {len(item["name"])}')


                if len(item['name']) <= 0:
                    raise forms.ValidationError(
                         'Поле "name" должно содержать хотябы один символ.')


                date_pattern = r'^\d{4}-\d{2}-\d{2}_\d{2}:\d{2}$'
                if not re.match(date_pattern, item['date']):
                    raise forms.ValidationError(
                        f'Поле "date" должно быть в формате "YYYY-MM-DD_HH:mm". Найдено: {item["date"]}')


                try:
                    datetime.strptime(item['date'], '%Y-%m-%d_%H:%M')
                except ValueError:
                    raise forms.ValidationError(f'Невалидная дата в поле "date": {item["date"]}')


            json_file.seek(0)
            return json_file

        except json.JSONDecodeError:
            raise forms.ValidationError('Файл содержит невалидный JSON')