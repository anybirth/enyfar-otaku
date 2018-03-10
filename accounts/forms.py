from django import forms
from django.utils import timezone
from . import models

class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email', 'username', 'password', 'birthday']
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput(),
            'birthday': forms.SelectDateWidget(
                years=range(1900, timezone.now().year),
                empty_label=("年", "月", "日"),
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['email', 'username', 'password', 'birthday']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].required = True

class ActivateForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
