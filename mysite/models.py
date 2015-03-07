# -*- encoding: utf-8 -*-
from django.db import models
from image_cropping.fields import ImageRatioField, ImageCropField
from django.contrib.auth.models import User
from municipios.models import Municipio
    
class EstablishmentType(models.Model):
    name_type = models.CharField(u'Tipo do Estabelecimento', null=False, max_length=100)
    def __unicode__(self):
        return self.name_type
         
class Establishment(models.Model):
    user = models.ForeignKey(User, related_name='ec_user')
    address = models.OneToOneField(Municipio, related_name='ec_address')
    ec_type = models.OneToOneField(EstablishmentType, related_name='ec_type')
    name = models.CharField(u'Nome do Estabelecimento', null=False, max_length=100)
    img_logo = models.ImageField(upload_to='establishmet/', blank=False, null=True)
    img_vitrin = models.ImageField(upload_to='establishmet/', blank=False, null=True)
    cnpj = models.CharField(u'Cnpj', null=True, max_length=40)
    insc_est = models.CharField(u'Insc. Estadual', null=True, max_length=40)
    phone = models.CharField(u'Telefone', null=False, max_length=50)
    site = models.URLField(u'Site', null=True, max_length=80)
    email = models.EmailField(u'E-mail', null=False, max_length=100)
    zip_code = models.CharField(u'Cep', null=False, max_length=20)
    
    def __unicode__(self):
        return self.nome
    
class UserProfile(models.Model):    
    user = models.OneToOneField(User, related_name='user_profile')
    image_field = models.ImageField(upload_to='profile/', blank=False, null=True)  
    phone = models.CharField(u'Telefone', null=False, max_length=50)
    birthday = models.DateField(u'Nascimento', null=True)
    address = models.OneToOneField(Municipio, related_name='user_address')

    def __unicode__(self):
        return self.user.username
    

class Image(models.Model):
    image_field = ImageCropField(upload_to='image/', blank=False)    
    cropping_free = ImageRatioField('image_field', '200x100', free_crop=False, size_warning=True, verbose_name='')

    def get_cropping_as_list(self):
        if self.cropping:
            return list(map(int, self.cropping.split(',')))
