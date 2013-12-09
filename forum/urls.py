from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('app.urls')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='auth_logout'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'', include('social_auth.urls')),

    # Examples:
    # url(r'^$', 'forum.views.home', name='home'),
    # url(r'^forum/', include('forum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
