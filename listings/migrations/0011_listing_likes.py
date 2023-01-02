# Generated by Django 4.0.5 on 2023-01-02 06:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listings', '0010_comment_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='likes',
            field=models.ManyToManyField(related_name='estate', to=settings.AUTH_USER_MODEL),
        ),
    ]
