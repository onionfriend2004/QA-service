# Generated by Django 5.1.2 on 2024-12-14 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='img/blank_pfp.png', upload_to='avatar/%y/%m/%d', verbose_name='avatar'),
        ),
    ]