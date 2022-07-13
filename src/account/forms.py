from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['class'] = 'form-control'
    #     self.fields['username'].widget.attrs['placeholder'] = 'User Name'
    #     self.fields['username'].label = ''
    #     self.fields['username'].help_text = ''
    #
    #     self.fields['password1'].widget.attrs['class'] = 'form-control'
    #     self.fields['password1'].widget.attrs['placeholder'] = 'Password'
    #     self.fields['password1'].label = ''
    #     self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = 'Confirm password'


class EditInfoForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].label = ''
        self.fields['password'].help_text = ''


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'bio', 'image', 'fb_url', 'tw_url', 'in_url', 'yt_url', 'website_url', 'cv']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['label'] = 'Your current job'
        self.fields['fb_url'].label = 'Your Facebook Url'
        self.fields['tw_url'].label = 'Your Twitter Url'
        self.fields['in_url'].label = 'Your Instgrame Url'
        self.fields['yt_url'].label = 'Your YouTube Url'
        self.fields['in_url'].label = 'Your Personal website'


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = 'Old Password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'
        self.fields['old_password'].label = ''
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''


class ResetPasswordForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']
