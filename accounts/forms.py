from django import forms
from accounts.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['phone_number', 'email', 'full_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Password aren't equal")
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='You can change password using<a href="../password/">this form</a>')

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'full_name', 'password', 'last_login', 'is_active']

class UserRegisterForm(forms.Form):
    email = forms.EmailField(max_length=255)
    full_name = forms.CharField(max_length=100, label='full name')
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email already used')
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(str(phone_number)) != 11 or str(phone_number)[0:2] != '09':
            raise ValidationError('Invalid phone number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('This phone number already used')
        return phone_number
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password2'] and cd['password'] != cd['password2']:
            raise ValidationError("Password aren't equal")
        return cd['password2']


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()
    
class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(str(phone_number)) != 11 or str(phone_number)[0:2] != '09':
            raise ValidationError('Invalid phone number')
        return phone_number