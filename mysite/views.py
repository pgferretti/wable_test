from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from easy_thumbnails.files import get_thumbnailer
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from mysite import settings
from django.core.files.storage import default_storage
from django.contrib import messages
from easy_thumbnails.source_generators import pil_image
from mysite.models import Image, UserProfile, Establishment
from mysite.forms import ImageForm, WableRegistrationForm, UserProfileForm, UserForm, FormEstablishment

@login_required
def index(request):
    try:
        estab = Establishment.objects.get(user=request.user.id)
    except:    
        estab = None
    if request.method == "POST":
        form = FormEstablishment(request.POST, request.FILES, instance=estab)
        if form.is_valid():
            estab = form.save(commit=False)
            estab.user = request.user
            estab.save()
    else:
        form = FormEstablishment(instance=estab) 
    return render_to_response("index.html", {'form': form},
                              context_instance=RequestContext(request))    
    

def register(request):    
    user_form = WableRegistrationForm()    
    if request.method == "POST":
        user_form = WableRegistrationForm(request.POST)        
        if user_form.is_valid():
            user = user_form.save(commit=False)                 
            if "@" in user.username:
                user.email = user.username 
            user.save()
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password1'))
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/profile/') 
    return render(request, 'register.html', {'user_form': user_form})
   
@login_required  
def profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user.id)
    except:    
        profile = None
    if request.method == "POST":
            clear_thumbnail(request, profile)
            prof_form = UserProfileForm(request.POST, request.FILES, instance=profile)
            user_form = UserForm(request.POST, instance=request.user)
            if request.FILES.get('image_field'):
                request.FILES.get('image_field').name = request.user.id.__str__()+'_'+request.FILES.get('image_field').name
            if prof_form.is_valid() and user_form.is_valid():
                user_form.save()
                if profile is None:
                    profile = prof_form.save(commit=False) 
                    profile.user = request.user
                    profile.save()
                    if profile.image_field:
                        profile = saveImage(profile)
                else:
                    if request.FILES.get('image_field'):
                        profile = prof_form.save()
                        profile = saveImage(profile)
                    else:
                        profile = prof_form.save()
                messages.add_message(request, messages.INFO, 'Perfil salvo com sucesso!')
    else:
        user_form = UserForm(instance=request.user)
        prof_form = UserProfileForm(instance=profile)    
    return render(request, "profile.html", {'profile': profile, 'user_form': user_form, 'prof_form': prof_form})



def modelform_example(request, user_id=None):  
    image = get_object_or_404(Image, pk=user_id) if user_id else None        
    form = ImageForm(instance=image)
    if request.method == "POST":
        print request.FILES.get('image_field')
        form = ImageForm(request.POST, request.FILES, instance=image)  
        if form.is_valid():                            
#             image = form.save()   
            get_thumbnailer(image.image_field).delete_thumbnails()                 
            return HttpResponseRedirect(reverse('frag_form', args=(image.pk,)))        
    else:
        return render(request, 'modelform_example.html', {'form': form, 'image': image})
    
def clear_thumbnail(request, image):
    try:
        if image.image_field and request.FILES.get('image_field'):
            get_thumbnailer(image.image_field).delete()
    except:
        pass    
    
def saveImage(image):
    try:
        width, height = pil_image(image.image_field).size
        if width >= settings.VALID_IMAGE_WIDTH and height >= settings.VALID_IMAGE_HEIGHT:        
            img_name = thumbnail(image.image_field).name
            default_storage.delete(default_storage.location+'/'+image.image_field.__str__()) 
            image.image_field = img_name
            get_thumbnailer(image.image_field).delete_thumbnails()
            image.save()
    except:
        pass
    return image    

def thumbnail(image_path):
    thumbnailer = get_thumbnailer(image_path)
    thumbnail_options = {
        'detail': True,
        'upscale': True,
        'size': settings.IMAGE_CROPPING_THUMB_SIZE,
    }
    thumb = thumbnailer.get_thumbnail(thumbnail_options)
    return thumb


