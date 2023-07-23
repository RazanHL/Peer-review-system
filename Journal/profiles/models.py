from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import django_filters
from django.urls import reverse

User._meta.get_field('email')._unique = True

USER_TYPE_CHOICES = (
        ('AUTHOR', _('AUTHOR')),
        ('REVIEWER', _('REVIEWER')),
        ('EDITOR', _('EDITOR')),
        ('PUBLISHER', _('PUBLISHER')),
    )

class Profiles(models.Model):

    user = models.OneToOneField(User, related_name="profiles", on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=150, blank=True, null=True)
    en_name = models.CharField(_('English Name'), max_length=150, blank=True, null=True)
    email2 = models.EmailField(_('E.mail2'), max_length=150, blank=True, null=True)
    address = models.CharField(_('Address'), max_length=255, null=True, blank=True)
    work_address = models.TextField(_('Work Address'), blank=True, null=True)
    en_work_address = models.TextField(_('English Work Address'), blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=32, blank=True, null=True)
    phone2 = models.CharField(_('Phone2'), max_length=32, blank=True, null=True)
    country = models.CharField(_('Country'), max_length=150, null=True, blank=True)
    certificate = models.CharField(_('Certificate'), max_length=15, blank=True, null=True, help_text='الدكتور, المهندس ...')
    en_certificate = models.CharField(_('English Certificate'), max_length=15, blank=True, null=True, help_text='PhD, Eng ...')
    specialist = models.CharField(_('Specialist'), max_length=255, blank=True, null=True, help_text='اقتصاد زراعي, محاصيل, موارد طبيعية ...')
    specific_specialist = models.CharField(_('Specific Specialist'), max_length=255, blank=True, null=True)
    publications_count = models.IntegerField(_('Publications Count'), blank=True, null=True)
    bio = models.TextField(_('Bio'), blank=True, null=True)
    
    user_type = models.CharField(_('User Type'), choices=USER_TYPE_CHOICES, max_length=64, default='AUTHOR')
    
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("update-user-profile", args=[str(self.pk)]) # kwargs={"slug": self.slug})


    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

class ProfilesFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Profiles
        fields = {
            'name': ['icontains'],
            'en_name': ['icontains'],
            'work_address': ['icontains'],
            'en_work_address': ['icontains'],
            'country': ['icontains'],
            'certificate': ['icontains'],
            'en_certificate': ['icontains'],
            'specialist': ['icontains'],
            'specific_specialist': ['icontains'],
            'user_type': ['exact'],
            # 'price': ['lt', 'gt'],
            # 'release_date': ['exact', 'year__gt'],

        }