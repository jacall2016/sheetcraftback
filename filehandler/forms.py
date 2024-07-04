from django import forms

SCRIPT_CHOICES = [
    ('test', 'Test Script'),
    ('compile_flip700', 'Compile Flip700 Script'),
    ('compile_yemk', 'Compile Yemk Script'),
    ('compile_phl', 'Compile Phl Script'),
    ('compile_live', 'Compile Live Script'),
    ('concatenate_analysis', 'Concatenate Analysis Script'),
    ('analysis_yemk_phl_live', 'Analysis Yemk PHL Live Script'),
    ('analysis_flip700_phl_live', 'Analysis Flip700 PHL Live Script')
]

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class FileFieldForm(forms.Form):
    file_field = MultipleFileField()
    script_type = forms.ChoiceField(choices=SCRIPT_CHOICES)
