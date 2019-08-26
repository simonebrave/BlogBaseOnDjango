from django import forms
from .models import User, Blog

class LoginForm(forms.Form):
    username = forms.CharField(max_length=68, label='', widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField( max_length=256, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))



class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=256, label='输入密码', widget=forms.PasswordInput(attrs={'placeholder': 'Input Password'}))
    password2 = forms.CharField(max_length=256, label='确认密码', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('两个密码不匹配！')
        return cd['password2']


    class Meta:
        model = User
        fields = ('username','email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'})
        }
        labels = {
            'username': '用户名',
            'email': '邮箱地址'
        }


class NewBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'body')

        labels = {
            'title': '标题',
            'body': '正文'
        }
        widgets = {
            'body': forms.TextInput()
        }




