# views.py
import io
import base64
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .scripts import available_scripts  # Import the dictionary of available scripts

class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "upload.html"  # Replace with your template.
    success_url = "/filehandler/upload/"  # Replace with your URL or reverse().

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        script_type = form.cleaned_data['script_type']
        
        if script_type in available_scripts:
            try:
                processed_data, output, filename = available_scripts[script_type](files)
                # Encode the file content in base64 before saving it in the session
                encoded_file_content = base64.b64encode(output.getvalue()).decode('utf-8')
                self.request.session['file_content'] = encoded_file_content
                self.request.session['file_name'] = filename

                # Prepare the context for the display.html template
                context = {
                    'processed_data': processed_data,
                    'download_available': True,
                }

                return render(self.request, 'display.html', context)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'Unknown script type.'}, status=400)

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
