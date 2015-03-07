# -*- encoding: utf-8 -*-
from django import forms
from .models import Image, UserProfile, Establishment
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import TextInput, PasswordInput
from mysite.widgets import MyClearableFileInput
from municipios.widgets import SelectMunicipioWidget

        
class FormEstablishment(forms.ModelForm):    
    class Meta:
        model = Establishment
        fields = ('name', 'address', 'ec_type', 'img_logo', 'img_vitrin', 'cnpj', 'insc_est', 'phone',
                   'site', 'email', 'zip_code')
        widgets = {
            "img_vitrin": MyClearableFileInput(),
            "img_logo": MyClearableFileInput(),
            "address": SelectMunicipioWidget(),
        }    
    def __init__(self, *args, **kwargs):
        super(FormEstablishment, self).__init__(*args, **kwargs)        
        self.fields['name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Nome'}
        self.fields['address'].widget.attrs = {'class': 'form-control'}
        self.fields['ec_type'].widget.attrs = {'class': 'form-control'}
        self.fields['img_logo'].required = False
        self.fields['img_logo'].widget.attrs = {'class': 'form-control'}
        self.fields['img_vitrin'].required = False
        self.fields['img_vitrin'].widget.attrs = {'class': 'form-control'}
        self.fields['phone'].widget.attrs = {'class': 'form-control', 'placeholder': 'Telefone'}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'E-mail'}
        self.fields['site'].required = False
        self.fields['site'].widget.attrs = {'class': 'form-control', 'placeholder': 'Site'}
        self.fields['zip_code'].widget.attrs = {'class': 'form-control', 'placeholder': 'Cep'}
        self.fields['cnpj'].required = False
        self.fields['cnpj'].widget.attrs = {'class': 'form-control', 'placeholder': 'CNPJ'}
        self.fields['insc_est'].required = False
        self.fields['insc_est'].widget.attrs = {'class': 'form-control', 'placeholder': 'Incrição Estadual'}

class WableAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder':'Senha'})) 
    
    
class WableRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')
        
    def __init__(self, *args, **kwargs):
        super(WableRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Nome'}
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Sobrenome'}
        self.fields['email'].required = False
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'E-mail'}
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'E-mail ou número do celular'}
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Senha'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirme a senha'}
        
    def save(self, commit=True):
        user = super(WableRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Nome'}
        self.fields['last_name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Sobrenome'}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'E-mail'}
        
class UserProfileForm(forms.ModelForm):    
    class Meta:
        model = UserProfile
        fields = ('phone', 'birthday', 'image_field', 'address')
        widgets = {
            "image_field": MyClearableFileInput(),
            "address": SelectMunicipioWidget(),
        }    
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['image_field'].required = False
        self.fields['image_field'].widget.attrs = {'onChange': 'readFile(this);'}
        self.fields['birthday'].required = False
        self.fields['birthday'].widget.attrs = {'class': 'form-control', 'placeholder': 'dd/mm/aaaa'}
        self.fields['phone'].widget.attrs = {'class': 'form-control', 'placeholder': 'Telefone'}
        self.fields['address'].widget.attrs = {'class': 'form-control'}

        

class ImageForm(forms.ModelForm):        
    class Meta:
        model = Image               
        fields = ('image_field', 'cropping_free')
        labels = {
            'image_field': (''),
        }

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image_field'].widget.attrs = {'onChange': 'readURL(this);'}