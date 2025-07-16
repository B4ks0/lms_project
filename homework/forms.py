from django import forms
from .models import HomeworkSubmission

class HomeworkUploadForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Jika belum ada gambar, field wajib diisi
        if not (self.instance and self.instance.image):
            self.fields['image'].required = True
            self.fields['image'].error_messages = {
                'required': 'Silakan upload gambar tugas terlebih dahulu.'
            }
        else:
            self.fields['image'].required = False 