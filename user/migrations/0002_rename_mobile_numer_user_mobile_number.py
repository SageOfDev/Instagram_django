# Generated by Django 4.0.2 on 2022-02-17 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='mobile_numer',
            new_name='mobile_number',
        ),
    ]
