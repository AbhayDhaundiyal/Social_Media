# Generated by Django 4.0.3 on 2022-03-04 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_remove_comments_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='by',
            field=models.CharField(default='xx', max_length=200),
        ),
    ]
