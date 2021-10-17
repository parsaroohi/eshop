from django import forms
from django.contrib.auth.models import User
from django.core import validators


class EditUserForm(forms.Form):
    first_name=forms.CharField(
        widget=forms.TextInput(attrs={"placeholder":"لطفا نام خود را وارد نمایید."}),
        label="نام"
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "لطفا نام خانوادگی خود را وارد نمایید."}),
        label="نام خانوادگی"
    )


class LoginForm(forms.Form):
    user_name=forms.CharField(
        widget=forms.TextInput(attrs={"placeholder":"لطفا نام کاربری خود را وارد نمایید."}),
        label="نام کاربری"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "لطفا کلمه عبور خود را وارد نمایید."}),
        label="کلمه عبور"
    )

    def clean_user_name(self):
        username=self.cleaned_data.get('user_name')
        is_exists_user=User.objects.filter(username=username).exists()
        if not is_exists_user:
            raise forms.ValidationError('کاربری با مشخصات وارد شده ثبت نام نکرده است.')
        return username


class RegisterForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "لطفا نام کاربری خود را وارد نمایید."}),
        label="نام کاربری",
        validators=[
            validators.MaxLengthValidator(limit_value=20,message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد.'),
            validators.MinLengthValidator(limit_value=5,message='تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 کاراکتر باشد.')
        ]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "لطفا نام ایمیل خود را وارد نمایید."}),
        label="ایمیل",
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نیست.')
        ]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "لطفا کلمه عبور خود را وارد نمایید."}),
        label="کلمه عبور"
    )

    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "لطفا مجدداً کلمه عبور خود را وارد نمایید."}),
        label="تکرار کلمه عبور"
    )

    def clean_re_password(self):
        password=self.cleaned_data.get('password')
        re_password=self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError('کلمه های عبور با یکدیگر تفاوت دارند.')
        return password

    def clean_user_name(self):
        username=self.cleaned_data.get('username')
        is_exists_user=User.objects.filter(username=username).exists()
        if is_exists_user:
            raise forms.ValidationError('کاربری با این نام کاربری قبلاً ثبت نام کرده است.')
        return username

    def clean_email(self):
        email=self.cleaned_data.get('email')
        is_exists_email=User.objects.filter(email=email).exists()
        if is_exists_email:
            raise forms.ValidationError('ایمیل وارد شده تکراری است.')
        return email
