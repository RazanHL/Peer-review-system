# Generated by Django 4.1.5 on 2023-07-08 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_reviewdetailes_approval_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewdetailes',
            name='review_file_link',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Review File'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='approval',
            field=models.CharField(blank=True, choices=[('approve', 'Approve this article after complying with suggested amendments and comments, without return.'), ('reject', 'Reject this article and send it back to the author for the following reasons:'), ('approve_with_return', 'Return the article to the author to make the required modifications, then return it to me again.')], max_length=225, null=True, verbose_name='Approval'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='done_review',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Done Review'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='invitation_expire_on',
            field=models.DateField(blank=True, null=True, verbose_name='Invitation Expire on'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='invited',
            field=models.BooleanField(default=False, verbose_name='Invited'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='invited_at',
            field=models.DateField(blank=True, null=True, verbose_name='Invited at'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Update'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='notes_to_author',
            field=models.TextField(blank=True, null=True, verbose_name='Notes to Authors'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='notes_to_editor',
            field=models.TextField(blank=True, null=True, verbose_name='Notes to Editor'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='replay',
            field=models.CharField(blank=True, choices=[('ACCEPT', 'accept invitation'), ('REJECT', 'reject invitaion')], max_length=225, null=True, verbose_name='Replay'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='review_ends_on',
            field=models.DateField(blank=True, null=True, verbose_name='Review Ends on'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='review_start_on',
            field=models.DateField(blank=True, null=True, verbose_name='Review Start on'),
        ),
        migrations.AlterField(
            model_name='reviewdetailes',
            name='score',
            field=models.FloatField(blank=True, null=True, verbose_name='Score'),
        ),
    ]
