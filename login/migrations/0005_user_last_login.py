# Generated by Django 4.0.3 on 2022-03-05 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_post_unlikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
