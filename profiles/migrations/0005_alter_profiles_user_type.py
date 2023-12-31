# Generated by Django 4.1.5 on 2023-03-16 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_remove_profiles_publications_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='user_type',
            field=models.CharField(choices=[('AUTHOR', 'AUTHOR'), ('REVIEWER', 'REVIEWER'), ('EDITOR', 'EDITOR'), ('PUBLISHER', 'PUBLISHER')], default='AUTHOR', max_length=64),
        ),
    ]
