from django.db import models
from django.contrib.auth.models import User
from articles.models import Article
from django.utils.translation import gettext as _
from django.urls import reverse

REPLAY = [
    ('ACCEPT', _('accept invitation')),
    ('REJECT', _('reject invitaion')),
]
APPROVAL_CHOICES = (
        ('approve', _('Approve this article after complying with suggested amendments and comments, without return.')),
        ('reject', _('Reject this article and send it back to the author for the following reasons:')),
        ('approve_with_return', _('Return the article to the author to make the required modifications, then return it to me again.')),
)
class ReviewDetailes(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    approval = models.CharField(_('Approval'), max_length=225, choices=APPROVAL_CHOICES, blank=True, null=True)
    invited = models.BooleanField(_('Invited'), default=False)
    invited_at = models.DateField(_('Invited at'), blank=True, null=True)
    invitation_expire_on = models.DateField(_('Invitation Expire on'), blank=True, null=True)
    replay = models.CharField(_('Replay'), max_length=225, choices=REPLAY, blank=True, null=True)
    review_start_on = models.DateField(_('Review Start on'), blank=True, null=True)
    review_ends_on = models.DateField(_('Review Ends on'), blank=True, null=True)
    notes_to_editor = models.TextField(_('Notes to Editor'), blank=True, null=True)
    notes_to_author = models.TextField(_('Notes to Authors'), blank=True, null=True)
    q1 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q1_note = models.TextField(blank=True, null=True, verbose_name='')
    q2 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q2_note = models.TextField(blank=True, null=True, verbose_name='')
    q3 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q3_note = models.TextField(blank=True, null=True, verbose_name='')
    q4 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q4_note = models.TextField(blank=True, null=True, verbose_name='')
    q5 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q5_note = models.TextField(blank=True, null=True, verbose_name='')
    q6 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q6_note = models.TextField(blank=True, null=True, verbose_name='')
    q7 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q7_note = models.TextField(blank=True, null=True, verbose_name='')
    q8 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q8_note = models.TextField(blank=True, null=True, verbose_name='')
    q9 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q9_note = models.TextField(blank=True, null=True, verbose_name='')
    q10 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q10_note = models.TextField(blank=True, null=True, verbose_name='')
    q11 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q11_note = models.TextField(blank=True, null=True, verbose_name='')
    q12 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q12_note = models.TextField(blank=True, null=True, verbose_name='')
    q13 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q13_note = models.TextField(blank=True, null=True, verbose_name='')
    q14 = models.SmallIntegerField(blank=True, null=True, verbose_name='')
    q14_note = models.TextField(blank=True, null=True, verbose_name='')
    score = models.FloatField(_('Score'), blank=True, null=True)
    last_update = models.DateTimeField(_('Last Update'), auto_now=True)
    done_review = models.BooleanField(_('Done Review'), blank=True, null=True, default=False)
    review_file_link = models.FileField(_('Review File'), upload_to='' ,blank=True, null=True)

    def get_absolute_url(self):
        return reverse("invite-response", kwargs={'rev_id':self.reviewer_id.id, 'article_id':self.article_id.id})
    # def __str__(self):
    #     return str(self.article_id) + str(self.reviewer_id)
    