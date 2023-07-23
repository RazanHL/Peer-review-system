# Generated by Django 4.1.5 on 2023-06-26 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_profiles_address_alter_profiles_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='certificate',
            field=models.CharField(blank=True, help_text='الدكتور, المهندس ...', max_length=15, null=True, verbose_name='Certificate'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='country',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='email2',
            field=models.EmailField(blank=True, max_length=150, null=True, verbose_name='E.mail2'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='phone',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='phone2',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Phone2'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='publications_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Publications Count'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='specialist',
            field=models.CharField(blank=True, help_text='اقتصاد زراعي, محاصيل, موارد طبيعية ...', max_length=255, null=True, verbose_name='Specialist'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='specific_specialist',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Specific Specialist'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='user_type',
            field=models.CharField(choices=[('AUTHOR', 'AUTHOR'), ('REVIEWER', 'REVIEWER'), ('EDITOR', 'EDITOR'), ('PUBLISHER', 'PUBLISHER')], default='AUTHOR', max_length=64, verbose_name='User Type'),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='work_address',
            field=models.TextField(blank=True, null=True, verbose_name='Work Address'),
        ),
    ]
