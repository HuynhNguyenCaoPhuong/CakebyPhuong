from django import forms
from django.contrib.auth.models import User
from . models import Customer


class FormUser(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Username",
        "required" : "required",
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class" : "form-control",
        "placeholder" : "Email",
        "required" : "required",
    }))
    last_name = forms.CharField(max_length=255, label="Họ", widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Họ",
        "required" : "required",
    }))
    first_name = forms.CharField(max_length=255, label="Tên", widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Tên",
        "required" : "required",
    }))
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "Mật Khẩu",
        "required" : "required",
    }))
    confirm_password = forms.CharField(label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "Xác nhận Mật Khẩu",
        "required" : "required",
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


class FormCustomer(forms.ModelForm):
    tel = forms.CharField(max_length=20, label='Điện thoại', widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Điện thoại",
    }))
    address = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={
        "class" : "form-control",
        "placeholder" : "Địa chỉ",
        "rows" : "3",
    }))
    facebook = forms.CharField(max_length=50, label='Facebook', widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Facebook",
    }))

    class Meta:
        model = Customer
        exclude = ('user', 'avatar')