# Generated by Django 2.0.4 on 2018-07-02 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppFPBajo', '0005_auto_20180531_1946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filtro_butterworth',
            old_name='g10',
            new_name='g_10',
        ),
    ]
