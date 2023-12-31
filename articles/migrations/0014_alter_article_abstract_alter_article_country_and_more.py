# Generated by Django 4.1.5 on 2023-06-04 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_author_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='abstract',
            field=models.TextField(blank=True, null=True, verbose_name='abstract'),
        ),
        migrations.AlterField(
            model_name='article',
            name='country',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='article',
            name='current_status',
            field=models.CharField(blank=True, choices=[('Unsubmitted', 'Unsubmitted'), ('Pre Review', 'Pre Review'), ('Under Review', 'Under Review'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted'), ('Typesetting', 'Typesetting'), ('Pre Publication', 'Pre Publication'), ('Published', 'Published')], default='Unsubmitted', max_length=15, null=True, verbose_name='current_status'),
        ),
        migrations.AlterField(
            model_name='article',
            name='en_abstract',
            field=models.TextField(blank=True, null=True, verbose_name='en_abstract'),
        ),
        migrations.AlterField(
            model_name='article',
            name='en_keyword',
            field=models.TextField(blank=True, null=True, verbose_name='en_keyword'),
        ),
        migrations.AlterField(
            model_name='article',
            name='introduction',
            field=models.TextField(blank=True, null=True, verbose_name='introduction'),
        ),
        migrations.AlterField(
            model_name='article',
            name='key_words',
            field=models.TextField(blank=True, null=True, verbose_name='key_words'),
        ),
        migrations.AlterField(
            model_name='article',
            name='result',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='result'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.TextField(blank=True, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='author_order',
            name='contact',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='subject',
            name='scope',
            field=models.CharField(max_length=255, verbose_name='scope'),
        ),
    ]
