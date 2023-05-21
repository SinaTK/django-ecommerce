from django import forms

class UploadObj(forms.Form):
    file_name = forms.CharField(max_length=250, widget=forms.TextInput({'placeholder':'file addres/file name'}))
    bucket_file_name = forms.CharField(max_length=20, required=False, widget=forms.TextInput({'placeholder':'filename.format (optional)'}) )