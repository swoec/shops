# Generated by Django 2.1.4 on 2018-12-21 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(blank=True, max_length=80, null=True, verbose_name='name')),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], default='female', max_length=6, verbose_name='gender')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='birthday')),
                ('address', models.CharField(blank=True, max_length=120, null=True, verbose_name='address')),
                ('email', models.EmailField(blank=True, max_length=120, null=True, verbose_name='email')),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'user',
            },
        ),
    ]