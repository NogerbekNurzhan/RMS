"""
    URLconf for registration and activation, using django-registration's default backend.

    If the default behavior of these views is acceptable to you, simply use a line like this in your root URLconf to set up the default URLs for registration::

    (r'^accounts/', include('account.backends.default.urls')),

    This will also automatically set up the views in ``django.contrib.auth`` at sensible default locations.

    If you'd like to customize registration behavior, feel free to set up your own URL patterns for these views instead.
"""


from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from django.views.generic.base import TemplateView
from .views import dashboard
from .views import ActivationView
from .views import RegistrationView
from .views import ReactivationView


urlpatterns = [
    url(r'^activation/complete/$',
        TemplateView.as_view(template_name='account/activation_complete.html'),
        name='activation_complete'),

    url(r'^reactivation/$',
        ReactivationView.as_view(),
        name='reactivation'),

    url(r'^activation/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='activation'),

    url(r'^registration/complete/$',
        TemplateView.as_view(template_name='account/registration_complete.html'),
        name='registration_complete'),

    url(r'^registration/closed/$',
        TemplateView.as_view(template_name='account/registration_closed.html'),
        name='registration_closed'),
]

if getattr(settings, 'INCLUDE_REGISTRATION_URL', True):
    urlpatterns += [
        url(r'^registration/$',
            RegistrationView.as_view(),
            name='registration'),
    ]

if getattr(settings, 'INCLUDE_AUTH_URLS', True):
    urlpatterns += [
        url(r'', include('account.auth_urls')),
    ]
