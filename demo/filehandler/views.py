import io
import base64
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import FileUploadForm
from .scripts import available_scripts  # Import the dictionary of available scripts

def handle_uploaded_file(file, script_type):
    if script_type in available_scripts:
        # Call the corresponding script function
        processed_data, output, filename = available_scripts[script_type](file)
        return processed_data, output, filename
    else:
        raise ValueError(f"Unknown script type: {script_type}")

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            script_type = form.cleaned_data['script_type']
            try:
                processed_data, output, filename = handle_uploaded_file(file, script_type)
                # Encode the file content in base64 before saving it in the session
                encoded_file_content = base64.b64encode(output.getvalue()).decode('utf-8')
                request.session['file_content'] = encoded_file_content
                request.session['file_name'] = filename

                # Prepare a JSON response with the processed data and a download link
                response_data = {
                    'sheets': {
                        sheet_name: {
                            'columns': df.columns.tolist(),
                            'rows': df.values.tolist()
                        }
                        for sheet_name, df in processed_data.items()
                    },
                    'download_link': '/filehandler/download/'
                }

                return JsonResponse(response_data)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Invalid form submission.'}, status=400)
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

def download_file(request):
    encoded_file_content = request.session.get('file_content')
    file_name = request.session.get('file_name')
    if encoded_file_content and file_name:
        # Decode the base64 string back to bytes
        file_content = base64.b64decode(encoded_file_content)
        response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    else:
        return HttpResponse("No file to download.", status=404)
