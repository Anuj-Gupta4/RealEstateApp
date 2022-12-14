# Generated by Django 4.0.5 on 2022-06-25 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('City', models.CharField(max_length=30)),
                ('Price', models.IntegerField()),
                ('Bedroom', models.IntegerField()),
                ('Bathroom', models.IntegerField()),
                ('Floors', models.IntegerField()),
                ('Parking', models.IntegerField()),
                ('Face', models.CharField(max_length=30)),
                ('Area', models.IntegerField()),
                ('Road_Width', models.IntegerField()),
                ('Road_Type', models.CharField(max_length=30)),
                ('Build_Area', models.IntegerField()),
                ('Amenities', models.CharField(max_length=30)),
            ],
        ),
    ]
