# Generated by Django 4.0.3 on 2022-03-04 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_comments_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='unlikes',
            field=models.IntegerField(default=0),
        ),
    ]
