from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Article, Subject, STAGE_CHOICES, Author_Order, Reviewer_publication
from django.forms.widgets import NumberInput
from django.contrib.admin import widgets
from django.db.models import Max
from django.utils.translation import gettext_lazy as _

class ArticleForm(forms.ModelForm):
    APPROVAL_CHOICES = (
        ('approve', _('Approve this article')),
        ('Revise_manuscript', _('this article need further revision after complying with required modifications')),
        ('reject', _('Reject this article and send it back to the author with your comment')),
    )
    LANGUAGE_CHOICES = (
        ('ar', _('Arabic')),
        ('en', _('English')),
    )
    result = forms.ChoiceField(choices=APPROVAL_CHOICES, widget=forms.RadioSelect(), required=False, label=_("Results"))
    ar_en = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=True, label=_("Language"))
    title = forms.Textarea()
    en_title = forms.Textarea()
    country = forms.CharField(max_length=20, required=False, label=_("Country"))
    date_of_editor_decision = forms.DateField(label=_('Date of Editorial Decision'), required=False, widget=forms.TextInput(     
        attrs={'class': 'form-control', 'type': 'date'} 
    ))
    scope = forms.ModelMultipleChoiceField(required=False, label=_('Scope'),
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'title': forms.Textarea(attrs={'rows': 2}),
            'en_title': forms.Textarea(attrs={'rows': 2}),
            'key_words': forms.Textarea(attrs={'rows': 2}),
            'en_keyword': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            "author": _("Authors"),
            "scope": _("Scope"),
            "reviewer": _("Reviewers"),
        }

# class ArticleForm(forms.ModelForm):
#     APPROVAL_CHOICES = (
#         ('approve', _('Approve this article')),
#         ('Revise_manuscript', _('this article need further revision after complying with required modifications')),
#         ('reject', _('Reject this article and send it back to the author with your comment')),
#     )
#     LANGUAGE_CHOICES = (
#         ('ar', _('Arabic')),
#         ('en', _('English')),
#     )
#     result = forms.ChoiceField(choices=APPROVAL_CHOICES, widget=forms.RadioSelect(), required=False)
#     ar_en = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=False, label=_("Language"))
#     country = forms.CharField(max_length=20, required=False, label=_("Country"))
#     date_of_editor_decision = forms.DateField(required=False, widget=forms.TextInput(     
#         attrs={'class': 'form-control', 'type': 'date'} 
#     ))
#     scope = forms.ModelMultipleChoiceField(required=False, label=_('Scope'),
#         queryset=Subject.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )
#     # author, subject

#     class Meta:
#         model = Article
#         fields = '__all__'
#         widgets = {
#             'title': forms.Textarea(attrs={'rows': 2}),
#             'en_title': forms.Textarea(attrs={'rows': 2}),
#             'key_words': forms.Textarea(attrs={'rows': 2}),
#             'en_keyword': forms.Textarea(attrs={'rows': 2}),
#         }
#         labels = {
#             "author": _("Authors"),
#             "scope": _("Scope"),
#             "reviewer": _("Reviewers"),
#         }


class FinalArticleForm(forms.ModelForm):
    APPROVAL_CHOICES = (
        ('approve', _('Approve this article')),
        ('Revise_manuscript', _('this article need further revision after complying with required modifications')),
        ('reject', _('Reject this article and send it back to the author with your comment')),
    )
    result = forms.ChoiceField(choices=APPROVAL_CHOICES, widget=forms.RadioSelect(), required=False)
    date_of_editor_decision = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Article
        fields = '__all__' 
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full shadow-inner p-4 border-2'}),
            'abstract': forms.Textarea(attrs={
                'class': 'w-full shadow-inner p-4 border-2'}),
            'volume': forms.NumberInput(attrs={
                'class': 'rounded-0'}),
        }

class AuthorOrderForm(forms.ModelForm):
   class Meta:
        model = Author_Order
        fields = '__all__'
        labels = {
            'author_id': '',
            'order': '',
            'email': '',
            'contact': '',
        }
        ordering = ('order')
        
AuthorOrderFormSet = forms.inlineformset_factory(
    Article, Author_Order, form=AuthorOrderForm,
    extra=0, can_delete=True, can_delete_extra=True
)


class ReviewerpublicationForm(forms.ModelForm):
    scope = forms.ModelMultipleChoiceField(required=True, label=_('Scope'),
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Reviewer_publication
        fields = '__all__'









# class FinalArticleForm(forms.ModelForm):
#     APPROVAL_CHOICES = (
#         ('approve', _('Approve this article')),
#         ('Revise_manuscript', _('this article need further revision after complying with required modifications')),
#         ('reject', _('Reject this article and send it back to the author with your comment')),
#     )
#     result = forms.ChoiceField(choices=APPROVAL_CHOICES, widget=forms.RadioSelect(), required=False)
#     # current_status = forms.ChoiceField(choices=STAGE_CHOICES, widget=forms.RadioSelect())
#     date_of_editor_decision = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}))

#     class Meta:
#         model = Article
#         fields = '__all__' #["result", "score", "from_page", "to_page","notes_to_author", "current_status", "volume", "issue", "title", "abstract", "date_of_editor_decision"]
        
#         widgets = {
#             'title': forms.TextInput(attrs={
#                 'class': 'w-full shadow-inner p-4 border-2'}),
#             'abstract': forms.Textarea(attrs={
#                 'class': 'w-full shadow-inner p-4 border-2'}),
#             # 'issue_title': forms.TextInput(attrs={
#             #     'class': 'w-full shadow-inner p-4 border-2'}),
#             'volume': forms.NumberInput(attrs={
#                 'class': 'rounded-0'}),
#             # 'issue': forms.NumberInput(attrs={
#             #     'class': 'w-full shadow-inner md:w-1/3 rounded py-4 px-3 mb-6 md:mb-0 border-2'}),
#             # 'state': forms.Select(attrs={
#             #     'class': 'w-full md:w-1/3 rounded py-4 px-3 mb-6 md:mb-0'
#             # })
#         }

# class AuthorOrderForm(forms.ModelForm):

#    class Meta:
#         model = Author_Order
#         fields = '__all__'
#         # widgets = {
#         #     'author_id': forms.InlineForeignKeyField(attrs={'readonly': True})
#         # }
#         labels = {
#             'author_id': '',
#             'order': '',
#             'email': '',
#             'contact': '',
#         }
#         ordering = ('order')
        
# AuthorOrderFormSet = forms.inlineformset_factory(
#     Article, Author_Order, form=AuthorOrderForm,
#     extra=0, can_delete=True, can_delete_extra=True
# )