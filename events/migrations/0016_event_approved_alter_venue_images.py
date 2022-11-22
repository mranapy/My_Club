# Generated by Django 4.0.3 on 2022-11-22 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_alter_venue_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='images',
            field=models.ImageField(upload_to='venue/images/', verbose_name='Upload Image'),
        ),
    ]