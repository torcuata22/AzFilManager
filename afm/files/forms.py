
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control text-form mx-2 my-1'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control text-form m-2'}), validators=[validate_password])
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control text-form mx-2'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user