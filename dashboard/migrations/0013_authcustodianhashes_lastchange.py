# Generated by Django 3.0.4 on 2020-04-04 15:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_measurement_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='authcustodianhashes',
            name='lastChange',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
