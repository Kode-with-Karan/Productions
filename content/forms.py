from django import forms
from .models import Content, Collaborate

class ContentUploadForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'country', 'duration', 'genre', 'cast', 'description', 'content_type', 'file', 'thumbnail']
    
    country = forms.CharField(required=False) 
    duration = forms.CharField(required=False) 
    genre = forms.CharField(required=False) 
    cast = forms.CharField(widget=forms.Textarea, required=False)

# class ContentImageForm(forms.ModelForm):
#     images = forms.FileField(required=False)

class CollaborateUploadForm(forms.ModelForm):
    class Meta:
        model = Collaborate
        fields = ['name', 'email', 'idea_description', 'content_type']
