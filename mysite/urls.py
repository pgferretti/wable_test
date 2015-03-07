from django.conf.urls import patterns, include, url, static
from django.conf import settings

from django.contrib import admin
from mysite.forms import WableAuthenticationForm
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mysite.views.index', name='index'),
    url(r'^modelform_example/(?P<user_id>\d+)/$', 'mysite.views.modelform_example', name='frag_form'),
    url(r'^modelform_example/$', 'mysite.views.modelform_example', name='modelform_example'),
       
    url(r'^register/$', 'mysite.views.register', name='register'),
    url(r'^profile/$', 'mysite.views.profile', name='profile'),
    url(r'^login/', 'django.contrib.auth.views.login', {"template_name": "login.html", 'authentication_form': WableAuthenticationForm}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url": "/login/"}),
    url(r'^admin/', include(admin.site.urls)), 
    url(r'^municipios_app/', include('municipios.urls')),

)
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


