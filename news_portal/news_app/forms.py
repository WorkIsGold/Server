from django import forms
from .models import News
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    def save(self, commit=True):
        username = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        user = super(RegisterForm, self).save(commit=False)
        user.username = username
        if commit:
            user.save()
        return user
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Этот email уже используется.')

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'summary', 'content']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea(attrs={'rows': 10}),
            #'date_updated': forms.
        }