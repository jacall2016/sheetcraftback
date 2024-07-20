import os
import io
import base64
import zipfile
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .scripts import available_scripts

@method_decorator(csrf_exempt, name='dispatch')
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

            print("Session Data Set:", self.request.session.get('file_content'), self.request.session.get('file_name'))

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

                response_data = {
                    'sheets': sheets,
                    'images': images,
                    'download_available': True,
                }
                return JsonResponse(response_data)
            else:
                if isinstance(processed_data, dict):
                    response_data = {
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
                    response_data = {
                        'columns': processed_data.columns.tolist(),
                        'rows': processed_data.values.tolist(),
                        'download_available': True,
                    }
                    
                return JsonResponse(response_data)

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
        print("No file content or file name in session.")
        return HttpResponse("No file to download.", status=404)
    
@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    response = JsonResponse({'csrfToken': csrf_token})
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Origin"] = "http://localhost:3000", "http://127.0.0.1:3000"
    return response