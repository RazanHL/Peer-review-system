# Generated by Django 4.1.5 on 2023-03-02 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profiles_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profiles',
            name='publications',
        ),
        migrations.AddField(
            model_name='profiles',
            name='publications_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
