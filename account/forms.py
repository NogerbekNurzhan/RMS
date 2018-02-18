"""
Forms and validation code for user registration.

Note that all of these forms assume Django's bundle default ``User`` model;
Since it's not possible for a form to anticipate in advance the needs of custom user models, you will need to write your own forms if you're using a custom model.
"""
from __future__ import unicode_literals

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, EmailInput, PasswordInput
from captcha.fields import ReCaptchaField
from .users import UserModel, UsernameField

User = UserModel()


class RegistrationForm(UserCreationForm):
    """
        Form for registering a new user account.

        Validates that the requested username is not already in use, and requires the password to be entered twice to catch typos.

        Subclasses should feel free to add any additional validation they need, but should avoid defining a ``save()`` method -- the actual saving of collected user data is delegated to the active account backend.
    """
    required_css_class = 'required'
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    recaptcha = ReCaptchaField(
        attrs={'theme': 'light'},
        error_messages={'required': _("You're not a robot, right? You must select this Checkbox.")}
    )

    class Meta:
        model = User
        fields = (UsernameField(), 'email', 'first_name', 'last_name', 'recaptcha')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'placeholder': _('Username')})
        self.fields['username'].required = True
        self.fields['username'].error_messages = {'required': 'This field is required. Please enter your Username.'}

        self.fields['email'].widget = EmailInput(attrs={'placeholder': _('Email address')})
        self.fields['email'].required = True
        self.fields['email'].error_messages = {'required': 'This field is required. Please enter your Email.'}

        self.fields['first_name'].widget = TextInput(attrs={'placeholder': _('First name')})
        self.fields['first_name'].required = True
        self.fields['first_name'].error_messages = {'required': 'Please enter your First Name.'}

        self.fields['last_name'].widget = TextInput(attrs={'placeholder': _('Last name')})
        self.fields['last_name'].required = True
        self.fields['last_name'].error_messages = {'required': 'Please enter your Last Name.'}

        self.fields['password1'].widget = PasswordInput(attrs={'placeholder': _('Password')})
        self.fields['password1'].required = True
        self.fields['password1'].error_messages = {'required': 'This field is required. Please enter your Password.'}

        self.fields['password2'].widget = PasswordInput(attrs={'placeholder': _('Confirm password')})
        self.fields['password2'].required = True
        self.fields['password2'].error_messages = {'required': _('This field is required. Please enter your Confirm Password.')}

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Email already exists."))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Enter the same password as above, for verification."))
        return password2


class RegistrationFormTermsOfService(RegistrationForm):
    """
        Subclass of ``RegistrationForm`` which adds a required checkbox for agreeing to a site's Terms of Service.
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput,
                             label=_('I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})


class RegistrationFormUniqueEmail(RegistrationForm):
    """
        Subclass of ``RegistrationForm`` which enforces uniqueness of email addresses.
    """

    def clean_email(self):
        """
            Validate that the supplied email address is unique for the site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
        Subclass of ``RegistrationForm`` which disallows account with email addresses from popular free web-mail services; moderately useful for preventing automated spam registrations.

        To change the list of banned domains, subclass this form and override the attribute ``bad_domains``.
    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']

    def clean_email(self):
        """
            Check the supplied email address against a list of known free web-mail domains.
        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(
                _("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']


class ReactivationForm(forms.Form):
    required_css_class = 'required'
    email = forms.EmailField(label=_("E-mail"))
