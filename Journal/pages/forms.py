from django import forms
from .models import Editorial_board, Contact_journal
from django.utils.translation import gettext as _

class UpdateEditorialBoard(forms.ModelForm):
    class Meta:
        model = Editorial_board
        fields = '__all__'
        labels = {
            "arabic_name": _("Arabic Name"),
            "english_name": _("English Name"),
            "job_title": _("Job Title"),
            "specification": _("Specification"),
            "en_specification": _("en_Specification"),
            "work_address": _("Work Address"),
            "en_work_address": _("en_Work Address"),
            
        }
        # help_texts = {
        #     "name": ("Some useful help text."),
        # }

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Contact_journal
        fields = '__all__'
        labels = {
            "name": _("Name"),
            "email": _("Email"),
            "subject": _("Subject"),
            "message": _("Message"),
        }