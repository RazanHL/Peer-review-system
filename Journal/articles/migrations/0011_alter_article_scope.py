# Generated by Django 4.1.5 on 2023-03-27 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_alter_article_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='scope',
            field=models.ManyToManyField(blank=True, to='articles.subject'),
        ),
    ]
