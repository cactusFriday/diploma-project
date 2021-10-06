from django import forms
from django.contrib.auth.models import User
from .models import Profile, WorkerBiometric

ph = {
    'username': 'Логин',
    'first_name': 'Имя',
    'last_name': 'Фамилия',
    'email': 'Email',
    'password': 'Пароль',
    'password2': 'Повторите пароль',
    'date_of_birth': 'Дата рождения',
}


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control mt-2'
            self.fields[field].widget.attrs['placeholder'] = ph[field]

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control mt-2'
            self.fields[field].widget.attrs['placeholder'] = ph[field]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control mt-2'
            self.fields[field].widget.attrs['placeholder'] = ph[field]

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control mt-2'
            self.fields[field].widget.attrs['placeholder'] = ph[field]

class WorkerBioEditForm(forms.ModelForm):
    picture = forms.ImageField(required = False)
    class Meta:
        model = WorkerBiometric
        fields = ('picture',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'mt-2'