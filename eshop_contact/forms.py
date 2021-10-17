from django import forms
from django.core import validators
from captcha.fields import ReCaptchaField, ReCaptchaV3


class CreateContactForm(forms.Form):
    captcha=ReCaptchaField(
        label='تصویر امنیتی',
        widget=ReCaptchaV3(api_params={
            'hl':'fa'
        }),
        error_messages={
            'required':'لطفا تصویر امنیتی را تایید کنید.'
        }
    )

    full_name=forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'لطفا نام و نام خانوادگی خود را وارد نمایید.','class':'form-control'}),
        label='نام و نام خانوادگی',
        validators=[validators.MaxLengthValidator(150,'نام و نام خانوادگی شما نمیتواند بیش از 150 کاراکتر داشته باشد.')]
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید.','class':'form-control'}),
        label='ایمیل',
        validators=[
            validators.MaxLengthValidator(100, 'ایمیل شما نمیتواند بیش از 100 کاراکتر داشته باشد.')]
    )

    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا عنوان خود را وارد نمایید.','class':'form-control'}),
        label='عنوان',
        validators=[
            validators.MaxLengthValidator(200, 'عنوان شما نمیتواند بیش از 200 کاراکتر داشته باشد.')]
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'لطفا متن پیام خود را وارد نمایید.','class':'form-control','rows':'8'}),
        label='متن پیام'
    )