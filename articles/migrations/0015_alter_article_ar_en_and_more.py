# Generated by Django 4.1.5 on 2023-06-05 16:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_alter_article_abstract_alter_article_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='ar_en',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_of_editor_decision',
            field=models.DateField(blank=True, null=True, verbose_name='date_of_editor_decision'),
        ),
        migrations.AlterField(
            model_name='article',
            name='file_link',
            field=models.TextField(blank=True, null=True, verbose_name='file_link'),
        ),
        migrations.AlterField(
            model_name='article',
            name='from_page',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='from_page'),
        ),
        migrations.AlterField(
            model_name='article',
            name='issue',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='issue'),
        ),
        migrations.AlterField(
            model_name='article',
            name='notes_to_author',
            field=models.TextField(blank=True, null=True, verbose_name='notes_to_author'),
        ),
        migrations.AlterField(
            model_name='article',
            name='received_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='received_date'),
        ),
        migrations.AlterField(
            model_name='article',
            name='references',
            field=models.TextField(blank=True, null=True, verbose_name='references'),
        ),
        migrations.AlterField(
            model_name='article',
            name='score',
            field=models.FloatField(blank=True, null=True, verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='article',
            name='to_page',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='to_page'),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated_at'),
        ),
        migrations.AlterField(
            model_name='article',
            name='volume',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='volume'),
        ),
        migrations.AlterField(
            model_name='author_order',
            name='contact',
            field=models.BooleanField(default=False, verbose_name='contact'),
        ),
        migrations.AlterField(
            model_name='author_order',
            name='order',
            field=models.IntegerField(blank=True, null=True, verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='reviewer_publication',
            name='abstract',
            field=models.TextField(blank=True, null=True, verbose_name='abstract'),
        ),
        migrations.AlterField(
            model_name='reviewer_publication',
            name='num_current_reviews',
            field=models.IntegerField(blank=True, null=True, verbose_name='num_current_reviews'),
        ),
    ]
