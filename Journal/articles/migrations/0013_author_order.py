# Generated by Django 4.1.5 on 2023-04-27 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0012_article_from_page_article_notes_to_author_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('contact', models.BooleanField(blank=True, null=True)),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
