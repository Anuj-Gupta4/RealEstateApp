# Generated by Django 4.0.5 on 2022-12-31 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0007_listing_description_alter_listing_amenities_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='Description',
            field=models.CharField(default='Please describe your estate here. You may also justify the price of your estate here.', max_length=1000),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='listings.listing')),
            ],
        ),
    ]
