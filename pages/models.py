from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
# Create your models here.

editorial_role_choices = (
    ('رئيس_التحرير', 'رئيس التحرير'),
    ('رئيس_التحرير_المشارك', 'رئيس التحرير المشارك'),
    ('أمين_سر_المجلة', 'أمين سر المجلة'),
    ('التحليل_الإحصائي', 'التحليل الإحصائي'),
    ('مشرف_الموقع', 'مشرف الموقع'),
    ('مدقق_لغة_انكليزي', 'مدقق لغة انكليزي'),
    ('مدقق_لغة_عربي', 'مدقق لغة عربي'),
    ('هيئة_التحرير_الدولية', 'هيئة التحرير الدولية'),
    ('هيئة_التحرير_المحلية', 'هيئة التحرير المحلية'),
    ('المحكمين_الدوليين', 'المحكمين الدوليين'),
    ('المحكمين_المحليين', 'المحكمين المحليين'),
)
class Editorial_board(models.Model):
    arabic_name = models.CharField(_('arabic_name'), max_length=250, blank=True, null=True)
    english_name = models.CharField(_('english_name'), max_length=250, blank=True, null=True)    
    job_title = models.CharField(_('job_title'), choices=editorial_role_choices, max_length=250, blank=True, null=True)
    specification = models.CharField(_('specification'), max_length=250, blank=True, null=True)
    en_specification = models.CharField(_('en_specification'), max_length=250, blank=True, null=True)
    work_address = models.TextField(_('work_address'), blank=True, null=True)
    en_work_address = models.TextField(_('en_work_address'), blank=True, null=True)

    def __str__(self):
        return self.english_name

class Contact_journal(models.Model):
    name = models.CharField(_('name'), max_length= 250)
    email = models.EmailField(_('email'))
    subject = models.CharField(_('subject'), max_length= 250, blank=True, null=True)
    message =  models.TextField(_('message'))

    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        return reverse('contact-details', kwargs={'pk': self.pk})