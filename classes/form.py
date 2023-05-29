from django import forms
from . models import Contact, Comment, Blogcomment


class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=200, label="Name", widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Họ tên của bạn',
        'required' : 'required',
    }))

    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Email của bạn',
        'required' : 'required',
    }))

    subject = forms.CharField(max_length=50, label="Subject", widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Chủ đề',
        'required' : 'required',
    }))

    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Lời nhắn của bạn',
        'rows' : '8',
        'required' : 'required',
    }))

    class Meta:
        model = Contact
        fields = '__all__'


class FormComment(forms.ModelForm):
    content = forms.CharField(label="Nội dung", widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : "Nội dung",
        'rows' : '8',
        'required' : 'required',
    }))
    image = forms.ImageField(label="Hình ảnh")

    class Meta:
        model = Comment
        exclude = ('user_avatar',)


class FormBlogcomment(forms.ModelForm):
    content = forms.CharField(label="Nội dung", widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : "Nội dung",
        'rows' : '8',
        'required' : 'required',
    }))
    image = forms.ImageField(label="Hình ảnh")

    class Meta:
        model = Blogcomment
        exclude = ('user_avatar',)