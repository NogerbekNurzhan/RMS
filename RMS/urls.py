from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from RMS.views import home, unauthorized_close_projects, unauthorized_open_projects, manager_projects, developer_projects, business_analyst_projects, system_analyst_projects

urlpatterns = i18n_patterns(
    # Admin Page
    url(r'^admin/', admin.site.urls),

    # Rosetta Translation Interface Page
    url(r'^rosetta/', include('rosetta.urls')),

    # "Account" Application
    url(r'^account/', include('account.backends.default.urls')),

    # Home Page
    url(r'^$', home, name='home'),

    # Unauthorized Close Projects
    url(r'^unauthorized_close_projects/', unauthorized_close_projects, name='unauthorized_close_projects'),

    # Unauthorized Open Projects
    url(r'^unauthorized_open_projects/', unauthorized_open_projects, name='unauthorized_open_projects'),

    # START: URLs for authorized users
    url(r'^manager_projects/', manager_projects, name='manager_projects'),
    url(r'^developer_projects/', developer_projects, name='developer_projects'),
    url(r'^business_analyst_projects/', business_analyst_projects, name='business_analyst_projects'),
    url(r'^system_analyst_projects/', system_analyst_projects, name='system_analyst_projects'),
    # END: URLs for authorized users

    # Internationalization | Localization
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # Python Social Auth for Django
    url('', include('social_django.urls', namespace='social')),

    # "Project" Application
    url(r'^account/dashboard/', include('project.urls', namespace='project')),

    # "Django Select 2" Application
    url(r'^select2/', include('django_select2.urls')),
)

