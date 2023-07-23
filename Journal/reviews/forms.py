from django import forms
from django.conf import settings
from django.core.mail import send_mail
from .models import ReviewDetailes
from django.utils.translation import gettext_lazy as _

class InviteReviewForm(forms.Form):
    subject = forms.CharField(max_length=225, required= False)
    # from_email = forms.EmailField() # initial=str(settings.EMAIL_HOST_USER))
    recipient = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


    def send(self):
        clean_data = super().clean()

        recipient = [clean_data.get('recipient')]
        # from_email = clean_data.get('from_email')
        subject = clean_data.get('subject')
        message = clean_data.get('message')

        send_mail(
            subject = subject,
            message = message,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = recipient
        )

class ReviewForm(forms.ModelForm):
    q1 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q2 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q3 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q4 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q5 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q6 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q7 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q8 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q9 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q10 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q11 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q12 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q13 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    q14 = forms.IntegerField(max_value=5, min_value=1, label='', required=False)
    notes_to_editor = forms.CharField(max_length=300, required=False, label='', widget=forms.Textarea(attrs={'rows': 6}))
    notes_to_author = forms.CharField(max_length=300, required=False, label='', widget=forms.Textarea(attrs={'rows': 6}))
    done_review = forms.BooleanField(required=False,  label='')
    review_file_link = forms.FileField(required=False, label='')
    APPROVAL_CHOICES = (
        ('approve', _('Approve this article after complying with suggested amendments and comments, without return.')),
        ('reject', _('Reject this article and send it back to the author for the following reasons:')),
        ('approve_with_return', _('Return the article to the author to make the required modifications, then return it to me again.')),
    )
    approval = forms.ChoiceField(choices=APPROVAL_CHOICES, widget=forms.RadioSelect(), label='', required=False)
    # , widget=forms.RadioSelect(attrs={
    #     'class': 'text-red',
    # }))

    class Meta:
        model = ReviewDetailes
        fields = ['q1', 'q1_note', 'q2', 'q2_note', 'q3', 'q3_note', 'q4', 'q4_note',
                  'q5', 'q5_note', 'q6', 'q6_note', 'q7', 'q7_note', 'q8', 'q8_note',
                  'q9', 'q9_note', 'q10', 'q10_note', 'q11', 'q11_note', 'q12', 'q12_note',
                  'q13', 'q13_note', 'q14', 'q14_note','approval', 'notes_to_editor', 'notes_to_author',
                  'done_review', 'review_file_link']
        widgets = {
            'q1_note': forms.Textarea(attrs={'rows': 1}), 
            'q2_note': forms.Textarea(attrs={'rows': 1}),
            'q3_note': forms.Textarea(attrs={'rows': 1}),
            'q4_note': forms.Textarea(attrs={'rows': 1}),
            'q5_note': forms.Textarea(attrs={'rows': 1}),
            'q6_note': forms.Textarea(attrs={'rows': 1}),
            'q7_note': forms.Textarea(attrs={'rows': 1}),
            'q8_note': forms.Textarea(attrs={'rows': 1}),
            'q9_note': forms.Textarea(attrs={'rows': 1}),
            'q10_note': forms.Textarea(attrs={'rows': 1}), 
            'q11_note': forms.Textarea(attrs={'rows': 1}), 
            'q12_note': forms.Textarea(attrs={'rows': 1}),
            'q13_note': forms.Textarea(attrs={'rows': 1}),
            'q14_note': forms.Textarea(attrs={'rows': 1}),
        }


# class ReviewDecisionForm(forms.ModelForm):
#     notes_to_editor = forms.CharField(max_length=300,
#                                   widget=forms.Textarea(attrs={
#                                       'cols': 50, 'rows': 6,
#                                   }),
#                                   required=False)
#     notes_to_author = forms.CharField(max_length=300, required=False)
#     APPROVAL_CHOICES = (
#         ('approve', 'Approve this article after complying with suggested amendments and comments, without return.'),
#         ('reject', 'Reject this article and send it back to the author for the following reasons:'),
#         ('approve_with_return', 'Return the article to the author to make the required modifications, then return it to me again.'),
#     )
#     approval = forms.ChoiceField(choices=APPROVAL_CHOICES, required=False, widget=forms.RadioSelect(attrs={
#         'class': 'text-red',
#     }))
#     class Meta:
#         model = ReviewDetailes
#         fields = ['approval', 'notes_to_editor', 'notes_to_author']


