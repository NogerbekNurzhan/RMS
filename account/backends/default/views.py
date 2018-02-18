from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ... import signals
from ...models import RegistrationProfile
from ...views import ActivationView as BaseActivationView
from ...views import RegistrationView as BaseRegistrationView
from ...views import ReactivationView as BaseReactivationView
from ...users import UserModel


class RegistrationView(BaseRegistrationView):
    """
    A account backend which follows a simple workflow:

    1. User signs up, inactive account is created.

    2. Email is sent to user with activation link.

    3. User clicks activation link, account is now active.

    Using this backend requires that

    * ``account`` be listed in the ``INSTALLED_APPS`` setting (since this backend makes use of models defined in this application).

    * The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying (as an integer) the number of days from account during which a user may activate their account (after that period  expires, activation will be disallowed).

    * The creation of the templates
      ``account/activation_email_subject.txt`` and ``account/activation_email.txt``, which will be used for the activation email.
      See the notes for this backends ``register`` method for details regarding these templates.

    When subclassing this view, you can set the ``SEND_ACTIVATION_EMAIL`` class variable to False to skip sending the new user a confirmation  email or set ``SEND_ACTIVATION_EMAIL`` to ``False``.
    Doing so implies that you will have to activate the user manually from the admin site or send an activation by some other method. For example, by listening for the ``user_registered`` signal.

    Additionally, account can be temporarily closed by adding the setting ``REGISTRATION_OPEN`` and setting it to ``False``.
    Omitting this setting, or setting it to ``True``, will be interpreted as meaning that account is currently open and permitted.

    Internally, this is accomplished via storing an activation key in an instance of ``account.models.RegistrationProfile``.
    See that model and its custom manager for full documentation of its fields and supported operations.
    """
    SEND_ACTIVATION_EMAIL = getattr(settings, 'SEND_ACTIVATION_EMAIL', True)
    success_url = 'registration_complete'

    registration_profile = RegistrationProfile

    def register(self, form):
        """
        Given a username, email address and password, register a new user account, which will initially be inactive.

        Along with the new ``User`` object, a new ``account.models.RegistrationProfile`` will be created, tied to that ``User``, containing the activation key which will be used for this account.

        An email will be sent to the supplied email address; this email should contain an activation link.
        The email will be rendered using two templates.
        See the documentation for ``RegistrationProfile.send_activation_email()`` for information about these templates and the contexts provided to them.

        After the ``User`` and ``RegistrationProfile`` are created and the activation email is sent, the signal ``account.signals.user_registered`` will be sent, with  the new ``User`` as the keyword argument ``user`` and the class of this backend as the sender.
        """
        site = get_current_site(self.request)

        if hasattr(form, 'save'):
            new_user_instance = form.save()
        else:
            new_user_instance = (UserModel().objects.create_user(**form.cleaned_data))

        new_user = self.registration_profile.objects.create_inactive_user(
            new_user=new_user_instance,
            site=site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=self.request,
        )
        signals.user_registered.send(sender=self.__class__, user=new_user, request=self.request)
        return new_user

    def registration_allowed(self):
        """
        Indicate whether account account is currently permitted, based on the value of the setting ``REGISTRATION_OPEN``. This is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is set to ``True``, account is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to ``False``, account is not permitted.

        """
        return getattr(settings, 'REGISTRATION_OPEN', True)


class ActivationView(BaseActivationView):

    registration_profile = RegistrationProfile

    def activate(self, *args, **kwargs):
        """
            Given an an activation key, look up and activate the user account corresponding to that key (if possible).

            After successful activation, the signal ``account.signals.user_activated`` will be sent, with the newly activated ``User`` as the keyword argument ``user`` and the class of this backend as the sender.
        """
        activation_key = kwargs.get('activation_key', '')
        activated_user = (self.registration_profile.objects.activate_user(activation_key))
        if activated_user:
            signals.user_activated.send(sender=self.__class__, user=activated_user, request=self.request)
        return activated_user

    def get_success_url(self, user):
        return ('activation_complete', (), {})


class ReactivationView(BaseReactivationView):

    registration_profile = RegistrationProfile

    def reactivation(self, form):
        """
            Given an email, look up user by email and resend activation key if user is not already activated or previous activation key has not expired.
            Returns True if activation key was successfully sent, False otherwise.
        """
        site = get_current_site(self.request)
        email = form.cleaned_data['email']
        return self.registration_profile.objects.resend_activation_mail(email, site, self.request)

    def render_form_submitted_template(self, form):
        """
            Renders resend activation complete template with the submitted email.
        """
        email = form.cleaned_data['email']
        context = {'email': email}
        return render(self.request, 'account/reactivation_complete.html', context)


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})
