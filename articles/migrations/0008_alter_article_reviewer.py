# Generated by Django 4.1.5 on 2023-03-17 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_profiles_user_type'),
        ('articles', '0007_alter_article_reviewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='reviewer',
            field=models.ManyToManyField(blank=True, to='profiles.profiles'),
        ),
    ]
