from django import forms
from . import models

class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email', 'username', 'password']
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None

class ActivateForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
