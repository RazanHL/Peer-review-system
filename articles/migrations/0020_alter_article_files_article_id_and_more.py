# Generated by Django 4.1.5 on 2023-06-25 08:17

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_article_copyright_file_link_article_en_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article_files',
            name='Article_id',
            field=models.ForeignKey(on_delete=django.db.models.expressions.Case, to='articles.article'),
        ),
        migrations.AlterField(
            model_name='article_files',
            name='file_directory',
            field=models.FileField(max_length=500, upload_to=''),
        ),
    ]
