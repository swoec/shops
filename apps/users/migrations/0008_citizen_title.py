# Generated by Django 2.1.4 on 2019-01-10 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20190110_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='citizen',
            name='title',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='title'),
        ),
    ]
