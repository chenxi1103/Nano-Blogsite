#!/usr/bin/env python
# coding:utf-8
# ------Author:Chenxi Li--------
from django import forms
from django.forms import ModelForm
from .models import userProfile

from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password1 = forms.CharField(max_length = 200,
                                label='Password',
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                label='Confirm password',
                                widget = forms.PasswordInput())
    email = forms.EmailField(max_length=100, label='email')
    firstName = forms.CharField(max_length=30)
    lastName = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if userProfile.objects.filter(email__exact=email):
            raise forms.ValidationError("This Email has already registered!")
        return email

class EditProfile(forms.Form):
    firstName = forms.CharField(label='firstName', max_length=30)
    lastName = forms.CharField(label='lastName', max_length=30,)
    Age = forms.IntegerField(label='Age',max_value=100)
    tel = forms.CharField(label='tel', max_length=11, required=False)
    whatsUp = forms.CharField(label='whatsUp', max_length=420,
                              required=False)

    def clean_Age(self):
        Age = self.cleaned_data['Age']
        if Age < 0 or Age > 100:
           raise forms.ValidationError("Sorry! Your age seems not correct!")
        return Age

class QuickPost(forms.Form):
    Post = forms.CharField(label='Post',max_length=42,required=True)
    Category = forms.CharField(label='Category',max_length=30,)

class changePassword(forms.Form):
    oldPwd = forms.CharField(label='oldPwd',max_length=100,widget = forms.PasswordInput())
    newPwd1 = forms.CharField(label='newPwd1',max_length=100,widget = forms.PasswordInput())
    newPwd2 = forms.CharField(label='newPwd2',max_length=100,widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = super(changePassword, self).clean()
        newPwd1 = cleaned_data.get('newPwd1')
        newPwd2 = cleaned_data.get('newPwd2')

        if newPwd1 and newPwd2 and newPwd1 != newPwd2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

class makeComment(forms.Form):
    comment = forms.CharField(max_length = 42)
