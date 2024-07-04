import os
import io
import base64
import zipfile
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .scripts import available_scripts

class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "upload.html"
    success_url = "/"

    def form_valid(self, form):
        files = form.cleaned_data['file_field']
        script_type = form.cleaned_data['script_type']

        if script_type not in available_scripts:
            return JsonResponse({'error': 'Invalid script type.'}, status=400)

        try:
            if script_type == 'test':
                processed_data, output, filename = available_scripts[script_type](files[0].read())
            elif script_type in ['analysis_yemk_phl_live', 'analysis_flip700_phl_live']:
                output, filename = available_scripts[script_type](files[0].read())
            elif script_type in ['compile_flip700', 'compile_yemk', 'compile_phl', 'compile_live', 'concatenate_analysis']:
                processed_data, output, filename = available_scripts[script_type](files)
            else:
                processed_data, output, filename = available_scripts[script_type](files[0].read())

            encoded_file_content = base64.b64encode(output.getvalue()).decode('utf-8')
            self.request.session['file_content'] = encoded_file_content
            self.request.session['file_name'] = filename

            if script_type in ['analysis_yemk_phl_live', 'analysis_flip700_phl_live']:
                zip_file = zipfile.ZipFile(io.BytesIO(output.getvalue()))
                sheets = {}
                images = []
                for name in zip_file.namelist():
                    if name.endswith('.xlsx'):
                        with zip_file.open(name) as f:
                            df = pd.read_excel(f)
                            sheet_name = os.path.basename(name)
                            sheets[sheet_name] = {
                                'columns': df.columns.tolist(),
                                'rows': df.values.tolist()
                            }
                    elif name.startswith('images/'):
                        images.append(name)

                context = {
                    'sheets': sheets,
                    'images': images,
                    'download_available': True,
                }
                return render(self.request, 'analysis_display.html', context)
            else:
                if isinstance(processed_data, dict):
                    context = {
                        'sheets': {
                            sheet_name: {
                                'columns': df['columns'] if 'columns' in df else df.columns.tolist(),
                                'rows': df['rows'] if 'rows' in df else df.values.tolist()
                            }
                            for sheet_name, df in processed_data.items()
                        },
                        'download_available': True,
                    }
                else:
                    context = {
                        'columns': processed_data.columns.tolist(),
                        'rows': processed_data.values.tolist(),
                        'download_available': True,
                    }

                return render(self.request, 'display.html', context)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

def download_file(request):
    encoded_file_content = request.session.get('file_content')
    file_name = request.session.get('file_name')
    if encoded_file_content and file_name:
        file_content = base64.b64decode(encoded_file_content)
        response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    else:
        return HttpResponse("No file to download.", status=404)
