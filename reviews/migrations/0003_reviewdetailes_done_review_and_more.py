# Generated by Django 4.1.5 on 2023-04-24 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_remove_reviewdetailes_order_reviewdetailes_approval_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewdetailes',
            name='done_review',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='reviewdetailes',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
