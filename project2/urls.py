from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'imagefinder.views.home', name='home'),
    url(r'^profile/$', 'imagefinder.views.profile', name='profile'),
    url(r'^search/$', 'imagefinder.views.search', name='search'),
    url(r'^license/$', 'imagefinder.views.license', name='license'),
    url(r'^show_image/$', 'imagefinder.views.show_image', name='show_image'),
    url(r'^save_image/$', 'imagefinder.views.save_image', name='save_image'),
    url(r'^unfavorite_image/$', 'imagefinder.views.unfavorite_image', name='unfavorite_image'),
    url(r'^featured/$', 'imagefinder.views.featured', name='featured'),
    url(r'^upload/$', 'imagefinder.views.upload', name='upload'),

    # LOGIN AND LOGOUT
    url(r'^register/$', 'imagefinder.views.register', name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    # USER AUTHENTICATION #
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    # Support old style base36 password reset links; remove in Django 1.7
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm_uidb36'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)