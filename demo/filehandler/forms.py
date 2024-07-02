from django import forms

# Define your script choices here
SCRIPT_CHOICES = [
    ('test', 'Test Script'),
    # Add more script choices here as needed
]

class FileUploadForm(forms.Form):
    file = forms.FileField()
    script_type = forms.ChoiceField(choices=SCRIPT_CHOICES)
