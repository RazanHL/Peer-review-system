from django.db import models
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify
from profiles.models import Profiles
import datetime
import random
from django.utils.translation import gettext_lazy as _
import django_filters

STAGE_UNSUBMITTED = (('Unsubmitted'))
STAGE_PRE_REVIEW = (('Pre Review'))
STAGE_UNDER_REVIEW = (('Under Review'))
STAGE_REJECTED = (('Rejected'))
STAGE_ACCEPTED = (('Accepted'))
STAGE_TYPESETTING = (('Typesetting'))
STAGE_READY_FOR_PUBLICATION = (('Pre Publication'))
STAGE_PUBLISHED = (('Published'))
STAGE_CHOICES = [
    (STAGE_UNSUBMITTED, (('Unsubmitted'))),
    (STAGE_PRE_REVIEW, (('Pre Review'))),
    (STAGE_UNDER_REVIEW, (('Under Review'))),
    (STAGE_REJECTED, (('Rejected'))),
    (STAGE_ACCEPTED, (('Accepted'))),
    (STAGE_TYPESETTING, (('Typesetting'))),
    (STAGE_READY_FOR_PUBLICATION, (('Pre Publication'))),
    (STAGE_PUBLISHED, (('Published'))),
]
SCOPE_CHOICES = [
    ('agricultural_economics', ('agricultural economics')),
    ('agriculture_biotechnology', ('agriculture biotechnology')),
    ('crop_production', ('crop production')),
    ('environmental_siences', ('environmental siences')),
    ('food_technology', ('food technology')),
    ('horticulture', ('horticulture')),
    ('livestock_production', ('livestock production')),
    ('natural_resources', ('natural resources')),
    ('plant_protection', ('plant protection')),
]

class Subject(models.Model):
    scope = models.CharField(_('scope'), max_length=255)

    def __str__(self):
        return self.scope

class Article(models.Model):
    slug = models.SlugField(blank=True, null=True, unique=True, max_length = 250) 
    ar_en = models.CharField(_('Language'), max_length=10, blank=True, null=True) 
    country = models.CharField(_('Country'), max_length=20, blank=True, null=True)
    received_date = models.DateField(_('Received Date'), default=datetime.date.today, blank=True, null=True)
    score = models.FloatField(_('Score'), blank=True, null=True)
    current_status = models.CharField(_('Current Status'), max_length=15, choices=STAGE_CHOICES, default=STAGE_UNSUBMITTED, blank=True, null=True)
    volume = models.SmallIntegerField(_('Volume'), blank=True, null=True)
    issue = models.SmallIntegerField(_('Issue'), blank=True, null=True)
    result = models.CharField(_('Result'), max_length=30, blank=True, null=True)
    date_of_editor_decision = models.DateField(_('Date of Editorial Decision'), blank=True, null=True)
    title = models.TextField(_('Arabic Title'))
    en_title = models.TextField(_('English Title'), blank=True, null=True)
    abstract = models.TextField(_('Arabic Abstract'), blank=True, null=True)
    key_words = models.TextField(_('Arabic Keywords'), blank=True, null=True)
    en_abstract = models.TextField(_('English Abstract'), blank=True, null=True)
    en_keyword = models.TextField(_('English Keyword'), blank=True, null=True)
    introduction = models.TextField(_('Introduction'), blank=True, null=True)# RichTextField()
    references =models.TextField(_('References'), blank=True, null=True) # RichTextField()
    file_link = models.FileField(_('Manuscript File'), upload_to='' ,blank=True, null=True)
    no_author_file = models.FileField(_('Manuscript File without Authors'), upload_to='' ,blank=True, null=True)
    copyright_file_link = models.FileField(_('Copyright File'), upload_to='' ,blank=True, null=True)
    revised_pdf_link = models.FileField(_('Revised PDF'), upload_to='' ,blank=True, null=True)
    num_references = models.IntegerField(blank=True, null=True)
    latest_reference = models.IntegerField(blank=True, null=True)
    oldest_reference = models.IntegerField(blank=True, null=True)
    meadian_reference = models.FloatField(blank=True, null=True)
    avg_recent_references = models.FloatField(blank=True, null=True)
    ref_mention_count = models.IntegerField(blank=True, null=True)
    num_figurs = models.IntegerField(blank=True, null=True)
    num_tables = models.IntegerField(blank=True, null=True)
    num_charts = models.IntegerField(blank=True, null=True)
    num_authors = models.IntegerField(blank=True, null=True)
    num_publication = models.IntegerField(blank=True, null=True)
    paper_len = models.FloatField(blank=True, null=True)
    ar_word_count = models.FloatField(blank=True, null=True)
    en_word_count = models.FloatField(blank=True, null=True)
    ar_word_avg = models.FloatField(blank=True, null=True)
    en_word_avg = models.FloatField(blank=True, null=True)
    num_sentences = models.FloatField(blank=True, null=True)
    avg_words_per_sentence = models.FloatField(blank=True, null=True)
    scope = models.ManyToManyField(Subject, blank=True)
    author = models.ManyToManyField(User, blank=True)
    reviewer = models.ManyToManyField(Profiles, blank=True)
    from_page = models.CharField(_('From Page'), max_length= 250, blank=True, null=True)
    to_page = models.CharField(_('To Page'), max_length= 250, blank=True, null=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)   
    notes_to_author = models.TextField(_('Notes to Author'), blank=True, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("article-detailes", args=[str(self.pk)]) # kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.en_keyword + str(random.random()))
        return super().save(*args, **kwargs)

class ArticlesFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = {
            'country': ['icontains'],
            'title': ['icontains'],
            'en_title': ['icontains'],
            'key_words': ['icontains'],
            'en_keyword': ['icontains'],
            'current_status': ['exact'],
            'scope__scope': ['icontains'],
            'author__username': ['icontains'],
            'reviewer__name': ['icontains'],
            'score': ['lt', 'gt'],
            'received_date': ['exact', 'year__gt'],
            'date_of_editor_decision': ['exact', 'year__gt'],
        }

class Article_files(models.Model):
    Article_id = models.ForeignKey(Article, on_delete=models.Case)
    file_directory = models.FileField(max_length=500, upload_to='')

def facility_path(filepath):
    return None


class Reviewer_publication(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    num_current_reviews = models.IntegerField(_('Number of Current Reviews'), blank=True, null=True)
    abstract = models.TextField(_('Abstract'), blank=True, null=True)
    scope = models.ManyToManyField(Subject) #, name=_('scope'))

class Author_Order(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    email = models.EmailField(_('E.mail'), blank=True, null=True)
    order = models.IntegerField(_('order'), blank=True, null=True)
    contact = models.BooleanField(_('contact'), default=False)
    