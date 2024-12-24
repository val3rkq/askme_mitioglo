from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    login = forms.CharField(max_length=32)
    password = forms.CharField(max_length=16)

    
class SignUpForm(forms.Form):
    login = forms.CharField(max_length=32, label="Логин")
    email = forms.EmailField(label="Email")
    nickname = forms.CharField(max_length=32, label="Никнейм")
    password = forms.CharField(max_length=16, widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(max_length=16, widget=forms.PasswordInput, label="Подтверждение пароля")
    avatar = forms.ImageField(required=False, label="Аватар")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error("confirm_password", "Пароли не совпадают!")
        return cleaned_data

    def create_user(self):
        user = User.objects.create_user(
            username=self.cleaned_data['login'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.first_name = self.cleaned_data.get('nickname', '')
        user.save()
        return user


class SettingsForm(forms.Form):
    login = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'Login'}),
        label='Login'
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
        label='Email'
    )
    nickname = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'NickName'}),
        label='NickName'
    )
    avatar = forms.ImageField(
        required=False,
        label='Avatar'
    )


class QuestionForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Input title...'}),
        label='Title'
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Input text...', 'rows': 5}),
        label='Text'
    )
    tags = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Input tags, separated by commas'}),
        label='Tags'
    )

class AnswerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Input text...', 'rows': 5}),
        label='Text'
    )