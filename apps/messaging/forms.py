from django import forms
from django.utils.translation import gettext_lazy as _

from apps.organizations.models import OrganizationSettings

from .providers import SECURITY_CHOICES


class EmailSettingsForm(forms.Form):
    is_active = forms.BooleanField(label=_("تفعيل الإرسال بالإيميل"), required=False)
    display_name = forms.CharField(label=_("اسم المرسل اللي هيظهر"), max_length=100, required=False)
    from_email = forms.EmailField(label=_("إيميل المرسل"), widget=forms.EmailInput(attrs={"dir": "ltr"}))
    host = forms.CharField(label=_("سيرفر SMTP"), max_length=200, widget=forms.TextInput(attrs={"dir": "ltr"}))
    port = forms.IntegerField(label=_("Port"), min_value=1, max_value=65535, initial=587)
    security = forms.ChoiceField(label=_("التشفير"), choices=SECURITY_CHOICES, initial="tls")
    username = forms.CharField(label=_("اسم المستخدم"), max_length=200, widget=forms.TextInput(attrs={"dir": "ltr"}))
    password = forms.CharField(
        label=_("كلمة المرور / App Password"),
        required=False,
        strip=True,
        widget=forms.PasswordInput(attrs={"dir": "ltr", "autocomplete": "new-password"}, render_value=False),
        help_text=_("سيبها فاضية لو مش عايز تغيّرها. بتتخزن متشفرة."),
    )

    def __init__(self, *args, has_password=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_password = has_password

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("is_active") and not (cleaned.get("password") or self.has_password):
            self.add_error("password", _("اكتب كلمة المرور عشان تفعّل الإرسال."))
        return cleaned


class TemplatesForm(forms.ModelForm):
    class Meta:
        model = OrganizationSettings
        fields = ["default_email_subject", "default_email_body", "default_whatsapp_message"]
        widgets = {
            "default_email_body": forms.Textarea(attrs={"rows": 9}),
            "default_whatsapp_message": forms.Textarea(attrs={"rows": 6}),
        }


class SendForm(forms.Form):
    subject = forms.CharField(label=_("عنوان الإيميل"), max_length=250)
    body = forms.CharField(label=_("نص الرسالة"), widget=forms.Textarea(attrs={"rows": 9}))
    confirm = forms.BooleanField(label=_("راجعت الأصناف والأسعار بنفسي"), required=False)
