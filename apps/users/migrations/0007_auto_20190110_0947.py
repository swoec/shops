# Generated by Django 2.1.4 on 2019-01-10 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_citizen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='title')),
            ],
        ),
        migrations.AlterModelOptions(
            name='citizen',
            options={'verbose_name': 'citizen', 'verbose_name_plural': 'citizen'},
        ),
        migrations.AddField(
            model_name='position',
            name='citizen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Citizen'),
        ),
        migrations.AddField(
            model_name='position',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
        migrations.AddField(
            model_name='position',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
