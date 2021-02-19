from django import forms
from django.contrib.auth.models import User
from .models import Profile, WorkerBiometric

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget = forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match")
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth',)

class WorkerBioEditForm(forms.ModelForm):
    picture = forms.ImageField(required = False)
    class Meta:
        model = WorkerBiometric
        fields = ('picture',)
    # def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList, label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None):
    #     super(WorkerBioEditForm, self).__init__(data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance, use_required_attribute=use_required_attribute, renderer=renderer)