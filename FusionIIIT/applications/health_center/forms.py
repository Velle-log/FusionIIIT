from django import forms

class UploadTestFileForm(forms.Form):
    file=forms.FileField()
