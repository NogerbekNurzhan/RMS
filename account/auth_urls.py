"""
URL patterns for the views included in ``django.contrib.auth``.

Including these URLs (via the ``include()`` directive) will set up the following patterns based at whatever URL prefix they are included under:

* User login at ``login/``.

* User logout at ``logout/``.

* The two-step password change at ``password/change/`` and ``password/change/done/``.

* The four-step password reset at ``password/reset/``, ``password/reset/confirm/``, ``password/reset/complete/`` and ``password/reset/done/``.

The default registration backend already has an ``include()`` for these URLs, so under the default setup it is not necessary to manually include these views.
Other backends may or may not include them, consult a specific backend's documentation for details.
"""

from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import set_password


urlpatterns = [
    url(r'^login/$',
        auth_views.login,
        name='auth_login',
        kwargs={
            'template_name': 'account/login.html'
        }),

    url(r'^logout/$',
        auth_views.logout,
        name='auth_logout',
        kwargs={
            'template_name': 'account/logout.html'
        }),

    url(r'^password/change/$',
        auth_views.password_change,
        name='auth_password_change',
        kwargs={
            'template_name': 'account/password_change_form.html',
            'post_change_redirect': reverse_lazy('auth_password_change_done')
        }),

    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done',
        kwargs={
            'template_name': 'account/password_change_done.html'
        }),

    url(r'^password/reset/$',
        auth_views.password_reset,
        name='auth_password_reset',
        kwargs={
            'template_name': 'account/password_reset_form.html',
            'email_template_name': 'account/password_reset_email.html',
            'post_reset_redirect': reverse_lazy('auth_password_reset_done')
        }),

    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete',
        kwargs={
            'template_name': 'account/password_reset_complete.html'
        }),

    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done',
        kwargs={
            'template_name': 'account/password_reset_done.html'
        }),

    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='auth_password_reset_confirm',
        kwargs={
            'template_name': 'account/password_reset_confirm.html',
            'post_reset_redirect': reverse_lazy('auth_password_reset_complete')
        }),

    url(r'^set/password/$', set_password, name='set_password'),

    url(r'^set/password/done$', TemplateView.as_view(template_name='account/set_password_done.html'), name='set_password_done'),
]
