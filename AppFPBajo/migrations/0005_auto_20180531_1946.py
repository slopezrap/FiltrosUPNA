# Generated by Django 2.0.4 on 2018-05-31 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFPBajo', '0004_auto_20180531_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelofpbajo',
            name='imagePlantilla',
            field=models.ImageField(blank=True, null=True, upload_to='FPBajo', verbose_name='Imagen Plantilla'),
        ),
    ]
