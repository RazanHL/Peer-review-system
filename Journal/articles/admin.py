from django.contrib import admin
from .models import Article, Author_Order, Reviewer_publication
# Register your models here.
admin.site.register(Article)
admin.site.register(Author_Order)
admin.site.register(Reviewer_publication)