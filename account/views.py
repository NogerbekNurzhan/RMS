"""
    Views which allow users to create and activate accounts.
"""

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from account.forms import ReactivationForm

REGISTRATION_FORM_PATH = getattr(settings, 'REGISTRATION_FORM', 'account.forms.RegistrationForm')
REGISTRATION_FORM = import_string(REGISTRATION_FORM_PATH)


class RegistrationView(FormView):
    """
        Base class for user account views.
    """
    disallowed_url = 'registration_closed'
    form_class = REGISTRATION_FORM
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = None
    template_name = 'account/registration_form.html'

    # Метод dispatch
    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        """
            Check that user signup is allowed before even bothering to dispatch or do other processing.
        """
        if not self.registration_allowed():
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new_user = self.register(form)
        success_url = self.get_success_url(new_user)
        try:
            to, args, kwargs = success_url
        except ValueError:
            return redirect(success_url)
        else:
            return redirect(to, *args, **kwargs)

    def registration_allowed(self):
        """
            Override this to enable/disable user account, either globally or on a per-request basis.
        """
        return True

    def register(self, form):
        """
            Implement user-account logic here.
        """
        raise NotImplementedError

    def get_success_url(self, user=None):
        """
            Use the new user when constructing success_url.
        """
        return super(RegistrationView, self).get_success_url()


class ActivationView(TemplateView):
    """
        Base class for user activation views.
    """
    http_method_names = ['get']
    template_name = 'account/activation.html'

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(*args, **kwargs)
        if activated_user:
            success_url = self.get_success_url(activated_user)
            try:
                to, args, kwargs = success_url
            except ValueError:
                return redirect(success_url)
            else:
                return redirect(to, *args, **kwargs)
        return super(ActivationView, self).get(request, *args, **kwargs)

    def activate(self, *args, **kwargs):
        """
            Implement account-activation logic here.
        """
        raise NotImplementedError

    def get_success_url(self, user):
        raise NotImplementedError


class ReactivationView(FormView):
    """
        Base class for resending activation views.
    """
    form_class = ReactivationForm
    template_name = 'account/reactivation_form.html'

    def form_valid(self, form):
        """
            Regardless if resend_activation is successful, display the same confirmation template.
        """
        self.reactivation(form)
        return self.render_form_submitted_template(form)

    def reactivation(self, form):
        """
            Implement resend activation key logic here.
        """
        raise NotImplementedError

    def render_form_submitted_template(self, form):
        """
            Implement rendering of confirmation template here.
        """


class AdminApprovalView(TemplateView):

    http_method_names = ['get']
    template_name = 'account/admin_approval.html'

    def get(self, request, *args, **kwargs):
        approved_user = self.approve(*args, **kwargs)
        if approved_user:
            success_url = self.get_success_url(approved_user)
            try:
                to, args, kwargs = success_url
            except ValueError:
                return redirect(success_url)
            else:
                return redirect(to, *args, **kwargs)
        return super(AdminApprovalView, self).get(request, *args, **kwargs)

    def approve(self, *args, **kwargs):
        """
            Implement admin-approval logic here.
        """
        raise NotImplementedError

    def get_success_url(self, user):
        raise NotImplementedError


def set_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('set_password_done')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'account/set_password_form.html', {'form': form})
